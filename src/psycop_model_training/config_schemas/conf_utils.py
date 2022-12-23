"""Utilities for handling config objects, e.g. load, change format.

Very useful when testing.
"""
from typing import Optional, Union

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

from psycop_model_training.config_schemas.basemodel import BaseModel
from psycop_model_training.config_schemas.full_config import FullConfigSchema


def convert_omegaconf_to_pydantic_object(
    conf: DictConfig,
    allow_mutation: bool = False,
) -> FullConfigSchema:
    """Converts an omegaconf DictConfig to a pydantic object.

    Args:
        conf (DictConfig): Omegaconf DictConfig
        allow_mutation (bool, optional): Whether to make the pydantic object mutable. Defaults to False.

    Returns:
        FullConfig: Pydantic object
    """
    conf = OmegaConf.to_container(conf, resolve=True)  # type: ignore
    return FullConfigSchema(**conf, allow_mutation=allow_mutation)


def load_test_cfg_as_omegaconf(
    config_file_name: str = "default_config",
    config_dir_path_rel: str = "../../../tests/config/",
    overrides: Optional[list[str]] = None,
) -> DictConfig:
    """Load config as omegaconf object."""
    with initialize(version_base=None, config_path=config_dir_path_rel):
        if overrides:
            cfg = compose(
                config_name=config_file_name,
                overrides=overrides,
            )
        else:
            cfg = compose(
                config_name=config_file_name,
            )

        # Override the type so we can get autocomplete and renaming
        # correctly working
        cfg: FullConfigSchema = cfg  # type: ignore

        gpu = cfg.project.gpu

        if not gpu and cfg.model.name == "xgboost":
            cfg.model.args["tree_method"] = "auto"

        return cfg


def load_app_cfg_as_pydantic(
    config_file_name: str,
    allow_mutation: bool = False,
    overrides: Optional[list[str]] = None,
):
    """Load application cfg as pydantic object."""
    cfg = load_test_cfg_as_omegaconf(
        config_file_name=config_file_name,
        overrides=overrides,
        config_dir_path_rel="../../../../application/config/",
    )

    return convert_omegaconf_to_pydantic_object(conf=cfg, allow_mutation=allow_mutation)


def load_test_cfg_as_pydantic(
    config_file_name: str,
    allow_mutation: bool = False,
    overrides: Optional[list[str]] = None,
) -> FullConfigSchema:
    """Load config as pydantic object."""
    cfg = load_test_cfg_as_omegaconf(
        config_file_name=config_file_name,
        overrides=overrides,
    )

    return convert_omegaconf_to_pydantic_object(conf=cfg, allow_mutation=allow_mutation)


class WatcherSchema(BaseModel):
    """Configuration for watchers."""

    archive_all: bool
    keep_alive_after_training_minutes: Union[int, float]
    n_runs_before_eval: int
    verbose: bool
