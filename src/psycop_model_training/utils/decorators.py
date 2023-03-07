"""Misc.

utility functions.
"""
import functools
import pathlib
import time
import traceback
from functools import wraps

import pandas as pd
import wandb
from wasabi import Printer


def cache_pandas_result(cache_dir: pathlib.Path, hard_reset: bool = False):
    """This decorator caches a pandas.DataFrame returning function.

    It saves the pandas.DataFrame in a parquet file in the cache_dir named a hash of its name, args and kwargs.
    It uses the following naming scheme for the caching files:
        cache_dir / function_name + '.trc.pqt'
    Parameters:
    cache_dir: a pathlib.Path object
    hard_reset: bool
    """

    def build_caching_function(func):
        @wraps(func)
        def cache_function(*args, **kwargs):
            if not isinstance(cache_dir, pathlib.Path):
                raise TypeError("cache_dir should be a pathlib.Path object")

            # Hash args to a string
            hash_str = str(hash((args, tuple(kwargs), func.__name__)))

            cache_file_path = cache_dir / (f"{hash_str}.trc.pqt")

            if not cache_dir.exists():
                print("Creating cache dir")
                cache_dir.mkdir(exist_ok=True, parents=True)

            if hard_reset or (not cache_file_path.exists()):
                result = func(*args, **kwargs)

                if not isinstance(result, pd.DataFrame):
                    raise TypeError(
                        f"The result of computing {func.__name__} is not a DataFrame",
                    )

                result.to_parquet(cache_file_path)
                return result

            result = pd.read_parquet(cache_file_path)
            return result

        return cache_function

    return build_caching_function


def print_df_dimensions_diff(func):
    """Print the difference in rows between the input and output dataframes."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        msg = Printer(timestamp=True)

        start_time = time.time()

        base_msg = f"{func.__name__}"

        arg_dfs = [arg for arg in args if isinstance(arg, pd.DataFrame)]
        kwargs_dfs = [arg for arg in kwargs.values() if isinstance(arg, pd.DataFrame)]
        potential_dfs = arg_dfs + kwargs_dfs

        if len(potential_dfs) > 1:
            raise ValueError("More than one DataFrame found in args or kwargs")

        df = potential_dfs[0]

        for dim in ("rows", "columns"):
            dim_int = 0 if dim == "rows" else 1

            n_in_dim_before_func = df.shape[dim_int]

            result = func(*args, **kwargs)

            diff = n_in_dim_before_func - result.shape[dim_int]

            diff_msg = ""
            if diff != 0:
                percent_diff = round(
                    (diff) / n_in_dim_before_func * 100,
                    2,
                )

                diff_msg += f"Dropped {diff} ({percent_diff}%) {dim}, started with {n_in_dim_before_func} {dim}. | "

        end_time = time.time()
        duration_str = f"{int(end_time - start_time)} s"

        msg.info(f"{duration_str} | {base_msg} | {diff_msg}")

        return result

    return wrapper


def wandb_alert_on_exception_return_terrible_auc(func):
    """Alerts wandb on exception."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # pylint: disable=broad-except, unused-variable
            if wandb.run is not None:
                wandb.alert(title="Run crashed", text=traceback.format_exc())
            return 0.5

    return wrapper
