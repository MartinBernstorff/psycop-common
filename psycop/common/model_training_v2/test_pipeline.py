from pathlib import Path

from sklearn.pipeline import Pipeline

from psycop.common.model_training_v2.config.baseline_pipeline import (
    train_baseline_model,
)
from psycop.common.model_training_v2.config.baseline_schema import (
    BaselineSchema,
    ProjectInfo,
)
from psycop.common.model_training_v2.config.config_utils import (
    load_baseline_config,
)
from psycop.common.model_training_v2.loggers.base_logger import (
    TerminalLogger,
)
from psycop.common.model_training_v2.trainer.cross_validator_trainer import (
    CrossValidatorTrainer,
)
from psycop.common.model_training_v2.trainer.data.minimal_test_data import (
    MinimalTestData,
)
from psycop.common.model_training_v2.trainer.preprocessing.pipeline import (
    BaselinePreprocessingPipeline,
)
from psycop.common.model_training_v2.trainer.preprocessing.steps.row_filters import (
    AgeFilter,
)
from psycop.common.model_training_v2.trainer.split_trainer import (
    SplitTrainer,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification_pipeline import (
    BinaryClassificationPipeline,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification_task import (
    BinaryClassificationTask,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_metrics import (
    BinaryAUROC,
)
from psycop.common.model_training_v2.trainer.task.estimator_steps import (
    logistic_regression_step,
)


def test_v2_train_model_pipeline(tmpdir: Path):
    logger = TerminalLogger()
    schema = BaselineSchema(
        project_info=ProjectInfo(
            experiment_path=Path(tmpdir),
        ),  # Must recast to Path, since the tmpdir fixture returns a local(), not a Path(). This means it does not implement the .seek() method, which is required when we write the dataset to .parquet.
        logger=logger,
        trainer=SplitTrainer(
            training_data=MinimalTestData(),
            training_outcome_col_name="outcome",
            validation_data=MinimalTestData(),
            validation_outcome_col_name="outcome_val",
            preprocessing_pipeline=BaselinePreprocessingPipeline(
                AgeFilter(min_age=4, max_age=99, age_col_name="pred_age"),
            ),
            task=BinaryClassificationTask(
                pred_time_uuid_col_name="pred_time_uuid",
                task_pipe=BinaryClassificationPipeline(
                    sklearn_pipe=Pipeline([logistic_regression_step()]),
                ),
            ),
            logger=logger,
            metric=BinaryAUROC(),
        ),
    )

    assert train_baseline_model(schema) == 1.0


def test_v2_train_model_pipeline_from_cfg(tmpdir: Path):
    config = load_baseline_config(
        Path(__file__).parent / "config" / "baseline_test_config.cfg",
    )
    config.project_info.Config.allow_mutation = True
    config.project_info.experiment_path = Path(
        tmpdir,
    )  # For some reason, the tmpdir fixture returns a local(), not a Path(). This means it does not implement the .seek() method, which is required when we write the dataset to .parquet.

    assert train_baseline_model(config) == 1.0


def test_v2_crossval_model_pipeline(tmpdir: Path):
    logger = TerminalLogger()
    schema = BaselineSchema(
        project_info=ProjectInfo(experiment_path=tmpdir),
        logger=logger,
        trainer=CrossValidatorTrainer(
            training_data=MinimalTestData(),
            outcome_col_name="outcome",
            preprocessing_pipeline=BaselinePreprocessingPipeline(
                AgeFilter(min_age=4, max_age=99, age_col_name="pred_age"),
            ),
            task=BinaryClassificationTask(
                pred_time_uuid_col_name="pred_time_uuid",
                task_pipe=BinaryClassificationPipeline(
                    sklearn_pipe=Pipeline([logistic_regression_step()]),
                ),
            ),
            metric=BinaryAUROC(),
            n_splits=2,
            group_col_name="pred_time_uuid",
            logger=logger,
        ),
    )

    assert train_baseline_model(schema) == 0.6666666666666667
