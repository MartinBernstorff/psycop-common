"""Misc.

utilities.
"""
import sys
import tempfile
import time
from collections.abc import Iterable, MutableMapping
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional, Union

import dill as pkl
import numpy as np
import pandas as pd
from omegaconf.dictconfig import DictConfig
from wandb.sdk.wandb_run import Run  # pylint: disable=no-name-in-module
from wasabi import msg

from psycopt2d.model_performance import ModelPerformance

SHARED_RESOURCES_PATH = Path(r"E:\shared_resources")
FEATURE_SETS_PATH = SHARED_RESOURCES_PATH / "feature_sets"
OUTCOME_DATA_PATH = SHARED_RESOURCES_PATH / "outcome_data"
RAW_DATA_VALIDATION_PATH = SHARED_RESOURCES_PATH / "raw_data_validation"
FEATURIZERS_PATH = SHARED_RESOURCES_PATH / "featurizers"
MODEL_PREDICTIONS_PATH = SHARED_RESOURCES_PATH / "model_predictions"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUC_LOGGING_FILE_PATH = PROJECT_ROOT / ".aucs" / "aucs.txt"


def format_dict_for_printing(d: dict) -> str:
    """Format a dictionary for printing. Removes extra apostrophes, formats
    colon to dashes, separates items with underscores and removes curly
    brackets.

    Args:
        d (dict): dictionary to format.
    Returns:
        str: Formatted dictionary.

    Example:
        >>> d = {"a": 1, "b": 2}
        >>> print(format_dict_for_printing(d))
        >>> "a-1_b-2"
    """
    return (
        str(d)
        .replace("'", "")
        .replace(": ", "-")
        .replace("{", "")
        .replace("}", "")
        .replace(", ", "_")
    )


def flatten_nested_dict(
    d: dict,
    parent_key: str = "",
    sep: str = ".",
) -> dict:
    """Recursively flatten an infinitely nested dict.

    E.g. {"level1": {"level2": "level3": {"level4": 5}}}} becomes
    {"level1.level2.level3.level4": 5}.

    Args:
        d (dict): dict to flatten.
        parent_key (str): The parent key for the current dict, e.g. "level1" for the first iteration.
        sep (str): How to separate each level in the dict. Defaults to ".".

    Returns:
        dict: The flattened dict.
    """

    items: list[dict[str, Any]] = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(
                flatten_nested_dict(d=v, parent_key=new_key, sep=sep).items(),
            )  # typing: ignore
        else:
            items.append((new_key, v))

    return dict(items)


def drop_records_if_datediff_days_smaller_than(
    df: pd.DataFrame,
    t2_col_name: str,
    t1_col_name: str,
    threshold_days: Union[float, int],
    inplace: bool = True,
) -> pd.DataFrame:
    """Drop rows where datediff is smaller than threshold_days. datediff = t2 - t1.

    Args:
        df (pd.DataFrame): Dataframe.
        t2_col_name (str): Column name of a time column
        t1_col_name (str): Column name of a time column
        threshold_days (Union[float, int]): Drop if datediff is smaller than this.
        inplace (bool, optional): Defaults to True.

    Returns:
        A pandas dataframe without the records where datadiff was smaller than threshold_days.
    """
    if inplace:
        df.drop(
            df[
                (df[t2_col_name] - df[t1_col_name]) / np.timedelta64(1, "D")
                < threshold_days
            ].index,
            inplace=True,
        )
    else:
        return df[
            (df[t2_col_name] - df[t1_col_name]) / np.timedelta64(1, "D")
            < threshold_days
        ]


def round_floats_to_edge(series: pd.Series, bins: list[float]) -> np.ndarray:
    """Rounds a float to the lowest value it is larger than.

    Args:
        series (pd.Series): The series of floats to round to bin edges.
        bins (list[floats]): Values to round to.

    Returns:
        A numpy ndarray with the borders.
    """
    _, edges = pd.cut(series, bins=bins, retbins=True)
    labels = [f"({abs(edges[i]):.0f}, {edges[i+1]:.0f}]" for i in range(len(bins) - 1)]

    return pd.cut(series, bins=bins, labels=labels)


def calculate_performance_metrics(
    eval_df: pd.DataFrame,
    outcome_col_name: str,
    prediction_probabilities_col_name: str,
    id_col_name: str = "dw_ek_borger",
) -> pd.DataFrame:
    """Log performance metrics to WandB.

    Args:
        eval_df (pd.DataFrame): DataFrame with predictions, labels, and id
        outcome_col_name (str): Name of the column containing the outcome (label)
        prediction_probabilities_col_name (str): Name of the column containing predicted
            probabilities
        id_col_name (str): Name of the id column

    Returns:
        A pandas dataframe with the performance metrics.
    """
    performance_metrics = ModelPerformance.performance_metrics_from_df(
        eval_df,
        prediction_col_name=prediction_probabilities_col_name,
        label_col_name=outcome_col_name,
        id_col_name=id_col_name,
        metadata_col_names=None,
        to_wide=True,
    )

    performance_metrics = performance_metrics.to_dict("records")[0]
    return performance_metrics


