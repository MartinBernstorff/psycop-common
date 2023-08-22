from abc import ABC, abstractmethod
from typing import List, Sequence

from psycop.common.feature_generation.sequences.mlm_sequence_loaders.diagnoses_sequences import (
    EventDfLoader,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.patient import (
    Patient,
)


class AbstractMLMDataLoader(ABC):
    @staticmethod
    @abstractmethod
    def get_train_set(loaders: Sequence[EventDfLoader]) -> List[Patient]:
        ...
