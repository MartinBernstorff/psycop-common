from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as dt
    from collections.abc import Sequence

    from psycop.common.data_structures import (
        Patient,
        StaticFeature,
        TemporalEvent,
    )


@dataclass(frozen=True)
class PredictionTime:
    """A cut sequence of events for a patient, ready to issue a prediction."""

    patient: Patient
    temporal_events: Sequence[TemporalEvent]
    static_features: Sequence[StaticFeature]
    prediction_timestamp: dt.datetime
    outcome: bool