def bin_continuous_data(series: pd.Series, bins: list[int]) -> pd.Series:
    """For prettier formatting of continuous binned data such as age.

    Args:
        series (pd.Series): Series with continuous data such as age
        bins (list[int]): Desired bins. Last value creates a bin from the last value to infinity.

    Returns:
        pd.Series: Binned data

    Example:
    >>> ages = pd.Series([15, 18, 20, 30, 32, 40, 50, 60, 61])
    >>> age_bins = [0, 18, 30, 50, 110]
    >>> bin_Age(ages, age_bins)
    0     0-18
    1     0-18
    2    19-30
    3    19-30
    4    31-50
    5    31-50
    6    31-50
    7      51+
    8      51+
    """
    labels = []
    # Apend maximum value from series ot bins set upper cut-off if larger than maximum bins value
    if series.max() > max(bins):
        bins.append(series.max())

    # Create bin labels
    for i, bin_v in enumerate(bins):
        # If not the final bin
        if i < len(bins) - 2:
            # If the difference between the current bin and the next bin is 1, the bin label is a single value and not an interval
            if (bins[i + 1] - bin_v) == 1:
                labels.append(f"{bin_v}")
            # Else generate bin labels as intervals
            else:
                if i == 0:
                    labels.append(f"{bin_v}-{bins[i+1]}")
                elif i < len(bins) - 2:
                    labels.append(f"{bin_v+1}-{bins[i+1]}")
        # If the final bin, the label is the final bin value and a plus sign
        elif i == len(bins) - 2:
            labels.append(f"{bin_v+1}+")
        else:
            continue

    return pd.cut(series, bins=bins, labels=labels)


def positive_rate_to_pred_probs(
    pred_probs: pd.Series,
    positive_rate_thresholds: Iterable,
) -> pd.Series:
    """Get thresholds for a set of percentiles. E.g. if one
    positive_rate_threshold == 1, return the value where 1% of predicted
    probabilities lie above.

    Args:
        pred_probs (pd.Sereis): Predicted probabilities.
        positive_rate_thresholds (Iterable): positive_rate_thresholds

    Returns:
        pd.Series: Thresholds for each percentile
    """

    # Check if percentiles provided as whole numbers, e.g. 99, 98 etc.
    # If so, convert to float.
    if max(positive_rate_thresholds) > 1:
        positive_rate_thresholds = [x / 100 for x in positive_rate_thresholds]

    # Invert thresholds for quantile calculation
    thresholds = [1 - threshold for threshold in positive_rate_thresholds]

    return pd.Series(pred_probs).quantile(thresholds).tolist()


def dump_to_pickle(obj: Any, path: str) -> None:
    """Pickles an object to a file.

    Args:
        obj (Any): Object to pickle.
        path (str): Path to pickle file.
    """
    with open(path, "wb") as f:
        pkl.dump(obj, f)


def read_pickle(path: str) -> Any:
    """Reads a pickled object from a file.

    Args:
        path (str): Path to pickle file.

    Returns:
        Any: Pickled object.
    """
    with open(path, "rb") as f:
        return pkl.load(f)


def write_df_to_file(
    df: pd.DataFrame,
    file_path: Path,
):
    """Write dataset to file. Handles csv and parquet files based on suffix.

    Args:
        df: Dataset
        file_path (str): File name.
    """

    file_suffix = file_path.suffix

    if file_suffix == ".csv":
        df.to_csv(file_path, index=False)
    elif file_suffix == ".parquet":
        df.to_parquet(file_path, index=False)
    else:
        raise ValueError(f"Invalid file suffix {file_suffix}")


def prediction_df_with_metadata_to_disk(
    df: pd.DataFrame,
    cfg: DictConfig,
    run: Optional[Run] = None,
) -> None:
    """Saves prediction dataframe and hydra config to disk. Stored as a dict
    with keys "df" and "cfg".

    Args:
        df (pd.DataFrame): Dataframe to save.
        cfg (DictConfig): Hydra config.
        run (Run): Wandb run. Used for getting name of the run.
    """
    model_args = format_dict_for_printing(cfg.model)

    timestamp = time.strftime("%Y_%m_%d_%H_%M")

    if run and run.name:
        run_descriptor = f"{timestamp}_{run.name}"
    else:
        run_descriptor = f"{timestamp}_{model_args}"[:100]

    if cfg.evaluation.save_model_predictions_on_overtaci and run:
        # Save to overtaci formatted with date
        dir_path = MODEL_PREDICTIONS_PATH / cfg.project.name / run_descriptor
    else:
        # Local path handling
        dir_path = PROJECT_ROOT / "evaluation_results" / run_descriptor

    dir_path.mkdir(parents=True, exist_ok=True)

    # Write the files
    dump_to_pickle(cfg, str(dir_path / "cfg.pkl"))
    write_df_to_file(df, dir_path / "df.parquet")

    msg.good(f"Saved evaluation results to {dir_path}")


def create_wandb_folders():
    """Creates folders to store logs on Overtaci."""
    if sys.platform == "win32":
        (Path(tempfile.gettempdir()) / "debug-cli.onerm").mkdir(
            exist_ok=True,
            parents=True,
        )
        (PROJECT_ROOT / "wandb" / "debug-cli.onerm").mkdir(exist_ok=True, parents=True)


def coerce_to_datetime(date_repr: Union[str, date]) -> datetime:
    """Coerce date or str to datetime."""
    if isinstance(date_repr, str):
        date_repr = date.fromisoformat(
            date_repr,
        )

    if isinstance(date_repr, date):
        date_repr = datetime.combine(
            date_repr,
            datetime.min.time(),
        )

    return date_repr
