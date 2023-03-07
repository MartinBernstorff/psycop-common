"""Plotting function for performance by age at time of predictio."""

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Optional, Union

from psycop_model_training.model_eval.base_artifacts.plots.base_charts import (
    plot_basic_chart,
)
from psycop_model_training.model_eval.base_artifacts.plots.utils import (
    create_performance_by_input,
)
from psycop_model_training.model_eval.dataclasses import EvalDataset
from sklearn.metrics import roc_auc_score


def plot_performance_by_age(
    eval_dataset: EvalDataset,
    save_path: Optional[Path] = None,
    bins: Sequence[Union[int, float]] = (18, 25, 35, 50, 70),
    bin_continuous_input: Optional[bool] = True,
    metric_fn: Callable = roc_auc_score,
    y_limits: Optional[tuple[float, float]] = (0.5, 1.0),
) -> Union[None, Path]:
    """Plot bar plot of performance (default AUC) by age at time of prediction.

    Args:
        eval_dataset: EvalDataset object
        bins (Sequence[Union[int, float]]): Bins to group by. Defaults to (18, 25, 35, 50, 70, 100).
        bin_continuous_input (bool, optional): Whether to bin input. Defaults to True.
        metric_fn (Callable): Callable which returns the metric to calculate
        save_path (Path, optional): Path to save figure. Defaults to None.
        y_limits (tuple[float, float], optional): y-axis limits. Defaults to (0.5, 1.0).

    Returns:
        Union[None, Path]: Path to saved figure or None if not saved.
    """

    df = create_performance_by_input(
        eval_dataset=eval_dataset,
        input_values=eval_dataset.age,
        input_name="age",
        metric_fn=metric_fn,
        bins=bins,
        bin_continuous_input=bin_continuous_input,
    )

    sort_order = sorted(df["age_binned"].unique())

    return plot_basic_chart(
        x_values=df["age_binned"],
        y_values=df["metric"],
        x_title="Age",
        y_title="AUC",
        sort_x=sort_order,
        y_limits=y_limits,
        plot_type=["bar"],
        save_path=save_path,
    )
