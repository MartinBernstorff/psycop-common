"""Loaders for visits to psychiatry."""

import logging
from typing import Literal, Optional

import pandas as pd
from timeseriesflattener.feature_spec_objects import BaseModel

from psycop_feature_generation.loaders.raw.sql_load import sql_load
from psycop_feature_generation.utils import data_loaders

log = logging.getLogger(__name__)


class RawValueSourceSchema(BaseModel):
    """A class for structuring raw values from source schemas.

    Fields:
        view (str): The name of the view for the schema.
        datetime_col (str): The name of the datetime column in the view. This should be defined as the end time of the visit, in order to prevent data leakage.
        value_col (Optional[str]): The name of the column used to calculate the value for the loader. To calculate length of visit, this needs to be the name of the column indicating the starting time of the visit. Defaults to None.
        location_col (Optional[str]): The name of the column indicating which shak unit was responsible for the visit (e.g. 6600). Defaults to None.
        where (str): A where clause that defines additional subsetting for views.
    """

    view: str
    end_datetime_col_name: str
    start_datetime_col_name: Optional[str] = None
    location_col_name: Optional[str] = None
    where_clause: str


def physical_visits(
    timestamp_for_output: Literal["start", "end"] = "end",
    shak_code: Optional[int] = None,
    shak_sql_operator: Optional[str] = "=",
    where_clause: Optional[str] = None,
    where_separator: Optional[str] = "AND",
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
    visit_types: list[
        Literal["admissions", "ambulatory_visits", "emergency_visits"]
    ] = ["admissions", "ambulatory_visits", "emergency_visits"],
) -> pd.DataFrame:
    """Load pshysical visits to both somatic and psychiatry.

    Args:
        timestamp_for_output (Literal["start", "end"], optional): Whether to use the start or end timestamp for the output. Defaults to "end".
        shak_code (Optional[int], optional): SHAK code indicating where to keep/not keep visits from (e.g. 6600). Combines with
            shak_sql_operator, e.g. "!= 6600". Defaults to None, in which case all admissions are kept.
        shak_sql_operator (Optional[str], optional): Operator to use with shak_code. Defaults to "=".
        where_clause (Optional[str], optional): Extra where-clauses to add to the SQL call. E.g. dw_ek_borger = 1. Defaults to None. # noqa: DAR102
        where_separator (Optional[str], optional): Separator between where-clauses. Defaults to "AND".
        n_rows (Optional[int], optional): Number of rows to return. Defaults to None.
        return_value_as_visit_length_days (Optional[bool], optional): Whether to return length of visit in days as the value for the loader. Defaults to False which results in value=1 for all visits.
        visit_types (list[Literal["admissions", "ambulatory_visits", "emergency_visits"]]]): Which visit types to load. Defaults to ["admissions", "ambulatory_visits", "emergency_visits"].

    Returns:
        pd.DataFrame: Dataframe with all physical visits to psychiatry. Has columns dw_ek_borger and timestamp.
    """

    # SHAK = 6600 ≈ in psychiatry

    source_schemas = {
        "LPR3": RawValueSourceSchema(
            view="[FOR_LPR3kontakter_psyk_somatik_inkl_2021_feb2022]",
            start_datetime_col_name="datotid_lpr3kontaktstart",
            end_datetime_col_name="datotid_lpr3kontaktslut",
            location_col_name="shakkode_lpr3kontaktansvarlig",
            where_clause="AND [Kontakttype] = 'Fysisk fremmøde'",
        ),
        "ambulatory_visits": RawValueSourceSchema(
            view="[FOR_besoeg_psyk_somatik_LPR2_inkl_2021_feb2022]",
            start_datetime_col_name="datotid_start",
            end_datetime_col_name="datotid_slut",
            location_col_name="shakafskode",
            where_clause="AND ambbesoeg = 1",
        ),
        "emergency_visits": RawValueSourceSchema(
            view="[FOR_akutambulantekontakter_psyk_somatik_LPR2_inkl_2021_feb2022]",
            start_datetime_col_name="datotid_start",
            end_datetime_col_name="datotid_slut",
            location_col_name="afsnit_stam",
            where_clause="",
        ),
        "admissions": RawValueSourceSchema(
            view="[FOR_indlaeggelser_psyk_somatik_LPR2_inkl_2021_feb2022]",
            start_datetime_col_name="datotid_indlaeggelse",
            end_datetime_col_name="datotid_udskrivning",
            location_col_name="shakKode_kontaktansvarlig",
            where_clause="",
        ),
    }

    allowed_visit_types = ["admissions", "ambulatory_visits", "emergency_visits"]

    if any(types not in allowed_visit_types for types in visit_types):
        raise ValueError(
            f"Invalid visit type. Allowed types of visits are {allowed_visit_types}.",
        )

    english_to_lpr3_visit_type = {  # pylint: disable=invalid-name
        "admissions": "'Indlæggelse'",
        "ambulatory_visits": "'Ambulant'",
        "emergency_visits": "'Akut ambulant'",
    }
    chosen_schemas = {
        visit_type: source_schemas[visit_type] for visit_type in visit_types + ["LPR3"]
    }
    english_to_lpr3_visit_type = [
        english_to_lpr3_visit_type[visit] for visit in visit_types
    ]
    chosen_schemas[
        "LPR3"
    ].where_clause += f" AND pt_type IN ({','.join(english_to_lpr3_visit_type)})"

    dfs = []

    for schema in chosen_schemas.values():
        cols = f"{schema.start_datetime_col_name}, {schema.end_datetime_col_name}, dw_ek_borger"

        sql = f"SELECT {cols} FROM [fct].{schema.view} WHERE {schema.start_datetime_col_name} IS NOT NULL {schema.where_clause}"

        if shak_code is not None:
            sql += f" AND {schema.location_col_name} != 'Ukendt'"
            sql += f" AND left({schema.location_col_name}, {len(str(shak_code))}) {shak_sql_operator} {str(shak_code)}"

        if where_clause is not None:
            sql += f" {where_separator} {where_clause}"

        df = sql_load(sql, database="USR_PS_FORSK", chunksize=None, n_rows=n_rows)
        df.rename(
            columns={
                schema.end_datetime_col_name: "timestamp_end",
                schema.start_datetime_col_name: "timestamp_start",
            },
            inplace=True,
        )

        dfs.append(df)

    # Concat the list of dfs
    output_df = pd.concat(dfs)

    # 0,8% of visits are duplicates. Unsure if overlap between sources or errors in source data. Removing.
    output_df = output_df.drop_duplicates(
        subset=["timestamp_start", "timestamp_end", "dw_ek_borger"],
        keep="first",
    )

    # Change value column to length of admission in days
    if return_value_as_visit_length_days:
        output_df["value"] = (
            output_df["timestamp_end"] - pd.to_datetime(output_df["timestamp_start"])
        ).dt.total_seconds() / 86400
    else:
        output_df["value"] = 1

    log.info("Loaded physical visits")

    output_df.rename(
        columns={f"timestamp_{timestamp_for_output}": "timestamp"}, inplace=True
    )

    # Keep only one visit per timestamp
    output_df = output_df.drop_duplicates(
        subset=["dw_ek_borger", "timestamp"], keep="first"
    )

    return output_df[["dw_ek_borger", f"timestamp", "value"]].reset_index(drop=True)


