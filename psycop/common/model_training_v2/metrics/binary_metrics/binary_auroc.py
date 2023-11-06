import pandas as pd
from sklearn.metrics import roc_auc_score

from psycop.common.model_training_v2.classifier_pipelines.binary_classification_pipeline import (
    PredProbaSeries,
)
from psycop.common.model_training_v2.metrics.base_metric import CalculatedMetric
from psycop.common.model_training_v2.metrics.binary_metrics.base_binary_metric import (
    BinaryMetric,
)


class BinaryAUROC(BinaryMetric):
    def calculate(
        self,
        y_true: pd.Series[int],
        y_pred: PredProbaSeries,
    ) -> CalculatedMetric:
        return CalculatedMetric(
            name="BinaryAUROC",
            value=float(roc_auc_score(y_true=y_true, y_score=y_pred)),
        )
