"""Higher-level module that handles spawning trainer processes using
trian_model.py."""
import subprocess
import time
from pathlib import Path
from typing import Optional, Union

from wasabi import Printer

from psycop.common.model_training.application_modules.get_search_space import (
    TrainerSpec,
)
from psycop.common.model_training.config_schemas.full_config import FullConfigSchema


def start_trainer(
    cfg: FullConfigSchema,
    config_file_name: str,
    lookahead_days: int,
    wandb_group_override: str,
    model_name: str,
    dataset_dir: Optional[Union[Path, list[Path], list[str]]] = None,
    train_single_model_file_path: Optional[Path] = None,
) -> subprocess.Popen:  # type: ignore
    """Start a trainer."""
    msg = Printer(timestamp=True)

    if cfg.train is None:
        raise ValueError("cfg.train is None, but is required for training in parallel.")

    if train_single_model_file_path is None:
        train_single_model_file_path = Path(
            "application/train_model_from_application_module.py",
        )

    subprocess_args: list[str] = [
        "python",
        str(train_single_model_file_path),
        f"project.wandb.group='{wandb_group_override}'",
        f"project.wandb.mode={cfg.project.wandb.mode}",
        f"hydra.sweeper.n_trials={cfg.train.n_trials_per_lookahead}",
        f"hydra.sweeper.n_jobs={cfg.train.n_jobs_per_trainer}",
        f"model={model_name}",
        f"preprocessing.pre_split.min_lookahead_days={lookahead_days}",
        "--config-name",
        f"{config_file_name}",
    ]

    # We have to insert to avoid coming after the config name or before the python executable in the args list
    if cfg.train.n_trials_per_lookahead > 1:
        subprocess_args.insert(2, "--multirun")

    if model_name == "xgboost":
        subprocess_args.insert(3, "++model.args.tree_method='gpu_hist'")

    if dataset_dir is not None:
        if isinstance(dataset_dir, list):
            dataset_dir = [str(d) for d in dataset_dir]

        subprocess_args.insert(4, f"data.dir={dataset_dir}")

    msg.info(f'{" ".join(subprocess_args)}')

    return subprocess.Popen(
        args=subprocess_args,
    )


def spawn_trainers(
    cfg: FullConfigSchema,
    config_file_name: str,
    wandb_prefix: str,
    trainer_specs: list[TrainerSpec],
    train_single_model_file_path: Path,
):
    """Train a model for each cell in the grid of possible look distances."""
    active_trainers: list[subprocess.Popen] = []  # type: ignore
    trainer_combinations_queue = trainer_specs.copy()
    trainer_combinations_queue = trainer_specs.copy()

    if cfg.train is None:
        raise ValueError("cfg.train is None, but is required for training in parallel.")

    while trainer_combinations_queue or active_trainers:
        # Wait until there is a free slot in the trainers group
        if (
            len(active_trainers) >= cfg.train.n_active_trainers
            or len(trainer_combinations_queue) == 0
        ):
            # Drop trainers if they have finished
            # If finished, t.poll() is not None
            active_trainers = [t for t in active_trainers if t.poll() is None]
            time.sleep(1)
            continue

        # Start a new trainer
        trainer_spec = trainer_combinations_queue.pop()

        msg = Printer(timestamp=True)
        msg.info(
            f"Spawning a new trainer with lookahead={trainer_spec.lookahead_days} days",
        )
        wandb_group = f"{wandb_prefix}"

        active_trainers.append(
            start_trainer(
                cfg=cfg,
                config_file_name=config_file_name,
                lookahead_days=trainer_spec.lookahead_days,
                wandb_group_override=wandb_group,
                model_name=trainer_spec.model_name,
                dataset_dir=cfg.data.dir,
                train_single_model_file_path=train_single_model_file_path,
            ),
        )

        # Sleep a bit to avoid segfaults
        time.sleep(10)
