"""Feature specification module."""
import logging
from typing import Callable

import numpy as np
from timeseriesflattener.aggregation_fns import count, latest, maximum, mean, minimum
from timeseriesflattener.feature_specs.group_specs import (
    NamedDataframe,
    OutcomeGroupSpec,
    PredictorGroupSpec,
)
from timeseriesflattener.feature_specs.single_specs import (
    AnySpec,
    BaseModel,
    OutcomeSpec,
    PredictorSpec,
    StaticSpec,
)

from psycop.common.feature_generation.application_modules.project_setup import (
    ProjectInfo,
)
from psycop.common.feature_generation.loaders.raw.load_demographic import sex_female
from psycop.common.feature_generation.loaders.raw.load_diagnoses import (
    essential_hypertension,
    f0_disorders,
    f1_disorders,
    f2_disorders,
    f3_disorders,
    f4_disorders,
    f5_disorders,
    f6_disorders,
    f7_disorders,
    f8_disorders,
    gerd,
    hyperkinetic_disorders,
    hyperlipidemia,
    polycystic_ovarian_syndrome,
    sleep_apnea,
)
from psycop.common.feature_generation.loaders.raw.load_lab_results import (
    alat,
    crp,
    fasting_ldl,
    hdl,
    ldl,
    triglycerides,
)
from psycop.common.feature_generation.loaders.raw.load_medications import (
    antihypertensives,
    antipsychotics,
    benzodiazepine_related_sleeping_agents,
    benzodiazepines,
    clozapine,
    diuretics,
    gerd_drugs,
    lamotrigine,
    lithium,
    pregabaline,
    selected_nassa,
    snri,
    ssri,
    statins,
    tca,
    top_10_weight_gaining_antipsychotics,
    valproate,
)
from psycop.common.feature_generation.loaders.raw.load_structured_sfi import (
    bmi,
    height_in_cm,
    weight_in_kg,
)
from psycop.projects.cancer.feature_generation.outcome_specification.cancer_loaders import (
    any_cancer,
)

log = logging.getLogger(__name__)


class SpecSet(BaseModel):
    """A set of unresolved specs, ready for resolving."""

    temporal_predictors: list[PredictorSpec]
    static_predictors: list[StaticSpec]
    outcomes: list[OutcomeSpec]
    metadata: list[AnySpec]


