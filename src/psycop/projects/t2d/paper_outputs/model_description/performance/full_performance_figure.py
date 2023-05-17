from datetime import datetime

from psycop.common.model_evaluation.patchwork.patchwork_grid import (
    create_patchwork_grid,
)
from psycop.projects.t2d.paper_outputs.config import FIGURES_PATH
from psycop.projects.t2d.paper_outputs.model_description.performance.auroc import (
    t2d_auroc_plot,
)
from psycop.projects.t2d.paper_outputs.model_description.performance.confusion_matrix_pipeline import (
    t2d_confusion_matrix_plot,
)
from psycop.projects.t2d.paper_outputs.model_description.performance.incidence_by_time_until_diagnosis import (
    t2d_first_pred_to_event,
)
from psycop.projects.t2d.paper_outputs.model_description.performance.sensitivity_by_time_to_event_pipeline import (
    t2d_sensitivity_by_time_to_event,
)
from psycop.projects.t2d.utils.best_runs import ModelRun
from wasabi import Printer

msg = Printer(timestamp=True)


def create_full_performance_figure(run: ModelRun):
    plot_fns = [
        t2d_auroc_plot,
        t2d_confusion_matrix_plot,
        t2d_sensitivity_by_time_to_event,
        t2d_first_pred_to_event,
    ]

    plots = []

    for group in plot_fns:
        for fn in plot_fns[group]:
            try:
                now = datetime.now()
                plots.append(fn(run))
                finished = datetime.now()
                msg.good(
                    f"{fn.__name__} finished in {round((finished - now).seconds, 0)} seconds",
                )
            except Exception:
                msg.fail(f"{fn.__name__} failed")
        datetime.now()

    grid = create_patchwork_grid(plots=plots, single_plot_dimensions=(7, 5), n_in_row=2)

    grid.savefig(FIGURES_PATH / "full_performance_figure.png")
