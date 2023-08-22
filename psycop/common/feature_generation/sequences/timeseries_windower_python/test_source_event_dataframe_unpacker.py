import datetime as dt

from psycop.common.feature_generation.sequences.timeseries_windower_python.events.static_feature import (
    StaticFeature,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.events.temporal_event import (
    TemporalEvent,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.patient import (
    Patient,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.source_event_dataframe_unpacker import (
    SourceEventDataframeUnpacker,
)
from psycop.common.test_utils.str_to_df import str_to_pl_df


def test_temporal_events():
    test_data = str_to_pl_df(
        """patient,timestamp,source,value
1,2020-01-01 00:00:00,source1,0
1,2020-01-01 00:00:00,source1,1
2,2020-01-01 00:00:00,source1,2
                             """,
    )

    patient_1 = Patient(
        patient_id=1,
        _temporal_events=[],
    )
    patient_1.add_events(
        [
            TemporalEvent(
                patient=patient_1,
                timestamp=dt.datetime(year=2020, month=1, day=1),
                value=0,
                source="source1",
                name=None,
            ),
            TemporalEvent(
                patient=patient_1,
                timestamp=dt.datetime(year=2020, month=1, day=1),
                value=1,
                source="source1",
                name=None,
            ),
        ],
    )

    patient_2 = Patient(
        patient_id=2,
    )
    patient_2.add_events(
        [
            TemporalEvent(
                patient=patient_2,
                timestamp=dt.datetime(year=2020, month=1, day=1),
                value=2,
                source="source1",
                name=None,
            ),
        ],
    )
    expected_patients = [patient_1, patient_2]

    unpacked = SourceEventDataframeUnpacker().unpack(
        source_event_dataframes=[test_data],
    )
    assert unpacked == expected_patients


def test_static_features():
    test_data = str_to_pl_df(
        """patient,source,value
1,test,0
                             """,
    )

    expected_patient = Patient(patient_id=1)

    expected_patient.add_events(
        [StaticFeature(source="test", patient=expected_patient, value=0)],
    )

    unpacked = SourceEventDataframeUnpacker().unpack(
        source_event_dataframes=[test_data],
    )

    assert unpacked == [expected_patient]


def test_multiple_event_sources():
    test_data = str_to_pl_df(
        """patient,source,value
1,test,0
                             """,
    )

    test_data2 = str_to_pl_df(
        """patient,source,timestamp,value
1,test2,2023-01-01,1
                             """,
    )

    expected_patient = Patient(patient_id=1)

    expected_patient.add_events(
        [
            StaticFeature(source="test", patient=expected_patient, value=0),
            TemporalEvent(
                source="test2",
                patient=expected_patient,
                timestamp=dt.datetime(2023, 1, 1),
                value=1,
                name=None,
            ),
        ],
    )

    unpacked = SourceEventDataframeUnpacker().unpack(
        source_event_dataframes=[test_data, test_data2],
    )

    assert unpacked == [expected_patient]