@data_loaders.register("physical_visits")
def physical_visits_loader(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
) -> pd.DataFrame:
    """Load physical visits to all units."""
    return physical_visits(
        n_rows=n_rows,
        return_value_as_visit_length_days=return_value_as_visit_length_days,
    )


@data_loaders.register("physical_visits_to_psychiatry")
def physical_visits_to_psychiatry(
    n_rows: Optional[int] = None,
    timestamps_only: bool = False,
    return_value_as_visit_length_days: Optional[bool] = True,
    timestamp_for_output: Literal["start", "end"] = "start",
) -> pd.DataFrame:
    """Load physical visits to psychiatry."""
    df = physical_visits(
        shak_code=6600,
        shak_sql_operator="=",
        n_rows=n_rows,
        return_value_as_visit_length_days=return_value_as_visit_length_days,
        timestamp_for_output=timestamp_for_output,
    )

    if timestamps_only:
        df.drop(columns=["value"], inplace=True)

    return df


@data_loaders.register("physical_visits_to_somatic")
def physical_visits_to_somatic(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
) -> pd.DataFrame:
    """Load physical visits to somatic."""
    return physical_visits(
        shak_code=6600,
        shak_sql_operator="!=",
        n_rows=n_rows,
        return_value_as_visit_length_days=return_value_as_visit_length_days,
    )


@data_loaders.register("admissions")
def admissions(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
    shak_code: Optional[int] = None,
    shak_sql_operator: Optional[str] = None,
) -> pd.DataFrame:
    """Load admissions."""
    return physical_visits(
        visit_types=["admissions"],
        return_value_as_visit_length_days=return_value_as_visit_length_days,
        n_rows=n_rows,
        shak_code=shak_code,
        shak_sql_operator=shak_sql_operator,
    )


@data_loaders.register("ambulatory_visits")
def ambulatory_visits(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
    shak_code: Optional[int] = None,
    shak_sql_operator: Optional[str] = None,
) -> pd.DataFrame:
    """Load ambulatory visits."""
    return physical_visits(
        visit_types=["ambulatory_visits"],
        return_value_as_visit_length_days=return_value_as_visit_length_days,
        n_rows=n_rows,
        shak_code=shak_code,
        shak_sql_operator=shak_sql_operator,
    )


@data_loaders.register("emergency_visits")
def emergency_visits(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
    shak_code: Optional[int] = None,
    shak_sql_operator: Optional[str] = None,
) -> pd.DataFrame:
    """Load emergency visits."""
    return physical_visits(
        visit_types=["emergency_visits"],
        return_value_as_visit_length_days=return_value_as_visit_length_days,
        n_rows=n_rows,
        shak_code=shak_code,
        shak_sql_operator=shak_sql_operator,
    )


@data_loaders.register("ambulatory_and_emergency_visits")
def ambulatory_and_emergency_visits(
    n_rows: Optional[int] = None,
    return_value_as_visit_length_days: Optional[bool] = False,
    shak_code: Optional[int] = None,
    shak_sql_operator: Optional[str] = None,
) -> pd.DataFrame:
    """Load emergency visits."""
    return physical_visits(
        visit_types=["ambulatory_visits", "emergency_visits"],
        return_value_as_visit_length_days=return_value_as_visit_length_days,
        n_rows=n_rows,
        shak_code=shak_code,
        shak_sql_operator=shak_sql_operator,
    )
