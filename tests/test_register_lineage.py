"""register_lineage 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import UpstreamLineageClass

from src.register_lineage import build_lineage_mcps, LINEAGE_MAP, register_lineage


def test_build_lineage_mcps_count():
    mcps = build_lineage_mcps()
    assert len(mcps) == len(LINEAGE_MAP)


def test_lineage_mcps_have_correct_aspect():
    mcps = build_lineage_mcps()
    for mcp in mcps:
        assert isinstance(mcp.aspect, UpstreamLineageClass)
        assert len(mcp.aspect.upstreams) > 0


def test_customer_features_has_three_upstreams():
    mcps = build_lineage_mcps()
    cf_mcp = None
    for mcp in mcps:
        if "customer_features" in mcp.entityUrn:
            cf_mcp = mcp
            break
    assert cf_mcp is not None
    assert len(cf_mcp.aspect.upstreams) == 3


def test_campaign_performance_has_two_upstreams():
    mcps = build_lineage_mcps()
    perf_mcp = None
    for mcp in mcps:
        if "campaign_performance" in mcp.entityUrn:
            perf_mcp = mcp
            break
    assert perf_mcp is not None
    assert len(perf_mcp.aspect.upstreams) == 2


def test_register_lineage_calls_emitter():
    emitter = MagicMock()
    result = register_lineage(emitter)
    assert len(result) == len(LINEAGE_MAP)
    assert emitter.emit.call_count == len(LINEAGE_MAP)
