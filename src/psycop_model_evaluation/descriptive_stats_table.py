"""Code for generating a descriptive stats table."""
import typing as t
from typing import Literal, Optional, Union

import numpy as np
import pandas as pd

from psycop_model_evaluation.utils import (
    BaseModel,
    bin_continuous_data,
)


class VariableSpec(BaseModel):
    _name: str = "Base"
    row_title: str  # Title for the created row in the table
    row_df_col_name: str  # Source column name in the dataset df
    n_decimals: Union[int, None] = 2  # Number of decimals to round the results to


class BinaryVariableSpec(VariableSpec):
    _name: str = "Binary"
    positive_class: Union[
        float, str
    ]  # Value of the class to generate results for (e.g. 1 for a binary variable)


class CategoricalVariableSpec(VariableSpec):
    _name: str = "Categorical"
    categories: Optional[list[str]] = None  # List of categories to include in the table


class ContinuousVariableSpec(VariableSpec):
    _name: str = "Continuous"
    aggregation_measure: t.Literal["mean"] = "mean"
    variance_measure: t.Literal["std"] = "std"


class ContinuousVariableToCategorical(VariableSpec):
    _name: str = "ContinuousToCategorical"
    bins: list[float]  # List of bin edges
    bin_decimals: Optional[int] = None  # Number of decimals to round the bin edges to


class VariableGroupSpec(BaseModel):
    title: str  # Title to add to the table
    group_column_name: Optional[str]  # Column name to group by
    add_total_row: bool = True  # Whether to add a total row, e.g. "100_000 patients"
    row_specs: list[
        Union[VariableSpec, t.Literal["Total"]]
    ]  # List of row specs to include in the table


class DatasetSpec(BaseModel):
    name: str  # Name of the dataset, used as a column name in the table
    df: pd.DataFrame


class GroupedDatasetSpec(BaseModel):
    name: str  # Name of the dataset, used as a column name in the table
    grouped_df: pd.DataFrame


def _create_row_df(
    row_title: str,
    col_title: str,
    cell_value: Union[float, str],
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Title": row_title,
            col_title: cell_value,
        },
        index=[0],
    )


def _get_col_value_for_total_row(
    dataset: GroupedDatasetSpec,
    variable_group_spec: Optional[VariableGroupSpec] = None,
) -> pd.DataFrame:
    if variable_group_spec is None:
        cell_value = dataset.grouped_df.shape[0]
        variable_title = ""
    else:
        cell_value = (
            dataset.grouped_df[variable_group_spec.group_column_name].nunique()
            if (variable_group_spec.group_column_name is not None)
            else dataset.grouped_df.shape[0]
        )
        variable_title = variable_group_spec.title.lower()

    return _create_row_df(
        row_title=f"Total {variable_title}",
        col_title=dataset.name,
        cell_value=cell_value,
    )


def _get_col_value_for_binary_row(
    dataset: GroupedDatasetSpec,
    row_spec: BinaryVariableSpec,
) -> pd.DataFrame:
    # Get proportion with the positive class
    positive_class_prop = (
        dataset.grouped_df[row_spec.row_df_col_name] == row_spec.positive_class
    ).mean()
    prop_rounded = round(positive_class_prop * 100, row_spec.n_decimals)

    return _create_row_df(
        row_title=row_spec.row_title,
        col_title=dataset.name,
        cell_value=f"{prop_rounded}%",
    )


def _get_col_value_for_continuous_row(
    dataset: GroupedDatasetSpec,
    row_spec: ContinuousVariableSpec,
) -> pd.DataFrame:
    # Aggregation
    agg_results = {
        "mean": dataset.grouped_df[row_spec.row_df_col_name].mean(),
        "median": dataset.grouped_df[row_spec.row_df_col_name].median(),
    }
    agg_result = agg_results[row_spec.aggregation_measure]
    agg_rounded = round(agg_result, row_spec.n_decimals)
    agg_cell_string = f"{agg_rounded}"

    # Variance
    variance_results = {
        "std": dataset.grouped_df[row_spec.row_df_col_name].std(),
        "iqr": dataset.grouped_df[row_spec.row_df_col_name].quantile(0.75)
        - dataset.grouped_df[row_spec.row_df_col_name].quantile(0.25),
    }
    variance_rounded = round(
        variance_results[row_spec.variance_measure],
        row_spec.n_decimals,
    )

    # Variance title
    variance_title_strings = {"std": "± SD", "iqr": "[IQR]"}
    variance_title_string = variance_title_strings[row_spec.variance_measure]

    # Variance cell
    variance_cell_strings = {
        "std": f"± {variance_rounded}",
        "iqr": f"[{agg_result - variance_rounded}, {agg_result + variance_rounded}]",
    }
    variance_cell_string = variance_cell_strings[row_spec.variance_measure]

    return _create_row_df(
        row_title=f"{row_spec.row_title} ({row_spec.aggregation_measure} {variance_title_string})",
        col_title=dataset.name,
        cell_value=f"{agg_cell_string} {variance_cell_string}",
    )


