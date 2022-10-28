"""Plotting functions for
1. AUC by calendar time
2. AUC by time from first visit
3. AUC by time until diagnosis
"""
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score

from psycopt2d.evaluation_dataclasses import EvalDataset
from psycopt2d.utils.utils import bin_continuous_data, round_floats_to_edge
from psycopt2d.visualization.base_charts import plot_basic_chart


def _calc_performance(df: pd.DataFrame, metric: Callable) -> float:
    """Calculates performance metrics of a df with 'y' and 'y_hat' columns.

    Args:
        df (pd.DataFrame): dataframe
        metric (Callable): which metric to calculate

    Returns:
        float: performance
    """
    if df.empty:
        return np.nan
    elif metric is roc_auc_score and len(df["y"].unique()) == 1:
        # msg.info("Only 1 class present in bin. AUC undefined. Returning np.nan") This was hit almost once per month, making it very hard to read.
        # Many of our models probably try to predict the majority class.
        # I'm not sure how exactly we want to handle this, but thousands of msg.info is not ideal.
        # For now, suppressing this message.
        return np.nan
    else:
        return metric(df["y"], df["y_hat"])


def create_performance_by_calendar_time_df(
    labels: Iterable[int],
    y_hat: Iterable[int],
    timestamps: Iterable[pd.Timestamp],
    metric_fn: Callable,
    bin_period: str,
) -> pd.DataFrame:
    """Calculate performance by calendar time of prediction.

    Args:
        labels (Iterable[int]): True labels
        y_hat (Iterable[int]): Predicted label or probability depending on metric
        timestamps (Iterable[pd.Timestamp]): Timestamps of predictions
        metric_fn (Callable): Callable which returns the metric to calculate
        bin_period (str): How to bin time. "M" for year/month, "Y" for year

    Returns:
        pd.DataFrame: Dataframe ready for plotting
    """
    df = pd.DataFrame({"y": labels, "y_hat": y_hat, "timestamp": timestamps})
    df["time_bin"] = df["timestamp"].astype(f"datetime64[{bin_period}]")

    output_df = df.groupby("time_bin").apply(_calc_performance, metric_fn)

    output_df = output_df.reset_index().rename({0: "metric"}, axis=1)
    return output_df


def plot_metric_by_calendar_time(
    eval_dataset: EvalDataset,
    y_title: str,
    bin_period: str = "Y",
    save_path: Optional[str] = None,
    metric_fn: Callable = roc_auc_score,
) -> Union[None, Path]:
    """Plot performance by calendar time of prediciton.

    Args:
        eval_dataset (EvalDataset): EvalDataset object
        y_title (str): Title of y-axis.
        bin_period (str): Which time period to bin on. Takes "M" or "Y".
        save_path (str, optional): Path to save figure. Defaults to None.
        metric_fn (Callable): Function which returns the metric.

    Returns:
        Union[None, Path]: Path to saved figure or None if not saved.
    """
    df = create_performance_by_calendar_time_df(
        labels=eval_dataset.y,
        y_hat=eval_dataset.y_hat_probs,
        timestamps=eval_dataset.pred_timestamps,
        metric_fn=metric_fn,
        bin_period=bin_period,
    )
    sort_order = np.arange(len(df))
    return plot_basic_chart(
        x_values=df["time_bin"],
        y_values=df["metric"],
        x_title="Calendar time",
        y_title=y_title,
        sort_x=sort_order,
        plot_type=["line", "scatter"],
        save_path=save_path,
    )


def create_performance_by_time_from_event_df(
    labels: Iterable[int],
    y_hat: Iterable[int],
    event_timestamps: Iterable[pd.Timestamp],
    prediction_timestamps: Iterable[pd.Timestamp],
    metric_fn: Callable,
    direction: str,
    bins: Iterable[float],
    pretty_bins: Optional[bool] = True,
    drop_na_events: Optional[bool] = True,
) -> pd.DataFrame:
    """Create dataframe for plotting performance metric from time to or from
    some event (e.g. time of diagnosis, time from first visit).

    Args:
        labels (Iterable[int]): True labels
        y_hat (Iterable[int]): Predicted probabilities or labels depending on metric
        event_timestamps (Iterable[pd.Timestamp]): Timestamp of event (e.g. first visit)
        prediction_timestamps (Iterable[pd.Timestamp]): Timestamp of prediction
        metric_fn (Callable): Which performance metric function to use (e.g. roc_auc_score)
        direction (str): Which direction to calculate time difference.
        Can either be 'prediction-event' or 'event-prediction'.
        bins (Iterable[float]): Bins to group by.
        pretty_bins (bool, optional): Whether to prettify bin names. I.e. make
            bins look like "1-7" instead of "[1-7)". Defaults to True.
        drop_na_events (bool, optional): Whether to drop rows where the event is NA. Defaults to True.

    Returns:
        pd.DataFrame: Dataframe ready for plotting
    """

    df = pd.DataFrame(
        {
            "y": labels,
            "y_hat": y_hat,
            "event_timestamp": event_timestamps,
            "prediction_timestamp": prediction_timestamps,
        },
    )
    # Drop rows with no events if specified
    if drop_na_events:
        df = df.dropna(subset=["event_timestamp"])

    # Calculate difference in days between prediction and event
    if direction == "event-prediction":
        df["days_from_event"] = (
            df["event_timestamp"] - df["prediction_timestamp"]
        ) / np.timedelta64(1, "D")

    elif direction == "prediction-event":
        df["days_from_event"] = (
            df["prediction_timestamp"] - df["event_timestamp"]
        ) / np.timedelta64(1, "D")

    else:
        raise ValueError(
            f"Direction should be one of ['event-prediction', 'prediction-event'], not {direction}",
        )

    # bin data
    bin_fn = bin_continuous_data if pretty_bins else round_floats_to_edge
    df["days_from_event_binned"] = bin_fn(df["days_from_event"], bins=bins)

    # Calc performance and prettify output
    output_df = df.groupby("days_from_event_binned").apply(_calc_performance, metric_fn)
    output_df = output_df.reset_index().rename({0: "metric"}, axis=1)
    return output_df


