import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from sklearn.pipeline import Pipeline

from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification import (
    BinaryClassification,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_classification_pipeline import (
    BinaryClassificationPipeline,
)
from psycop.common.model_training_v2.trainer.task.binary_classification.binary_metrics.binary_auroc import (
    BinaryAUROC,
)
from psycop.common.model_training_v2.trainer.task.estimator_steps.logistic_regression import (
    logistic_regression_step,
)


@pytest.mark.parametrize(
    ("pipe", "main_metric", "x", "y", "main_metric_expected"),
    [
        (
            BinaryClassificationPipeline(
                sklearn_pipe=Pipeline([logistic_regression_step()]),
            ),
            BinaryAUROC(),
            pd.DataFrame({"x": [1, 1, 2, 2], "uuid": [1, 2, 3, 4]}),
            pd.DataFrame({"y": [0, 0, 1, 1]}),
            1.0,
        ),
    ],
)
def test_binary_classification(
    pipe: BinaryClassificationPipeline,
    main_metric: BinaryAUROC,
    x: pd.DataFrame,
    y: pd.DataFrame,
    main_metric_expected: float,
):
    binary_classification_problem = BinaryClassification(
        task_pipe=pipe,
        pred_time_uuid_col_name="uuid",
    )
    binary_classification_problem.train(x=x, y=y, y_col_name="y")

    x["y_hat"] = binary_classification_problem.predict_proba(x=x)
    eval_ds = binary_classification_problem.construct_eval_dataset(
        df=pd.concat([x, y], axis=1),
        y_hat_col="y_hat",
        y_col="y",
    )

    assert main_metric.calculate(eval_ds) == main_metric_expected

    pred_uuids = eval_ds.df.to_pandas()[eval_ds.pred_time_uuid_col]
    assert_series_equal(pred_uuids, x["uuid"])
