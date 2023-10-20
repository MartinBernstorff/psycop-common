from collections.abc import Sequence

import numpy as np
from timeseriesflattener.aggregation_fns import count, mean
from timeseriesflattener.feature_specs.group_specs import (
    PredictorGroupSpec,
    PredictorSpec,
)

from psycop.common.feature_generation.loaders.raw.load_diagnoses import (
    essential_hypertension,
)
from psycop.common.feature_generation.loaders.raw.load_lab_results import ldl
from psycop.projects.cvd.feature_generation.feature_layeres.base import (
    FeatureLayer,
    LayerNamedDataframe,
)


class CVDLayer1(FeatureLayer):
    def get_features(self, lookbehind_days: int) -> Sequence[PredictorSpec]:
        layer = 1
        ldl_spec = PredictorGroupSpec(
            named_dataframes=(LayerNamedDataframe(df=ldl(), name="ldl", layer=layer),),
            aggregation_fns=[mean],
            fallback=[np.nan],
            lookbehind_days=[lookbehind_days],
        ).create_combinations()

        essential_hypertension_spec = PredictorGroupSpec(
            named_dataframes=(
                LayerNamedDataframe(
                    df=essential_hypertension(),
                    name="essential_hypertension",
                    layer=layer,
                ),
            ),
            aggregation_fns=[count],
            fallback=[0],
            lookbehind_days=[lookbehind_days],
        ).create_combinations()

        return ldl_spec + essential_hypertension_spec
