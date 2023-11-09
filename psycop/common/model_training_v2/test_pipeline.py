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
    load_config,
)
from psycop.common.model_training_v2.config.populate_registry import (
    populate_baseline_registry,
)
from psycop.common.model_training_v2.loggers.base_logger import (
    TerminalLogger,
)
from psycop.common.model_training_v2.trainer.preprocessing.pipeline import (
    BaselinePreprocessingPipeline,
)
from psycop.common.model_training_v2.trainer.preprocessing.steps.filters import (
    AgeFilter,
)
from psycop.common.model_training_v2.trainer.split_trainer import (
    SplitTrainer,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification import (
    BinaryClassification,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification_pipeline import (
    BinaryClassificationPipeline,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_metrics import (
    BinaryAUROC,
)
from psycop.common.model_training_v2.trainer.task.estimator_steps import (
    logistic_regression_step,
)
from psycop.common.test_utils.str_to_df import str_to_pl_df


def test_v2_train_model_pipeline(tmpdir: Path):
    training_data = str_to_pl_df(
        """pred_time_uuid,pred_1,outcome,pred_age
                                     1,1,1,1
                                     2,1,1,99
                                     3,1,1,99
                                     4,0,0,99
                                     5,0,0,99
                                     6,0,0,99
                                     """,
    )
    logger = TerminalLogger()
    schema = BaselineSchema(
        project_info=ProjectInfo(experiment_path=tmpdir),
        logger=logger,
        trainer=SplitTrainer(
            training_data=training_data,
            training_outcome_col_name="outcome",
            validation_data=training_data,
            validation_outcome_col_name="outcome",
            preprocessing_pipeline=BaselinePreprocessingPipeline(age_filter=
                AgeFilter(min_age=4, max_age=99, age_col_name="pred_age"),
            ),
            task=BinaryClassification(
                pred_time_uuid_col_name="pred_time_uuid",
                task_pipe=BinaryClassificationPipeline(
                    pipe=Pipeline([logistic_regression_step()]),
                ),
                main_metric=BinaryAUROC(),
            ),
            logger=logger,
        ),
    )

    assert train_baseline_model(schema) == 1.0

def test_v2_train_model_pipeline_from_cfg(tmpdir: Path):
    populate_baseline_registry()
    config = load_baseline_config(Path(__file__).parent / "config" / "baseline_test_config.cfg")
    config.project_info.Config.allow_mutation = True
    config.project_info.experiment_path = tmpdir

    pass