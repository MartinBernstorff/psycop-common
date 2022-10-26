"""Tests for all our visualisations.

Mainly tests that they run without errors.
"""
# pylint: disable=missing-function-docstring
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import f1_score, roc_auc_score

from psycopt2d.utils import positive_rate_to_pred_probs
from psycopt2d.visualization import plot_prob_over_time
from psycopt2d.visualization.base_charts import plot_basic_chart
from psycopt2d.visualization.feature_importance import plot_feature_importances
from psycopt2d.visualization.performance_over_time import (
    plot_auc_by_time_from_first_visit,
    plot_metric_by_time_until_diagnosis,
    plot_performance_by_calendar_time,
)
from psycopt2d.visualization.performance_by_n_hba1c import (
    plot_performance_by_n_hba1c,
)
from psycopt2d.visualization.performance_by_age import (
    plot_performance_by_age,
)
from psycopt2d.visualization.sens_over_time import (
    create_sensitivity_by_time_to_outcome_df,
    plot_sensitivity_by_time_to_outcome_heatmap,
)


@pytest.fixture(scope="function")
def df():
    repo_path = Path(__file__).parent
    path = repo_path / "test_data" / "synth_eval_data.csv"
    df = pd.read_csv(path)

    # Convert all timestamp cols to datetime[64]ns
    for col in [col for col in df.columns if "timestamp" in col]:
        df[col] = pd.to_datetime(df[col])

    df["n_hba1c"] = np.random.randint(0, 8, df.shape[0])

    df["age"] = np.random.uniform(18, 90, df.shape[0])

    return df


def test_prob_over_time(df, tmp_path):
    plot_prob_over_time(
        patient_id=df["dw_ek_borger"],
        timestamp=df["timestamp"],
        pred_prob=df["pred_prob"],
        outcome_timestamp=df["timestamp_t2d_diag"],
        label=df["label"],
        look_behind_distance=500,
        save_path=tmp_path,
    )


def test_get_sens_by_time_to_outcome_df(df):
    create_sensitivity_by_time_to_outcome_df(
        labels=df["label"],
        y_hat_probs=df["pred"],
        outcome_timestamps=df["timestamp_t2d_diag"],
        prediction_timestamps=df["timestamp"],
        pred_proba_threshold=0.5,
    )


def test_plot_bar_chart(df):
    plot_df = create_sensitivity_by_time_to_outcome_df(
        labels=df["label"],
        y_hat_probs=df["pred"],
        outcome_timestamps=df["timestamp_t2d_diag"],
        prediction_timestamps=df["timestamp"],
        pred_proba_threshold=0.5,
    )
    plot_basic_chart(
        x_values=plot_df["days_to_outcome_binned"],
        y_values=plot_df["sens"],
        x_title="Days to outcome",
        y_title="Sensitivity",
        plot_type="bar",
    )


def test_plot_performance_by_n_hba1c(df):
    plot_performance_by_n_hba1c(
        labels=df["label"],
        y_hat=df["pred"],
        n_hba1c=df["n_hba1c"],
    )


def test_plot_performance_by_age(df):
    plot_performance_by_age(
        labels=df["label"],
        y_hat=df["pred"],
        age=df["age"],
    )


def test_plot_performance_by_calendar_time(df):
    plot_performance_by_calendar_time(
        labels=df["label"],
        y_hat=df["pred"],
        timestamps=df["timestamp"],
        bin_period="M",
        metric_fn=roc_auc_score,
        y_title="AUC",
    )


def test_plot_metric_until_diagnosis(df):
    plot_metric_by_time_until_diagnosis(
        labels=df["label"],
        y_hat=df["pred"],
        diagnosis_timestamps=df["timestamp_t2d_diag"],
        prediction_timestamps=df["timestamp"],
        metric_fn=f1_score,
        y_title="F1",
    )


def test_plot_auc_time_from_first_visit(df):
    plot_auc_by_time_from_first_visit(
        labels=df["label"],
        y_hat_probs=df["pred_prob"],
        first_visit_timestamps=df["timestamp_first_pred_time"],
        prediction_timestamps=df["timestamp"],
    )


def test_plot_sens_by_time_to_outcome(df, tmp_path):
    positive_rate_thresholds = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    pred_proba_thresholds = positive_rate_to_pred_probs(
        pred_probs=df["pred_prob"],
        positive_rate_thresholds=positive_rate_thresholds,
    )

    plot_sensitivity_by_time_to_outcome_heatmap(  # noqa
        labels=df["label"],
        y_hat_probs=df["pred_prob"],
        outcome_timestamps=df["timestamp_t2d_diag"],
        prediction_timestamps=df["timestamp"],
        pred_proba_thresholds=pred_proba_thresholds,
        bins=[0, 30, 182, 365, 730, 1825],
        save_path=tmp_path,
    )


def test_plot_feature_importances():
    n_features = 10
    feature_name = "very long feature name right here yeah actually super long like the feature names"
    feature_names = [feature_name + str(i) for i in range(n_features)]
    # generate 10 random nubmers between 0 and 1
    feature_importance = np.random.rand(n_features)

    plot_feature_importances(
        feature_names,
        feature_importances=feature_importance,
        top_n_feature_importances=n_features,
        save_path="tmp",
    )
