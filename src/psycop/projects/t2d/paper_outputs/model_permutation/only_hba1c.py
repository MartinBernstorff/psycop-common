from collections.abc import Sequence
from pathlib import Path

import polars as pl
from psycop.projects.t2d.paper_outputs.model_permutation.modified_dataset import (
    FeatureModifier,
    evaluate_pipeline_with_modified_dataset,
)
from psycop.projects.t2d.utils.pipeline_objects import PipelineRun, SplitNames
from wasabi import Printer

msg = Printer(timestamp=True)


class Hba1cOnly(FeatureModifier):
    def __init__(self):
        self.name = "hba1c_only"

    def modify_features(
        self,
        run: PipelineRun,
        output_dir_path: Path,
        input_split_names: Sequence[SplitNames],
        output_split_name: str,
        recreate_dataset: bool,
    ) -> None:
        if output_dir_path.exists() and not recreate_dataset:
            msg.info("Boolean dataset has already been created, returning")
            return

        df: pl.LazyFrame = pl.concat(
            run.inputs.get_flattened_split_as_lazyframe(split)
            for split in input_split_names
        )

        hba1c_only_df = self._keep_only_hba1c_predictors(
            df,
            predictor_prefix=run.inputs.cfg.data.pred_prefix,
        )

        msg.info(f"Collecting modified df with input_splits {input_split_names}")
        hba1c_only_df = hba1c_only_df.collect()

        output_dir_path.mkdir(exist_ok=True, parents=True)
        hba1c_only_df.write_parquet(output_dir_path / f"{output_split_name}.parquet")

    @staticmethod
    def _keep_only_hba1c_predictors(
        df: pl.LazyFrame,
        predictor_prefix: str,
    ) -> pl.LazyFrame:
        non_hba1c_pred_cols = [
            c
            for c in df.schema
            if "hba1c" not in c
            and predictor_prefix in c
            and "pred_age" not in c
            and "pred_sex" not in c
        ]
        hba1c_only_df = df.drop(non_hba1c_pred_cols)

        non_five_year_hba1c = [
            c for c in df.schema if "pred_hba1c" in c and "1825" not in c
        ]
        five_year_hba1c_only = hba1c_only_df.drop(non_five_year_hba1c)

        non_mean_hba1c = [
            c
            for c in five_year_hba1c_only.schema
            if "pred_hba1c" in c and "_mean_" not in c
        ]
        mean_five_year_hba1c_only = five_year_hba1c_only.drop(non_mean_hba1c)

        return mean_five_year_hba1c_only


if __name__ == "__main__":
    from copy import copy

    from psycop.projects.t2d.paper_outputs.selected_runs import (
        BEST_EVAL_PIPELINE,
    )

    run = copy(BEST_EVAL_PIPELINE)
    cfg = run.inputs.cfg

    # Set XGBoost to default hyperparameters
    cfg.model.Config.allow_mutation = True
    cfg.model.args = {
        "n_estimators": 100,
        "alpha": 0,
        "lambda": 1,
        "max_depth": 6,
        "learning_rate": 0.3,
        "gamma": 0,
        "grow_policy": "depthwise",
    }

    evaluate_pipeline_with_modified_dataset(
        run=BEST_EVAL_PIPELINE,
        feature_modifier=Hba1cOnly(),
        rerun_if_exists=True,
    )
