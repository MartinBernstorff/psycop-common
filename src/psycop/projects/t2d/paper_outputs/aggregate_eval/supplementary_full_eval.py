import polars as pl
from psycop.projects.t2d.paper_outputs.aggregate_eval.md_objects import (
    create_supplementary_from_markdown_artifacts,
)
from psycop.projects.t2d.paper_outputs.aggregate_eval.single_pipeline_full_eval import (
    _t2d_create_markdown_artifacts,
    t2d_main_manuscript_eval,
)
from psycop.projects.t2d.paper_outputs.config import BEST_POS_RATE, DEVELOPMENT_GROUP
from psycop.projects.t2d.paper_outputs.run_pipeline_on_train import (
    get_test_pipeline_run,
)
from psycop.projects.t2d.utils.pipeline_objects import EVAL_ROOT, PipelineRun, RunGroup
from wasabi import Printer

msg = Printer(timestamp=True)


def get_best_runs_from_model_type(
    dev_run_group: RunGroup,
    model_type: str,
) -> tuple[PipelineRun]:
    """Get PipelineRun objects for the best runs of a given model type"""
    performance_df = pl.from_pandas(dev_run_group.all_runs_performance_df)

    best_run_df = (
        performance_df.filter(pl.col("model_name") == model_type)
        .sort(by=["roc_auc"], descending=True)
        .groupby(["model_name", "lookahead_days"])
        .head(1)
        .sort(by=["lookahead_days"], descending=False)
    )

    best_run_names = list(best_run_df["run_name"])

    best_runs = tuple(
        PipelineRun(
            group=dev_run_group,
            name=name,
            pos_rate=BEST_POS_RATE,
            create_output_paths_on_init=False,
        )
        for name in best_run_names
    )

    msg.divider(f"Evaluating {[run.name for run in best_runs]}")

    return best_runs


def full_eval_for_supplementary(
    dev_run_group: RunGroup,
    recreate_artifacts: bool = True,
) -> None:
    """Run full evaluation for the supplementary material."""
    best_model_type = "xgboost"
    best_runs_from_model_type = get_best_runs_from_model_type(
        dev_run_group=dev_run_group,
        model_type=best_model_type,
    )

    artifacts = []

    for run in best_runs_from_model_type:
        if recreate_artifacts:
            current_run_artifacts = t2d_main_manuscript_eval(dev_pipeline=run)
        else:
            msg.warn(
                f"recreate_artifacts set to {recreate_artifacts}: Not recreating artifacts",
            )
            run = get_test_pipeline_run(pipeline_to_train=run)  # noqa
            current_run_artifacts = _t2d_create_markdown_artifacts(run=run)

        artifacts += current_run_artifacts

        run_md = create_supplementary_from_markdown_artifacts(
            artifacts=current_run_artifacts,
        )

        with (
            EVAL_ROOT
            / f"supplementary_{run.inputs.cfg.preprocessing.pre_split.min_lookahead_days}_{run.model_type}_{run.name}.md"
        ).open("w") as f:
            f.write(run_md)

    combined_supplementary_md = create_supplementary_from_markdown_artifacts(
        artifacts=artifacts,
        first_table_index=4,
        first_figure_index=3,
    )

    with (EVAL_ROOT / f"supplementary_combined_{dev_run_group.name}.md").open("w") as f:
        f.write(combined_supplementary_md)


if __name__ == "__main__":
    full_eval_for_supplementary(
        dev_run_group=DEVELOPMENT_GROUP,
        recreate_artifacts=False,
    )
