import datetime as dt
from collections.abc import Sequence
from dataclasses import dataclass, field

from psycop.common.feature_generation.sequences.timeseries_windower_python.events.static_feature import (
    StaticFeature,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.events.temporal_event import (
    TemporalEvent,
)
from psycop.common.feature_generation.sequences.timeseries_windower_python.prediction_time import (
    PredictionTime,
)


@dataclass
class Patient:
    """All task-agnostic data for a patient."""

    patient_id: str | int
    _temporal_events: list[TemporalEvent] = field(default_factory=list)
    _static_features: list[StaticFeature] = field(default_factory=list)

    @staticmethod
    def _filter_events_within_time_interval(
        events: Sequence[TemporalEvent],
        start: dt.datetime,
        end: dt.datetime,
    ) -> Sequence[TemporalEvent]:
        # This could be much faster if we assume that the events are already sorted.
        # Then we could implement binary search, which is O(log n) instead of O(n).
        # However, this might be plenty fast. We can always optimize later.
        return [event for event in events if start <= event.timestamp < end]

    def add_events(self, events: list[TemporalEvent | StaticFeature]):
        # add patient reference to each event 
        for event in events:
            event.patient = self

        self._temporal_events += [event for event in events if isinstance(event, TemporalEvent)]
        self._static_features += [event for event in events if isinstance(event, StaticFeature)]

    @property
    def temporal_events(self) -> Sequence[TemporalEvent]:
        self._temporal_events.sort(key=lambda event: event.timestamp)
        return self._temporal_events

    @property
    def static_events(self) -> Sequence[StaticFeature]:
        return self._static_features

    def to_prediction_times(
        self,
        lookbehind: dt.timedelta,
        lookahead: dt.timedelta,
        outcome_timestamp: dt.datetime,
        prediction_timestamps: Sequence[dt.datetime],
    ) -> list[PredictionTime]:
        """Converts a patient's task-agnostic data into an object specific for the given task. E.g. for the task of predicting whether a patient will be diagnosed with diabetes within the next year, this function will return a list of PredictionTime objects, each of which contains the patient's data for a specific prediction time (predictors, prediction timestamp and whether the outcome occurs within the lookahead)."""
        # Map each prediction time to a prediction sequence:
        prediction_sequences = []

        for prediction_timestamp in prediction_timestamps:
            # 1. Filter the predictor events to those that are relevant to the prediction time. (Keep all static, drop all temporal that are outside the lookbehind window.)
            filtered_events = self._filter_events_within_time_interval(
                events=self.temporal_events,
                start=prediction_timestamp - lookbehind,
                end=prediction_timestamp,
            )

            outcome_within_lookahead = outcome_timestamp <= (
                prediction_timestamp + lookahead
            )

            # 2. Return prediction sequences
            prediction_sequences.append(
                PredictionTime(
                    patient=self,
                    prediction_timestamp=prediction_timestamp,
                    temporal_events=filtered_events,
                    outcome=outcome_within_lookahead,
                    static_features=self._static_features,
                ),
            )

        return prediction_sequences