class FeatureSpecifier:
    """Feature specification class."""

    def __init__(
        self,
        project_info: ProjectInfo,
        min_set_for_debug: bool = False,
    ) -> None:
        self.min_set_for_debug = min_set_for_debug
        self.project_info = project_info

    def _get_static_predictor_specs(self) -> list[StaticSpec]:
        """Get static predictor specs."""
        return [
            StaticSpec(
                timeseries_df=sex_female(),
                feature_base_name="sex_female",
                prefix=self.project_info.prefix.predictor,
            ),
        ]

    def _get_metadata_specs(self) -> list[AnySpec]:
        """Get metadata specs."""
        log.info("-------- Generating metadata specs --------")

        return [
            StaticSpec(
                feature_base_name="any_cancer",
                timeseries_df=any_cancer(),
                prefix="",
            ),
        ]

    def _get_outcome_specs(self) -> list[OutcomeSpec]:
        """Get outcome specs."""
        log.info("-------- Generating outcome specs --------")

        if self.min_set_for_debug:
            return [
                OutcomeSpec(
                    feature_base_name="any_cancer",
                    timeseries_df=any_cancer(),
                    lookahead_days=365,
                    aggregation_fn=maximum,
                    fallback=0,
                    incident=True,
                    prefix=self.project_info.prefix.outcome,
                ),
            ]

        return OutcomeGroupSpec(
            named_dataframes=[NamedDataframe(df=any_cancer(), name="any_cancer")],
            lookahead_days=[year * 365 for year in (1, 2, 3, 4, 5)],
            aggregation_fns=[maximum],
            fallback=[0],
            incident=[True],  # Set to false because they can have multiple cancers????
            prefix=self.project_info.prefix.outcome,
        ).create_combinations()

    def _get_medication_specs(
        self,
        resolve_multiple: list[Callable],
        interval_days: list[float],
    ) -> list[PredictorSpec]:
        """Get medication specs."""
        log.info("-------- Generating medication specs --------")

        psychiatric_medications = PredictorGroupSpec(
            named_dataframes=(
                NamedDataframe(df=antipsychotics(), name="antipsychotics"),
                NamedDataframe(df=clozapine(), name="clozapine"),
                NamedDataframe(
                    df=top_10_weight_gaining_antipsychotics(),
                    name="top_10_weight_gaining_antipsychotics",
                ),
                NamedDataframe(df=lithium(), name="lithium"),
                NamedDataframe(df=valproate(), name="valproate"),
                NamedDataframe(df=lamotrigine(), name="lamotrigine"),
                NamedDataframe(df=benzodiazepines(), name="benzodiazepines"),
                NamedDataframe(df=pregabaline(), name="pregabaline"),
                NamedDataframe(df=ssri(), name="ssri"),
                NamedDataframe(df=snri(), name="snri"),
                NamedDataframe(df=tca(), name="tca"),
                NamedDataframe(df=selected_nassa(), name="selected_nassa"),
                NamedDataframe(
                    df=benzodiazepine_related_sleeping_agents(),
                    name="benzodiazepine_related_sleeping_agents",
                ),
            ),
            lookbehind_days=interval_days,
            aggregation_fns=resolve_multiple,
            fallback=[0],
        ).create_combinations()

        lifestyle_medications = PredictorGroupSpec(
            named_dataframes=(
                NamedDataframe(df=gerd_drugs(), name="gerd_drugs"),
                NamedDataframe(df=statins(), name="statins"),
                NamedDataframe(df=antihypertensives(), name="antihypertensives"),
                NamedDataframe(df=diuretics(), name="diuretics"),
            ),
            lookbehind_days=interval_days,
            aggregation_fns=resolve_multiple,
            fallback=[0],
        ).create_combinations()

        return psychiatric_medications + lifestyle_medications

    def _get_diagnoses_specs(
        self,
        resolve_multiple: list[Callable],
        interval_days: list[float],
    ) -> list[PredictorSpec]:
        """Get diagnoses specs."""
        log.info("-------- Generating diagnoses specs --------")

        lifestyle_diagnoses = PredictorGroupSpec(
            named_dataframes=(
                NamedDataframe(
                    df=essential_hypertension(),
                    name="essential_hypertension",
                ),
                NamedDataframe(df=hyperlipidemia(), name="hyperlipidemia"),
                NamedDataframe(
                    df=polycystic_ovarian_syndrome(),
                    name="polycystic_ovarian_syndrome",
                ),
                NamedDataframe(df=sleep_apnea(), name="sleep_apnea"),
                NamedDataframe(df=gerd(), name="gerd"),
            ),
            aggregation_fns=resolve_multiple,
            lookbehind_days=interval_days,
            fallback=[0],
        ).create_combinations()

        psychiatric_diagnoses = PredictorGroupSpec(
            named_dataframes=(
                NamedDataframe(df=f0_disorders(), name="f0_disorders"),
                NamedDataframe(df=f1_disorders(), name="f1_disorders"),
                NamedDataframe(df=f2_disorders(), name="f2_disorders"),
                NamedDataframe(df=f3_disorders(), name="f3_disorders"),
                NamedDataframe(df=f4_disorders(), name="f4_disorders"),
                NamedDataframe(df=f5_disorders(), name="f5_disorders"),
                NamedDataframe(df=f6_disorders(), name="f6_disorders"),
                NamedDataframe(df=f7_disorders(), name="f7_disorders"),
                NamedDataframe(df=f8_disorders(), name="f8_disorders"),
                NamedDataframe(
                    df=hyperkinetic_disorders(),
                    name="hyperkinetic_disorders",
                ),
            ),
            aggregation_fns=resolve_multiple,
            lookbehind_days=interval_days,
            fallback=[0],
        ).create_combinations()

        return lifestyle_diagnoses + psychiatric_diagnoses

    def _get_lab_result_specs(
        self,
        resolve_multiple: list[Callable],
        interval_days: list[float],
    ) -> list[PredictorSpec]:
        """Get lab result specs."""
        log.info("-------- Generating lab result specs --------")

        general_lab_results = PredictorGroupSpec(
            named_dataframes=(
                NamedDataframe(df=alat(), name="alat"),
                NamedDataframe(df=hdl(), name="hdl"),
                NamedDataframe(df=ldl(), name="ldl"),
                NamedDataframe(df=triglycerides(), name="triglycerides"),
                NamedDataframe(df=fasting_ldl(), name="fasting_ldl"),
                NamedDataframe(df=crp(), name="crp"),
            ),
            aggregation_fns=resolve_multiple,
            lookbehind_days=interval_days,
            fallback=[np.nan],
        ).create_combinations()

        return general_lab_results  # + diabetes_lab_results

    def _get_temporal_predictor_specs(self) -> list[PredictorSpec]:
        """Generate predictor spec list."""
        log.info("-------- Generating temporal predictor specs --------")

        if self.min_set_for_debug:
            return [
                PredictorSpec(
                    timeseries_df=alat(),
                    feature_base_name="alat",
                    lookbehind_days=30,
                    aggregation_fn=maximum,
                    fallback=np.nan,
                    prefix=self.project_info.prefix.predictor,
                ),
            ]

        resolve_multiple = [maximum, minimum, mean, latest, count]
        interval_days: list[float] = [30, 90, 180, 365, 730]

        lab_results = self._get_lab_result_specs(
            resolve_multiple,
            interval_days,
        )

        diagnoses = self._get_diagnoses_specs(
            resolve_multiple,
            interval_days,
        )

        medications = self._get_medication_specs(
            resolve_multiple,
            interval_days,
        )

        demographics = PredictorGroupSpec(
            named_dataframes=[
                NamedDataframe(df=weight_in_kg(), name="weight_in_kg"),
                NamedDataframe(df=height_in_cm(), name="height_in_cm"),
                NamedDataframe(df=bmi(), name="bmi"),
            ],
            lookbehind_days=interval_days,
            aggregation_fns=[latest],
            fallback=[np.nan],
            prefix=self.project_info.prefix.predictor,
        ).create_combinations()

        return lab_results + medications + diagnoses + demographics

    def get_feature_specs(self) -> list[AnySpec]:
        """Get a spec set."""

        if self.min_set_for_debug:
            log.warning(
                "--- !!! Using the minimum set of features for debugging !!! ---",
            )
            return (
                self._get_temporal_predictor_specs()
                + self._get_outcome_specs()
                + self._get_metadata_specs()
            )

        return (
            self._get_temporal_predictor_specs()
            + self._get_static_predictor_specs()
            + self._get_outcome_specs()
            + self._get_metadata_specs()
        )
