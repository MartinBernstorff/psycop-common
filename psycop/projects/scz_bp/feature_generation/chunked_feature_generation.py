from psycop.common.feature_generation.application_modules.generate_feature_set import init_wandb_and_generate_feature_set
from psycop.common.feature_generation.application_modules.project_setup import ProjectInfo


import pandas as pd
import polars as pl
from timeseriesflattener.feature_specs.single_specs import AnySpec


from pathlib import Path
from typing import Iterable, Literal


class ChunkedFeatureGenerator:
    @staticmethod
    def generate_feature_set(
        project_info: ProjectInfo,
        eligible_prediction_times: pd.DataFrame,
        feature_specs: list[AnySpec],
        chunksize: int = 500,
    ) -> None:
        """Generate features in chunks to avoid memory issues with multiprocessing"""
        print(f"Generation features in chunks of {chunksize}")
        for i in range(0, len(feature_specs), chunksize):
            print(f"Generating features for chunk {i} to {i+chunksize}")
            init_wandb_and_generate_feature_set(
                project_info=project_info,
                eligible_prediction_times=eligible_prediction_times,
                feature_specs=feature_specs[i : i + chunksize],
            )
            ChunkedFeatureGenerator.move_contents_of_dir_to_dir(
                source_dir=project_info.project_path / "flattened_datasets",
                target_dir=project_info.project_path / f"flattened_datasets_chunk_{i}",
            )
        print("Feature generation done. Merging feature sets...")
        ChunkedFeatureGenerator.merge_feature_sets_from_dirs(
            source_dirs=project_info.project_path.glob("flattened_datasets_chunk_*"),
            target_dir=project_info.project_path / "flattened_datasets",
            splits=["train", "val", "test"],
        )

    @staticmethod
    def move_contents_of_dir_to_dir(
        source_dir: Path,
        target_dir: Path,
    ) -> None:
        """Move all files and folders from source_dir to target_dir using pathlib"""
        target_dir.mkdir(exist_ok=True, parents=True)
        for file in source_dir.iterdir():
            file.rename(target_dir / file.name)

    # test whether the concatenations are correct
    # against a join. Infer exclude cols
    @staticmethod
    def merge_feature_sets_from_dirs(
        source_dirs: Iterable[Path],
        target_dir: Path,
        splits: list[Literal["train", "val", "test"]] = ["train", "val", "test"],
    ) -> None:
        """Merge all feature sets from source_dirs into target_dir"""
        target_dir.mkdir(exist_ok=True, parents=True)
        for split in splits:
            dfs = ChunkedFeatureGenerator._read_split_dataframes_from_dir(
                source_dirs=source_dirs, split=split
            )
            shared_cols = ChunkedFeatureGenerator._find_shared_cols(dfs=dfs)
            # dataframes are sorted so can safely concat
            # need to remove duplicate columns
            dfs = ChunkedFeatureGenerator._remove_shared_cols_from_all_but_one_df(
                dfs=dfs, shared_cols=shared_cols
            )
            split_df = pl.concat(dfs, how="horizontal")
            split_df.write_parquet(target_dir / f"{split}.parquet")

    @staticmethod
    def _remove_shared_cols_from_all_but_one_df(
        dfs: list[pl.DataFrame],
        shared_cols: list[str],
    ) -> list[pl.DataFrame]:
        return [
            df.select(pl.exclude(shared_cols)) for i, df in enumerate(dfs) if i != 0
        ]

    @staticmethod
    def _read_split_dataframes_from_dir(
        source_dirs: Iterable[Path], split: Literal["train", "val", "test"]
    ) -> list[pl.DataFrame]:
        return [
            pl.read_parquet(source_dir / f"{split}.parquet")
            for source_dir in source_dirs
        ]

    @staticmethod
    def _find_shared_cols(
        dfs: list[pl.DataFrame],
    ) -> list[str]:
        """Find columns that are present in all dataframes in dfs. Only checks the
        first two dataframes in dfs"""
        cols = set(dfs[0].columns).intersection(dfs[1].columns)
        return list(cols)