import plotnine as pn
from psycop.common.model_evaluation.binary.subgroup_data import get_auroc_by_input_df
from psycop.projects.t2d.paper_outputs.config import EVAL_RUN
from psycop.projects.t2d.paper_outputs.model_description.robustness.robustness_plot import (
    t2d_plot_robustness,
)
from psycop.projects.t2d.utils.best_runs import ModelRun


def plot_performance_by_n_hba1c(
    run: ModelRun,
) -> pn.ggplot:
    """Plot performance by n hba1c"""
    eval_ds = run.get_eval_dataset(
        custom_columns=["eval_hba1c_within_9999_days_count_fallback_nan"],
    )

    col_name = "eval_hba1c_within_9999_days_count_fallback_nan"
    df = get_auroc_by_input_df(
        eval_dataset=eval_ds,
        input_values=eval_ds.custom_columns[col_name],  # type: ignore
        input_name=col_name,
        bins=[0, 2, 4, 6, 8, 10, 12],
        bin_continuous_input=True,
        confidence_interval=True,
    )

    return t2d_plot_robustness(
        df,
        x_column="eval_hba1c_within_9999_days_count_fallback_nan_binned",
        line_y_col_name="auroc",
        xlab="n HbA1c measurements prior to visit",
        figure_file_name="t2d_auroc_by_hba1c",
    )


if __name__ == "__main__":
    plot_performance_by_n_hba1c(run=EVAL_RUN)
