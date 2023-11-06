from typing import Protocol

import pandas as pd

from psycop.common.model_training_v2.classifier_pipelines.binary_classification_pipeline import (
    PredProbaSeries,
)
from psycop.common.model_training_v2.metrics.base_metric import CalculatedMetric


class BinaryMetric(Protocol):
    def calculate(
        self,
        y_true: pd.Series[int],
        y_pred: PredProbaSeries,
    ) -> CalculatedMetric:
        ...
