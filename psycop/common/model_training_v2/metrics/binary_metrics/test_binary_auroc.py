from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
import pytest

from psycop.common.model_training_v2.metrics.binary_metrics.binary_auroc import (
    BinaryAUROC,
)

if TYPE_CHECKING:
    from psycop.common.model_training_v2.classifier_pipelines.binary_classification_pipeline import (
        PredProbaSeries,
    )


@pytest.mark.parametrize(
    ("y_true", "y_pred", "expected"),
    [
        (
            pd.Series([1, 1, 0, 0]),
            pd.Series([0.9, 0.9, 0.1, 0.1]),
            1.0,
        ),
        (
            pd.Series([1, 0, 1, 0]),
            pd.Series([0.9, 0.9, 0.9, 0.9]),
            0.5,
        ),
    ],
)
def test_binary_auroc(y_true: pd.Series[int], y_pred: PredProbaSeries, expected: float):
    auroc = BinaryAUROC()
    calculated_metric = auroc.calculate(y_true=y_true, y_pred=y_pred)
    assert calculated_metric.value == expected
