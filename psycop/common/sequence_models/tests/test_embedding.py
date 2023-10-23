import datetime as dt

import pytest
import torch

from psycop.common.data_structures import Patient, TemporalEvent
from psycop.common.sequence_models.embedders.BEHRT_embedders import BEHRTEmbedder
from psycop.common.sequence_models.embedders.interface import Embedder


@pytest.mark.parametrize(
    "embedding_module",
    [BEHRTEmbedder(d_model=384, dropout_prob=0.1, max_sequence_length=128)],
)
def test_embeddings(patients: list, embedding_module: Embedder):
    """
    Test embedding interface
    """
    embedding_module.fit(patients)

    inputs_ids = embedding_module.collate_patients(patients)

    assert isinstance(inputs_ids, dict)
    assert isinstance(inputs_ids["diagnosis"], torch.Tensor)  # type: ignore
    assert isinstance(inputs_ids["age"], torch.Tensor)  # type: ignore
    assert isinstance(inputs_ids["segment"], torch.Tensor)
    assert isinstance(inputs_ids["position"], torch.Tensor)

    # forward
    embedding_module(inputs_ids)


@pytest.mark.parametrize(
    "embedding_module",
    [BEHRTEmbedder(d_model=384, dropout_prob=0.1, max_sequence_length=128)],
)
def test_diagnosis_mapping(
    patients: list,
    embedding_module: BEHRTEmbedder,
):
    """
    Test mapping of diagnosis from ICD10 to caliber
    """

    patient = Patient(
        patient_id=11,
        date_of_birth=dt.datetime(year=1990, month=1, day=1),
    )

    # Add temporal events to check that diagnosis codes are mapped correctly
    temporal_events = [
        TemporalEvent(
            timestamp=dt.datetime(2021, 1, 1),
            value="A00",
            source_type="diagnosis",
            source_subtype="A",
        ),
        # Check that two different ICD10 codes map to the same caliber code (A00, A30 -> Bacterial Diseases (excl TB))
        TemporalEvent(
            timestamp=dt.datetime(2021, 1, 3),
            value="A30",
            source_type="diagnosis",
            source_subtype="A",
        ),
        # Check that diagnoses with different subtype than A are excluded
        TemporalEvent(
            timestamp=dt.datetime(2021, 1, 3),
            value="A30",
            source_type="diagnosis",
            source_subtype="B",
        ),
        # Check that ICD10 code maps to different caliber code than those above (I65 -> Transient ischaemic attack)
        TemporalEvent(
            timestamp=dt.datetime(2021, 1, 3),
            value="I65",
            source_type="diagnosis",
            source_subtype="A",
        ),
        # Check that F909 is mapped to F90 (Hyperkinetic disorders) since F909 is not in the mapping
        TemporalEvent(
            timestamp=dt.datetime(2021, 1, 3),
            value="F909",
            source_type="diagnosis",
            source_subtype="A",
        ),
    ]

    patient.add_events(temporal_events)

    patient_events: list[tuple[Patient, TemporalEvent]] = [
        (p, e)
        for p in [*patients, patient]
        for e in embedding_module.filter_events(p.temporal_events)
    ]
    diagnosis_codes: list[str] = [e.value for p, e in patient_events]  # type: ignore

    # map diagnosis codes
    mapped_diagnosis_codes = embedding_module.map_icd10_to_caliber(
        diagnosis_codes=diagnosis_codes,
    )

    assert mapped_diagnosis_codes == [
        "Bacterial Diseases (excl TB)",
        "Bacterial Diseases (excl TB)",
        "Transient ischaemic attack",
        "Hyperkinetic disorders",
    ]
