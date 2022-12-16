from psycop_model_training.utils.basemodel import BaseModel


class WandbSchema(BaseModel):
    """Configuration for weights and biases."""

    group: str
    mode: str
    entity: str


class ProjectSchema(BaseModel):
    """Project configuration."""

    wandb: WandbSchema
    name: str = "psycop_model_training"
    seed: int
    gpu: bool
