import pandas as pd
from sklearn.pipeline import Pipeline

from psycop_model_training.preprocessing.post_split.feature_selectors import (
    DropDateTimeColumns,
)
from psycop_model_training.preprocessing.post_split.feature_transformers import (
    ConvertToBoolean,
    DateTimeConverter,
)
from psycop_model_training.utils.config_schemas.full_config import FullConfigSchema


def apply_pre_split_pipeline(cfg: FullConfigSchema, data: pd.DataFrame):
    pipe = create_pre_split_pipeline(cfg=cfg)

    return pipe.fit_transform(X=data)


def create_pre_split_pipeline(cfg: FullConfigSchema):
    steps = []
    # Conversion
    if cfg.preprocessing.pre_split.drop_datetime_predictor_columns:
        steps.append(
            (
                "DropDateTimeColumns",
                DropDateTimeColumns(pred_prefix=cfg.data.pred_prefix),
            ),
        )

    if cfg.preprocessing.pre_split.convert_datetimes_to_ordinal:
        dtconverter = DateTimeConverter()
        steps.append(("DateTimeConverter", dtconverter))

    if cfg.preprocessing.pre_split.convert_to_boolean:
        steps.append(("ConvertToBoolean", ConvertToBoolean()))

    return Pipeline(steps)
