import polars as pl
import pytest

from psycop.common.model_training_v2.classifier_pipelines.binary_classification_pipeline import (
    BinaryClassificationPipeline,
)
from psycop.common.model_training_v2.classifier_pipelines.estimator_steps.logistic_regression import (
    logistic_regression_step,
)
from psycop.common.model_training_v2.metrics.binary_metrics.base_binary_metric import (
    BinaryMetric,
)
from psycop.common.model_training_v2.metrics.binary_metrics.binary_auroc import (
    BinaryAUROC,
)
from psycop.common.model_training_v2.presplit_preprocessing.polars_frame import (
    PolarsFrame,
)
from psycop.common.model_training_v2.problem_type.binary_classification import (
    BinaryClassification,
)


@pytest.mark.parametrize(
    ("pipe", "main_metric", "x", "y", "main_metric_expected"),
    [
        (
            BinaryClassificationPipeline(steps=[logistic_regression_step()]),
            BinaryAUROC(),
            pl.DataFrame({"x": [1, 1, 2, 2], "uuid": ["a", "b", "c", "d"]}),
            pl.DataFrame({"y": [0, 0, 1, 1]}),
            1.0,
        ),
    ],
)
def test_binary_classification(
    pipe: BinaryClassificationPipeline,
    main_metric: BinaryMetric,
    x: PolarsFrame,
    y: pl.DataFrame,
    main_metric_expected: float,
):
    binary_classification_problem = BinaryClassification(
        pipe=pipe,
        main_metric=main_metric,
        pred_time_uuid_col_name="uuid",
    )
    binary_classification_problem.train(x=x, y=y)

    result = binary_classification_problem.evaluate(x=x, y=y)
    assert result.metric.value == main_metric_expected
