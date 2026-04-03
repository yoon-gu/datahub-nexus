"""DataHub 데이터 리니지(Lineage) 등록.

데이터 흐름:
  customer + transaction + card_product → customer_features
  customer_features + model_metadata → model_scores
  model_scores + campaign → campaign_target
  campaign_target → campaign_response
  campaign_response + campaign → campaign_performance
"""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import make_dataset_urn
from datahub.metadata.schema_classes import (
    UpstreamLineageClass,
    UpstreamClass,
    DatasetLineageTypeClass,
)

from src.config import PLATFORM, ENV, setup_logging

logger = setup_logging()


def _dataset_urn(name):
    return make_dataset_urn(platform=PLATFORM, name=name, env=ENV)


def _upstream(name, lineage_type=DatasetLineageTypeClass.TRANSFORMED):
    return UpstreamClass(dataset=_dataset_urn(name), type=lineage_type)


# 리니지 정의: {downstream: [upstream1, upstream2, ...]}
LINEAGE_MAP = {
    "customer_features": [
        _upstream("customer"),
        _upstream("transaction"),
        _upstream("card_product"),
    ],
    "model_scores": [
        _upstream("customer_features"),
        _upstream("model_metadata"),
    ],
    "campaign_target": [
        _upstream("model_scores"),
        _upstream("campaign"),
    ],
    "campaign_response": [
        _upstream("campaign_target"),
    ],
    "campaign_performance": [
        _upstream("campaign_response"),
        _upstream("campaign"),
    ],
}


def build_lineage_mcps():
    """리니지 MCP 목록을 반환한다."""
    mcps = []
    for downstream_name, upstreams in LINEAGE_MAP.items():
        downstream_urn = _dataset_urn(downstream_name)
        mcp = MetadataChangeProposalWrapper(
            entityUrn=downstream_urn,
            aspect=UpstreamLineageClass(upstreams=upstreams),
        )
        mcps.append(mcp)
    return mcps


def register_lineage(emitter):
    """데이터 리니지를 DataHub에 등록한다."""
    mcps = build_lineage_mcps()
    for mcp in mcps:
        emitter.emit(mcp)
    logger.info("리니지 %d개 등록 완료", len(mcps))
    return mcps
