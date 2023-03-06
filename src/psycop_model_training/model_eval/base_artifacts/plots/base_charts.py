"""Base charts."""
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
from numpy import isin


def plot_basic_chart(
    x_values: Iterable,
    y_values: Union[Iterable[int, float], Iterable[Iterable[int, float]]],
    x_title: str,
    y_title: str,
    plot_type: Union[list[str], str],
    labels: Optional[list[str]] = None,
    sort_x: Optional[Iterable[int]] = None,
    sort_y: Optional[Iterable[int]] = None,
    flip_x_axis: bool = False,
    flip_y_axis: bool = False,
    y_limits: Optional[tuple[float, float]] = None,
    fig_size: Optional[tuple] = (5, 5),
    dpi: Optional[int] = 300,
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
        labels: (Optional[list[str]]): Optional labels to add to the plot(s).
        sort_x (Optional[Iterable[int]], optional): order of values on the x-axis. Defaults to None.
        sort_y (Optional[Iterable[int]], optional): order of values on the y-axis. Defaults to None.
        y_limits (Optional[tuple[float, float]], optional): y-axis limits. Defaults to None.
        fig_size (Optional[tuple], optional): figure size. Defaults to None.
        dpi (Optional[int], optional): dpi of figure. Defaults to 300.
        save_path (Optional[Path], optional): path to save figure. Defaults to None.
        flip_x_axis (bool, optional): Whether to flip the x axis. Defaults to False.
        flip_y_axis (bool, optional): Whether to flip the y axis. Defaults to False.

    Returns:
        Union[None, Path]: None if save_path is None, else path to saved figure
    """
    if isinstance(plot_type, str):
        plot_type = [plot_type]

    df = pd.DataFrame(
        {"x": x_values, "sort_x": sort_x, "sort_y": sort_y},
    )

    if sort_x is not None:
        df = df.sort_values(by=["sort_x"])

    if sort_y is not None:
        df = df.sort_values(by=["sort_y"])

    plt.figure(figsize=fig_size, dpi=dpi)

    if not isinstance(y_values[0], Iterable):
        y_values = [y_values]  # Make y_values an iterable

    plot_functions = {
        "bar": plt.bar,
        "hbar": plt.barh,
        "line": plt.plot,
        "scatter": plt.scatter,
    }

    # choose the first plot type as the one to use for legend
    label_plot_type = plot_type[0]

    label_plots = []
    for y_series in y_values:
        for p_type in plot_type:
            plot_function = plot_functions.get(p_type)
            plot = plot_function(df["x"], y_series)
            if p_type == label_plot_type:
                # need to one of the plot types for labelling
                label_plots.append(plot)
            if p_type == "hbar":
                plt.yticks(fontsize=7)

    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(fontsize=7)
    plt.xticks(rotation=45)

    if y_limits is not None:
        plt.ylim(y_limits)

    if flip_x_axis:
        plt.gca().invert_xaxis()
    if flip_y_axis:
        plt.gca().invert_yaxis()
    if labels is not None:
        plt.figlegend(
            [plot[0] for plot in label_plots],
            [str(label) for label in labels],
            loc="upper right",
            bbox_to_anchor=(0.9, 0.88),
            frameon=True,
        )

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path)

    plt.close()

    return save_path
