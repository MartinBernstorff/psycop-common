import polars as pl

from psycop.common.feature_generation.loaders.raw.load_visits import (
    physical_visits_to_psychiatry,
)
from psycop.projects.t2d.feature_generation.eligible_prediction_times.combined_filters import (
    filter_prediction_times_by_eligibility,
)
from psycop.projects.t2d.t2d_config import get_t2d_eligible_prediction_times_as_pandas


def get_eligible_prediction_times_as_polars() -> pl.DataFrame:
    df = pl.from_pandas(
        physical_visits_to_psychiatry(
            timestamps_only=True,
            timestamp_for_output="start",
        ),
    )

    filtered_df = filter_prediction_times_by_eligibility(
        df=df,
    ).select(["dw_ek_borger", "timestamp"])

    return filtered_df


if __name__ == "__main__":
    df = get_t2d_eligible_prediction_times_as_pandas()
