"""Base charts."""
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd


def plot_basic_chart(
    x_values: Iterable,
    y_values: Iterable,
    x_title: str,
    y_title: str,
    plot_type: Optional[Union[list[str], str]],
    sort_x: Optional[Iterable[int]] = None,
    sort_y: Optional[Iterable[int]] = None,
    fig_size: Optional[tuple] = (10, 10),
    save_path: Optional[Path] = None,
) -> Union[None, Path]:
    """Plot a simple chart using matplotlib. Options for sorting the x and y
    axis are available.

    Args:
        x_values (Iterable): The x values of the bar chart.
        y_values (Iterable): The y values of the bar chart.
        x_title (str): title of x axis
        y_title (str): title of y axis
        plot_type (Optional[Union[List[str], str]], optional): type of plots.
            Options are combinations of ["bar", "hbar", "line", "scatter"] Defaults to "bar".
        sort_x (Optional[Iterable[int]], optional): order of values on the x-axis. Defaults to None.
        sort_y (Optional[Iterable[int]], optional): order of values on the y-axis. Defaults to None.
        fig_size (Optional[tuple], optional): figure size. Defaults to None.
        save_path (Optional[Path], optional): path to save figure. Defaults to None.

    Returns:
        Union[None, Path]: None if save_path is None, else path to saved figure
    """
    if isinstance(plot_type, str):
        plot_type = [plot_type]

    df = pd.DataFrame(
        {"x": x_values, "y": y_values, "sort_x": sort_x, "sort_y": sort_y},
    )

    if sort_x is not None:
        df = df.sort_values(by=["sort_x"])

    if sort_y is not None:
        df = df.sort_values(by=["sort_y"])

    plt.figure(figsize=fig_size)
    if "bar" in plot_type:
        plt.bar(df["x"], df["y"])
    if "hbar" in plot_type:
        plt.barh(df["x"], df["y"])
    if "line" in plot_type:
        plt.plot(df["x"], df["y"])
    if "scatter" in plot_type:
        plt.scatter(df["x"], df["y"])

    plt.xlabel(x_title)
    plt.ylabel(y_title)

    if save_path is not None:
        plt.savefig(save_path)

    plt.close()
    return save_path
