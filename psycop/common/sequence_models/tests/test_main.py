from datetime import datetime
from pathlib import Path

import lightning.pytorch as pl
import lightning.pytorch.loggers as pl_loggers
from lightning.pytorch.callbacks import ModelCheckpoint
import pytest
from torch import nn
from torch.utils.data import DataLoader

from psycop.common.data_structures import Patient, TemporalEvent
from psycop.common.sequence_models import (
    BEHRTEmbedder,
    BEHRTForMaskedLM,
    PatientDataset,
)
from psycop.projects.sequence_models.train import (
    TorchAccelerator,
    TrainingConfig,
    create_trainer,
)


@pytest.fixture()
def patients() -> list[Patient]:
    """
    Returns a list of patient objects
    """

    e1 = TemporalEvent(
        timestamp=datetime(2021, 1, 1),
        value="d1",
        source_type="diagnosis",
        source_subtype="",
    )
    e2 = TemporalEvent(
        timestamp=datetime(2021, 1, 3),
        value="d2",
        source_type="diagnosis",
        source_subtype="",
    )

    patient1 = Patient(
        patient_id=1,
        date_of_birth=datetime(1990, 1, 1),
    )
    patient1.add_events([e1, e2])

    patient2 = Patient(
        patient_id=2,
        date_of_birth=datetime(1993, 3, 1),
    )
    patient2.add_events([e1, e2, e2, e1])

    return [patient1, patient2]


@pytest.fixture()
def patient_dataset(patients: list) -> PatientDataset:
    return PatientDataset(patients)


@pytest.fixture()
def trainable_module(patients: list[Patient]) -> BEHRTForMaskedLM:
    d_model = 32
    emb = BEHRTEmbedder(d_model=d_model, dropout_prob=0.1, max_sequence_length=128)
    emb.fit(patients=patients, add_mask_token=True)

    encoder_layer = nn.TransformerEncoderLayer(
        d_model=d_model,
        nhead=int(d_model / 4),
        dim_feedforward=d_model * 4,
    )
    encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)

    # this includes the loss and the MLM head
    module = BEHRTForMaskedLM(
        embedding_module=emb,
        encoder_module=encoder,
    )
    return module


def test_behrt(patient_dataset: PatientDataset):
    d_model = 32
    emb = BEHRTEmbedder(d_model=d_model, dropout_prob=0.1, max_sequence_length=128)
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=d_model,
        nhead=int(d_model / 4),
        dim_feedforward=d_model * 4,
    )
    encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)

    patients = patient_dataset.patients
    emb.fit(patients, add_mask_token=True)

    behrt = BEHRTForMaskedLM(embedding_module=emb, encoder_module=encoder)

    dataloader = DataLoader(
        patient_dataset,
        batch_size=32,
        shuffle=True,
        collate_fn=behrt.collate_fn,
    )

    for input_ids, masked_labels in dataloader:
        output = behrt(input_ids, masked_labels)
        loss = output["loss"]
        loss.backward()  # ensure that the backward pass works


def test_module_with_trainer(
    patients: list[Patient],
    trainable_module: BEHRTForMaskedLM,
    tmp_path: Path,
):
    """
    Tests the general intended workflow of the Trainer class
    """

    assert isinstance(trainable_module, pl.LightningModule)

    patients = patients * 10
    midpoint = int(len(patients) / 2)
    train_patients = patients[:midpoint]
    val_patients = patients[midpoint:]

    train_dataset = PatientDataset(train_patients)
    val_dataset = PatientDataset(val_patients)

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=2,
        shuffle=True,
        collate_fn=trainable_module.collate_fn,
    )
    val_dataloader = DataLoader(
        val_dataset,
        batch_size=2,
        shuffle=True,
        collate_fn=trainable_module.collate_fn,
    )

    config = TrainingConfig(n_steps=10, accelerator=TorchAccelerator.CPU)
    save_dir = Path(__file__).parent

    wandb_logger = pl_loggers.WandbLogger(
        name=config.run_name,
        save_dir=save_dir,
        offline=config.offline,
        project=config.project_name,
    )

    checkpoint_callback = ModelCheckpoint(
        dirpath=tmp_path / "checkpoints",
        every_n_train_steps=1,
        verbose=True,
    )

    trainer = pl.Trainer(
        accelerator=config.accelerator.value,
        max_steps=config.n_steps,
        val_check_interval=config.validate_every_n_batches,
        logger=wandb_logger,
        callbacks=[checkpoint_callback],
    )

    trainer.fit(
        model=trainable_module,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader,
    )

    # Checkpoints are saved
    checkpoint_paths = list((tmp_path / "checkpoints").glob("*.ckpt"))
    assert len(checkpoint_paths) == 1

    # Checkpoints can be loaded
    trainer = pl.Trainer(
        accelerator=config.accelerator.value,
        max_steps=config.n_steps,
        val_check_interval=config.validate_every_n_batches,
        logger=wandb_logger,
        callbacks=[checkpoint_callback],
        resume_from_checkpoint=checkpoint_paths[0],
    )

    # Are hyperparameters logged? Yes!