def plot_auc_by_time_from_first_visit(
    eval_dataset: EvalDataset,
    bins: tuple = (0, 28, 182, 365, 730, 1825),
    prettify_bins: Optional[bool] = True,
    save_path: Optional[Path] = None,
) -> Union[None, Path]:
    """Plot AUC as a function of time to first visit.

    Args:
        eval_dataset (EvalDataset): EvalDataset object
        bins (list, optional): Bins to group by. Defaults to [0, 28, 182, 365, 730, 1825].
        prettify_bins (bool, optional): Prettify bin names. I.e. make
        bins look like "1-7" instead of "[1-7)" Defaults to True.
        save_path (Path, optional): Path to save figure. Defaults to None.

    Returns:
        Union[None, Path]: Path to saved figure or None if not saved.
    """
    eval_df = pd.DataFrame(
        {"ids": eval_dataset.ids, "pred_timestamps": eval_dataset.pred_timestamps},
    )

    first_visit_timestamps = eval_df.groupby("ids")["pred_timestamps"].transform("min")

    df = create_performance_by_time_from_event_df(
        labels=eval_dataset.y,
        y_hat=eval_dataset.y_hat_probs,
        event_timestamps=first_visit_timestamps,
        prediction_timestamps=eval_dataset.pred_timestamps,
        direction="prediction-event",
        bins=bins,
        pretty_bins=prettify_bins,
        drop_na_events=False,
        metric_fn=roc_auc_score,
    )

    sort_order = np.arange(len(df))
    return plot_basic_chart(
        x_values=df["days_from_event_binned"],
        y_values=df["metric"],
        x_title="Days from first visit",
        y_title="AUC",
        sort_x=sort_order,
        plot_type=["line", "scatter"],
        save_path=save_path,
    )


def plot_metric_by_time_until_diagnosis(
    eval_dataset: EvalDataset,
    bins: Iterable[int] = (
        -1825,
        -730,
        -365,
        -182,
        -28,
        -0,
    ),
    pretty_bins: bool = True,
    metric_fn: Callable = f1_score,
    y_title: str = "F1",
    save_path: Optional[Path] = None,
) -> Union[None, Path]:
    """Plots performance of a specified performance metric in bins of time
    until diagnosis. Rows with no date of diagnosis (i.e. no outcome) are
    removed.

    Args:
        eval_dataset (EvalDataset): EvalDataset object
        bins (list, optional): Bins to group by. Negative values indicate days after
        diagnosis. Defaults to [ -1825, -730, -365, -182, -28, -14, -7, -1, 0, 1, 7, 14, 28, 182, 365, 730, 1825] (which is stupid).
        pretty_bins (bool, optional): Whether to prettify bin names. Defaults to True.
        metric_fn (Callable): Which performance metric  function to use.
        y_title (str): Title for y-axis (metric name)
        save_path (Path, optional): Path to save figure. Defaults to None.

    Returns:
        Union[None, Path]: Path to saved figure if save_path is specified, else None
    """
    df = create_performance_by_time_from_event_df(
        labels=eval_dataset.y,
        y_hat=eval_dataset.y_hat_int,
        event_timestamps=eval_dataset.outcome_timestamps,
        prediction_timestamps=eval_dataset.pred_timestamps,
        direction="event-prediction",
        bins=bins,
        pretty_bins=pretty_bins,
        drop_na_events=True,
        metric_fn=metric_fn,
    )
    sort_order = np.arange(len(df))

    return plot_basic_chart(
        x_values=df["days_from_event_binned"],
        y_values=df["metric"],
        x_title="Days to diagnosis",
        y_title=y_title,
        sort_x=sort_order,
        plot_type=["scatter", "line"],
        save_path=save_path,
    )
