import pandas as pd

from psycop.common.feature_generation.loaders.raw.load_scz_bp_outcomes import (
    scz_and_sczaffective,
)


def get_first_scz_diagnosis() -> pd.DataFrame:
    df = scz_and_sczaffective()

    df_first_scz_diagnosis = (
        df.sort_values("timestamp")
        .groupby("dw_ek_borger")
        .first()
        .reset_index(drop=False)
    )
    return df_first_scz_diagnosis
