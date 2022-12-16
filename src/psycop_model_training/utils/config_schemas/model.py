from psycop_model_training.utils.config_schemas import BaseModel


class ModelConfSchema(BaseModel):
    """Model configuration."""

    name: str  # Model, can currently take xgboost
    require_imputation: bool  # Whether the model requires imputation. (shouldn't this be false?)
    args: dict