def _get_col_value_for_categorical_row():
    pass


def _get_col_value_transform_continous_to_categorical(
    dataset: GroupedDatasetSpec,
    row_spec: ContinuousVariableToCategorical,
) -> pd.DataFrame:
    values = bin_continuous_data(
        series=dataset.grouped_df[row_spec.row_df_col_name],
        bins=row_spec.bins,
        bin_decimals=row_spec.bin_decimals,
    )

    result_df = pd.DataFrame({"Title": values[0], "n_in_category": values[1]})

    # Get col percentage for each category within group
    grouped_df = result_df.groupby("Title").mean()
    grouped_df = grouped_df.reset_index()

    grouped_df[dataset.name] = (
        grouped_df["n_in_category"] / grouped_df["n_in_category"].sum() * 100
    )

    if row_spec.n_decimals is not None:
        grouped_df[dataset.name] = round(
            grouped_df[dataset.name],
            row_spec.n_decimals,
        )
    else:
        grouped_df[dataset.name] = grouped_df[dataset.name].astype(int)

    # Add a % symbol
    grouped_df[dataset.name] = grouped_df[dataset.name].astype(str) + "%"

    # Add "Age", "" as first row
    grouped_df = pd.concat(
        [
            pd.DataFrame(
                {"Title": row_spec.row_title, dataset.name: np.nan},
                index=[0],
            ),
            grouped_df,
        ],
    )

    return grouped_df[["Title", dataset.name]]


def _process_row(
    row_spec: Union[VariableSpec, Literal["Total"]],
    dataset: DatasetSpec,
    group_col_name: Union[str, None],
) -> pd.DataFrame:
    spec_to_func = {
        "Binary": _get_col_value_for_binary_row,
        "Continuous": _get_col_value_for_continuous_row,
        "ContinuousToCategorical": _get_col_value_transform_continous_to_categorical,
        "Total": _get_col_value_for_total_row,
    }

    if group_col_name is not None:
        agg_df = dataset.df.groupby(group_col_name).agg(np.mean)
        grouped_dataset_spec = GroupedDatasetSpec(name=dataset.name, grouped_df=agg_df)
    else:
        grouped_dataset_spec = GroupedDatasetSpec(
            name=dataset.name,
            grouped_df=dataset.df,
        )

    if row_spec == "Total":
        return _get_col_value_for_total_row(
            dataset=grouped_dataset_spec,
        )

    return spec_to_func[row_spec._name](  # type: ignore
        dataset=grouped_dataset_spec,
        row_spec=row_spec,
    )


def _process_group(
    group_spec: VariableGroupSpec,
    datasets: t.Sequence[DatasetSpec],
) -> pd.DataFrame:
    rows = []

    if group_spec.add_total_row:
        # Add total to the front of the row specs
        group_spec.row_specs.insert(
            0,
            "Total",
        )

    for row_spec in group_spec.row_specs:
        dataset_row_vals = []

        for dataset in datasets:
            dataset_row_vals.append(
                _process_row(
                    row_spec=row_spec,
                    dataset=dataset,
                    group_col_name=group_spec.group_column_name,
                ),
            )

        row: pd.DataFrame = dataset_row_vals[0]

        for col_df in dataset_row_vals[1:]:
            row = row.merge(col_df, on="Title", how="outer")

        rows.append(row)

    group_header = pd.DataFrame(
        {datasets[0].name: [f"[{group_spec.title}]"]},
        columns=["Title"] + [dataset.name for dataset in datasets],
    )

    return pd.concat([group_header, *rows])


def create_descriptive_stats_table(
    variable_group_specs: t.Sequence[VariableGroupSpec],
    datasets: t.Sequence[DatasetSpec],
) -> pd.DataFrame:
    groups = []

    for group_spec in variable_group_specs:
        groups.append(_process_group(group_spec=group_spec, datasets=datasets))

    all_groups = pd.concat(groups)

    # Replace NaN with " "
    return all_groups.fillna(" ")
