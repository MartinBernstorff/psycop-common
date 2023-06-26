import pandas as pd

from psycop.common.feature_generation.loaders.raw.load_scz_bp_outcomes import (
    manic_and_bipolar,
)


def get_first_bp_diagnosis() -> pd.DataFrame:
    df = manic_and_bipolar()

    df_first_bp_diagnosis = (
        df.sort_values("timestamp")
        .groupby("dw_ek_borger")
        .first()
        .reset_index(drop=False)
    )
    return df_first_bp_diagnosis


if __name__ == "__main__":
    df = get_first_bp_diagnosis()
    pass
