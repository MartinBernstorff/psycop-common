"""Flatten the dataset."""
from __future__ import annotations

import logging
from typing import Optional, Sequence

import pandas as pd
import psutil
from psycop.common.feature_generation.application_modules.filter_prediction_times import (
    PredictionTimeFilterer,
)
from psycop.common.feature_generation.application_modules.project_setup import (
    ProjectInfo,
)
from psycop.common.feature_generation.application_modules.save_dataset_to_disk import (
    split_and_save_dataset_to_disk,
)
from psycop.common.feature_generation.application_modules.wandb_utils import (
    wandb_alert_on_exception,
)
from psycop.common.feature_generation.loaders.raw.load_demographic import birthdays
from timeseriesflattener.feature_spec_objects import _AnySpec
from timeseriesflattener.flattened_dataset import TimeseriesFlattener

log = logging.getLogger(__name__)


def flatten_dataset_to_disk(
    project_info: ProjectInfo,
    feature_specs: list[_AnySpec],
    prediction_times_df: pd.DataFrame,
    quarantine_df: pd.DataFrame | None = None,
    quarantine_days: int | None = None,
    split2ids_df: Optional[dict[str, pd.DataFrame]] = None,
    split_names: Sequence[str] = ("train", "val", "test"),
):
    flattened_dataset = create_flattened_dataset(
        project_info=project_info,
        feature_specs=feature_specs,
        prediction_times_df=prediction_times_df,
        quarantine_df=quarantine_df,
        quarantine_days=quarantine_days,
    )

    split_and_save_dataset_to_disk(
        flattened_df=flattened_dataset,
        project_info=project_info,
        split_ids=split2ids_df,
        split_names=split_names,
    )


@wandb_alert_on_exception
def create_flattened_dataset(
    project_info: ProjectInfo,
    feature_specs: list[_AnySpec],
    prediction_times_df: pd.DataFrame,
    add_birthdays: bool = False,
    drop_pred_times_with_insufficient_look_distance: bool = False,
    quarantine_df: pd.DataFrame | None = None,
    quarantine_days: int | None = None,
) -> pd.DataFrame:
    """Create flattened dataset.

    Args:
        feature_specs (list[_AnySpec]): List of feature specifications of any type.
        project_info (ProjectInfo): Project info.
        prediction_times_df (pd.DataFrame): Prediction times dataframe.
            Should contain entity_id and timestamp columns with col_names matching those in project_info.col_names.
        drop_pred_times_with_insufficient_look_distance (bool): Whether to drop prediction times with insufficient look distance.
            See timeseriesflattener tutorial for more info.
        quarantine_df (pd.DataFrame, optional): Quarantine dataframe with "timestamp" and "project_info.col_names.id" columns.
        quarantine_days (int, optional): Number of days to quarantine. Any prediction time within quarantine_days after the timestamps in quarantine_df will be dropped.
        add_birthdays (bool, optional): Whether to add age feature - only possible on Ovartaci, where we can query the date of birth of the patients.

    Returns:
        FlattenedDataset: Flattened dataset.
    """

    filtered_prediction_times_df = PredictionTimeFilterer(
        prediction_times_df=prediction_times_df,
        entity_id_col_name=project_info.col_names.id,
        quarantine_timestamps_df=quarantine_df,
        quarantine_interval_days=quarantine_days,
    ).run_filter()

    flattened_dataset = TimeseriesFlattener(
        prediction_times_df=filtered_prediction_times_df,
        n_workers=min(
            len(feature_specs),
            psutil.cpu_count(logical=True),
        ),
        cache=None,
        drop_pred_times_with_insufficient_look_distance=drop_pred_times_with_insufficient_look_distance,
        predictor_col_name_prefix=project_info.prefix.predictor,
        outcome_col_name_prefix=project_info.prefix.outcome,
        timestamp_col_name=project_info.col_names.timestamp,
        entity_id_col_name=project_info.col_names.id,
    )

    if add_birthdays:
        flattened_dataset.add_age(
            date_of_birth_df=birthdays(),
            date_of_birth_col_name="date_of_birth",
        )

    flattened_dataset.add_spec(spec=feature_specs)

    return flattened_dataset.get_df()
