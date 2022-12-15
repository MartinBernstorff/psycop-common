import pandas as pd

from psycop_feature_generation.application_modules.filter_prediction_times import (
    PredictionTimeFilterer,
)
from psycop_feature_generation.utils_for_testing import str_to_df


def test_filter_by_quarantine_date():
    """Test filtering by quarantine date.

    Should filter if the prediction times is within X days after the quarantine date.

    Uses dataframes as input.
    """
    quarantine_df = str_to_df(
        """entity_id,timestamp,
        1,2021-01-01 00:00:01,
        1,2022-01-01 00:00:01,
        """,
    )

    prediction_time_df = str_to_df(
        """entity_id,timestamp,
        1,2020-12-01 00:00:01, # keep: before quarantine date 
        1,2022-12-01 00:00:01, # drop: after quarantine date
        1,2026-02-01 00:00:01, # keep: outside quarantine days
        2,2023-02-01 00:00:01, # keep: no quarantine date for this id
        """,
        add_pred_time_uuid=True,
    )

    expected_df = str_to_df(
        """entity_id,timestamp,
        1,2020-12-01 00:00:01,
        1,2026-02-01 00:00:01,
        2,2023-02-01 00:00:01,
        """,
        add_pred_time_uuid=True,
    )

    filterer = PredictionTimeFilterer(
        prediction_time_df=prediction_time_df,
        quarantine_df=quarantine_df,
        quarantine_days=730,
        id_col_name="entity_id",
    )

    result_df = filterer.filter()

    # Check that the result is as expected using pandas.testing.assert_frame_equal
    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        expected_df.reset_index(drop=True),
    )
