"""Utilites for testing."""

from io import StringIO

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame

from psycop_feature_generation.loaders.synth.raw.load_synth_data import (
    load_synth_outcome,
    load_synth_prediction_times,
)
from psycop_feature_generation.utils import data_loaders


def convert_cols_with_matching_colnames_to_datetime(
    df: DataFrame,
    colname_substr: str,
) -> DataFrame:
    """Convert columns that contain colname_substr in their name to datetimes
    Args:
        df (DataFrame): The df to convert. # noqa: DAR101
        colname_substr (str): Substring to match on. # noqa: DAR101

    Returns:
        DataFrame: The converted df
    """
    df.loc[:, df.columns.str.contains(colname_substr)] = df.loc[
        :,
        df.columns.str.contains(colname_substr),
    ].apply(pd.to_datetime)

    return df


def str_to_df(
    string: str,
    convert_timestamp_to_datetime: bool = True,
    convert_np_nan_to_nan: bool = True,
    convert_str_to_float: bool = False,
    add_pred_time_uuid: bool = False,
    entity_id_colname: str = "entity_id",
) -> DataFrame:
    """Convert a string representation of a dataframe to a dataframe.

    Args:
        string (str): A string representation of a dataframe.
        convert_timestamp_to_datetime (bool): Whether to convert the timestamp column to datetime. Defaults to True.
        convert_np_nan_to_nan (bool): Whether to convert np.nan to np.nan. Defaults to True.
        convert_str_to_float (bool): Whether to convert strings to floats. Defaults to False.

    Returns:
        DataFrame: A dataframe.
    """
    # Drop anything after the last comma
    string = string[: string.rfind(",") + 1]

    df = pd.read_table(StringIO(string), sep=",", index_col=False)

    if convert_timestamp_to_datetime:
        df = convert_cols_with_matching_colnames_to_datetime(df, "timestamp")

    if convert_np_nan_to_nan:
        # Convert "np.nan" str to the actual np.nan
        df = df.replace("np.nan", np.nan)

    if convert_str_to_float:
        # Convert all str to float
        df = df.apply(pd.to_numeric, axis=0, errors="coerce")

    if add_pred_time_uuid:
        df["pred_time_uuid"] = (
            df[entity_id_colname].astype(str) + "_" + df["timestamp"].astype(str)
        )

    # Drop "Unnamed" cols
    return df.loc[:, ~df.columns.str.contains("^Unnamed")]


@data_loaders.register("load_event_times")
def load_event_times():
    """Load event times."""
    event_times_str = """dw_ek_borger,timestamp,value,
                    1,2021-12-30 00:00:01, 1
                    1,2021-12-29 00:00:02, 2
                    """

    return str_to_df(event_times_str)


def check_any_item_in_list_has_str(list_of_str: list, str_: str):
    """Check if any item in a list contains a string.

    Args:
        list_of_str (list): A list of strings.
        str_ (str): A string.

    Returns:
        bool: True if any item in the list contains the string.
    """
    return any(str_ in item for item in list_of_str)


@pytest.fixture(scope="function")
def synth_prediction_times():
    """Load the prediction times."""
    return load_synth_prediction_times()


@pytest.fixture(scope="function")
def synth_outcome():
    """Load the synth outcome times."""
    return load_synth_outcome()
