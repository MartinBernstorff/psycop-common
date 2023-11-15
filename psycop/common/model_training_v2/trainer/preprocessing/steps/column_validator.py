from dataclasses import dataclass

import polars as pl
from polars import LazyFrame

from psycop.common.model_training_v2.config.baseline_registry import BaselineRegistry
from psycop.common.model_training_v2.trainer.preprocessing.step import (
    PolarsFrame_T0,
    PresplitStep,
)


@dataclass(frozen=True)
class MissingColumnError(Exception):
    column_name: str


@BaselineRegistry.preprocessing.register("column_exists_validator")
class ColumnExistsValidator(PresplitStep):
    def __init__(
        self,
        *args: str,
    ):
        self.column_names = args

    def apply(self, input_df: PolarsFrame_T0) -> PolarsFrame_T0:
        df = input_df.fetch(1) if isinstance(input_df, LazyFrame) else input_df

        errors: list[MissingColumnError] = [
            self._column_name_exists(column_name=column, df=df)
            for column in self.column_names
            if self._column_name_exists(column_name=column, df=df) is not None
        ] # type: ignore

        if errors:
            missing_columns_str = ", ".join([e.column_name for e in errors])
            raise MissingColumnError(
                f"Column(s) [{missing_columns_str}] not found in dataset.",
            )

        return input_df

    def _column_name_exists(
        self,
        column_name: str,
        df: pl.DataFrame,
    ) -> MissingColumnError | None:
        if column_name not in df.columns:
            return MissingColumnError(column_name=column_name)

        return None
