import pandas as pd

from psycop.common.feature_generation.loaders.raw.load_diagnoses import SCORE2_CVD


def get_first_cvd_indicator() -> pd.DataFrame:
    df = SCORE2_CVD()

    first_cvd = (
        df.sort_values("timestamp")
        .groupby("dw_ek_borger")
        .first()
        .reset_index(drop=False)
    )

    return first_cvd[["dw_ek_borger", "timestamp"]]


if __name__ == "__main__":
    df = get_first_cvd_indicator()

    pass
