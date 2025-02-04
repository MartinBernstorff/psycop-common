from dataclasses import dataclass
from datetime import datetime

import plotnine as pn

from psycop.projects.scz_bp.evaluation.pipeline_objects import RunGroup

########################################
# UPDATE THESE TO SELECT MODEL OUTPUTS #
########################################
DEV_GROUP_NAME = "tfidf-500-aktuelt-psykisk"
DEVELOPMENT_GROUP = RunGroup(name=DEV_GROUP_NAME, project_name="scz_bp")
BEST_POS_RATE = 0.03

EVAL_GROUP_NAME = f"{DEV_GROUP_NAME}-eval-on-test"
EVAL_GROUP = RunGroup(name=EVAL_GROUP_NAME, project_name="scz_bp")

SCZ_BP_CUSTOM_COLUMNS = ["meta_scz_or_bp_indicator"]  # , "meta_first_visit"]


################
# OUTPUT PATHS #
################
date_str = datetime.now().strftime("%Y-%m-%d")

T2D_PN_THEME = pn.theme_bw() + pn.theme(
    panel_grid=pn.element_blank(),
    axis_title=pn.element_text(size=14),
)


@dataclass
class Colors:
    primary = "#0072B2"
    secondary = "#009E73"
    tertiary = "#D55E00"
    background = "lightgray"


COLORS = Colors()
