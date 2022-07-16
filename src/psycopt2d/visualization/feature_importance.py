from typing import Iterable

import altair as alt
import numpy as np
from interpret.glassbox import ExplainableBoostingClassifier

from psycopt2d.visualization.base_charts import plot_bar_chart


def plot_feature_importances(
    val_X_column_names: Iterable[str],
    feature_importances: Iterable[str],
    top_n_feature_importances: int,
) -> alt.Chart:
    """Plots feature importances.

    Args:
        val_X_column_names (Iterable[str]): Feature names
        feature_importances (np.ndarray): Feature importances

    Returns:
        alt.Chart: Bar chart of feature importances
    """
    feature_importances = np.array(feature_importances)
    # argsort sorts in ascending order, need to reverse
    sorted_idx = feature_importances.argsort()[::-1]

    x_values = np.array(val_X_column_names)[sorted_idx][:top_n_feature_importances]
    y_values = feature_importances[sorted_idx][:top_n_feature_importances]

    return plot_bar_chart(
        x_values=x_values,
        y_values=y_values,
        x_title="Feature name",
        y_title="Feature importance",
    )


def log_emb_feature_importances(model: ExplainableBoostingClassifier):
    pass
