"""Testing of config schemas."""
from pathlib import Path

import pytest
from hydra import compose, initialize

from psycop_model_training.utils.config_schemas.conf_utils import (
    convert_omegaconf_to_pydantic_object,
)
from psycop_model_training.utils.utils import PROJECT_ROOT

CONFIG_DIR_PATH_ABS = PROJECT_ROOT / "tests" / "config"
CONFIG_DIR_PATH_REL = "../tests/config"

CONFIG_DIR_PATH_APP_ABS = PROJECT_ROOT / "application" / "config"


def get_config_file_names() -> list[str]:
    """Get all config file names."""
    config_file_paths = list(CONFIG_DIR_PATH_ABS.glob("*.yaml"))

    return [f"{path.stem}.yaml" for path in config_file_paths]


@pytest.mark.parametrize("config_file_name", get_config_file_names())
def test_test_configs(config_file_name):
    """Test that all configs load correctly."""
    with initialize(version_base=None, config_path=CONFIG_DIR_PATH_REL):
        cfg = compose(
            config_name=config_file_name,
        )

    cfg = convert_omegaconf_to_pydantic_object(conf=cfg)


@pytest.mark.parametrize("config_file_name", get_config_file_names())
def test_app_configs(config_file_name):
    """Test that all configs load correctly."""
    with initialize(version_base=None, config_path=CONFIG_DIR_PATH_REL):
        cfg = compose(
            config_name=config_file_name,
        )

    cfg = convert_omegaconf_to_pydantic_object(conf=cfg)
