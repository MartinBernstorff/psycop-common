from torch import nn

from psycop.common.sequence_models.tasks.tasks import (
    BEHRTForMaskedLM,
    EncoderForClassification,
)

from ..aggregators import AggregationModule
from ..embedders.BEHRT_embedders import BEHRTEmbedder
from ..optimizers import LRSchedulerFn, OptimizerFn
from ..registry import Registry


@Registry.tasks.register("behrt")
def create_behrt(
    embedding_module: BEHRTEmbedder,
    encoder_module: nn.Module,
    optimizer: OptimizerFn,
    lr_scheduler: LRSchedulerFn,
) -> BEHRTForMaskedLM:
    return BEHRTForMaskedLM(
        embedding_module=embedding_module,
        encoder_module=encoder_module,
        optimizer_fn=optimizer,
        lr_scheduler_fn=lr_scheduler,
    )


@Registry.tasks.register("encoder_for_clf")
def create_encoder_for_clf(
    embedding_module: BEHRTEmbedder,
    encoder_module: nn.Module,
    aggregation_module: AggregationModule,
    optimizer: OptimizerFn,
    lr_scheduler: LRSchedulerFn,
    num_classes: int = 2,
) -> EncoderForClassification:
    return EncoderForClassification(
        embedding_module=embedding_module,
        encoder_module=encoder_module,
        aggregation_module=aggregation_module,
        optimizer_fn=optimizer,
        lr_scheduler_fn=lr_scheduler,
        num_classes=num_classes,
    )
