"""Main feature generation."""

import logging
import sys
from pathlib import Path

from psycop.common.feature_generation.application_modules.describe_flattened_dataset import (
    save_flattened_dataset_description_to_disk,
)
from psycop.common.feature_generation.application_modules.flatten_dataset import (
    create_flattened_dataset,
)
from psycop.common.feature_generation.application_modules.loggers import (
    init_root_logger,
)
from psycop.common.feature_generation.application_modules.project_setup import (
    ProjectInfo,
    init_wandb,
)
from psycop.common.feature_generation.application_modules.save_dataset_to_disk import (
    split_and_save_dataset_to_disk,
)
from psycop.common.feature_generation.application_modules.wandb_utils import (
    wandb_alert_on_exception,
)
from psycop.common.feature_generation.loaders.raw.load_moves import (
    load_move_into_rm_for_exclusion,
)
from psycop.common.global_utils.paths import OVARTACI_SHARED_DIR
from psycop.projects.forced_admission_inpatient.feature_generation.modules.loaders.load_forced_admissions_dfs_with_prediction_times_and_outcome import (
    forced_admissions_inpatient,
)
from psycop.projects.forced_admission_inpatient.feature_generation.modules.specify_features import (
    FeatureSpecifier,
)
from psycop.projects.forced_admission_inpatient.feature_generation.modules.utils import (
    add_outcome_col,
)

log = logging.getLogger()


@wandb_alert_on_exception
def main(feature_set_name: str | None = None) -> Path:
    """Main function for loading, generating and evaluating a flattened
    dataset."""
    feature_specs = FeatureSpecifier(
        project_info=project_info,
        min_set_for_debug=True,  # Remember to set to False when generating full dataset
        limited_feature_set=False,
    ).get_feature_specs()

    flattened_df = create_flattened_dataset(
        feature_specs=feature_specs,  # type: ignore
        prediction_times_df=forced_admissions_inpatient(
            timestamps_only=True,
        ),
        drop_pred_times_with_insufficient_look_distance=False,
        project_info=project_info,
        quarantine_df=load_move_into_rm_for_exclusion(),
        quarantine_days=720,
    )

    flattened_df = add_outcome_col(
        flattened_df=flattened_df,
        visit_type="inpatient",
    )

    if feature_set_name:
        feature_set_dir = project_info.flattened_dataset_dir / feature_set_name
    else:
        feature_set_dir = project_info.flattened_dataset_dir

    if Path.exists(feature_set_dir):
        while True:
            response = input(
                f"The path '{feature_set_dir}' already exists. Do you want to potentially overwrite the contents of this folder with new feature sets? (yes/no): ",
            )

            if response.lower() not in ["yes", "y", "no", "n"]:
                print("Invalid response. Please enter 'yes/y' or 'no/n'.")
            if response.lower() in ["no", "n"]:
                print("Process stopped.")
                return feature_set_dir
            if response.lower() in ["yes", "y"]:
                print(f"Folder '{feature_set_dir}' will be overwritten.")
                break

    split_and_save_dataset_to_disk(
        flattened_df=flattened_df,
        project_info=project_info,
        feature_set_dir=feature_set_dir,
    )

    save_flattened_dataset_description_to_disk(
        project_info=project_info,
        feature_specs=feature_specs,  # type: ignore
        feature_set_dir=feature_set_dir,
    )
    return feature_set_dir


if __name__ == "__main__":
    # Run elements that are required before wandb init first,
    # then run the rest in main so you can wrap it all in
    # wandb_alert_on_exception, which will send a slack alert
    # if you have wandb alerts set up in wandb
    project_info = ProjectInfo(
        project_name="forced_admissions_inpatient",
        project_path=OVARTACI_SHARED_DIR / "forced_admissions_inpatient",
    )

    init_root_logger(project_info=project_info)

    log.info(
        f"Stdout level is {logging.getLevelName(log.level)}",
    )  # pylint: disable=logging-fstring-interpolation
    log.debug("Debugging is still captured in the log file")

    # Use wandb to keep track of your dataset generations
    # Makes it easier to find paths on wandb, as well as
    # allows monitoring and automatic slack alert on failure
    # allows monitoring and automatic slack alert on failure
    if sys.platform == "win32":
        (Path(__file__).resolve().parents[0] / "wandb" / "debug-cli.onerm").mkdir(
            exist_ok=True,
            parents=True,
        )

    init_wandb(
        project_info=project_info,
    )

    main(feature_set_name="min_dataset_for_debug")
