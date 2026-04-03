"""register_domains 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import DomainPropertiesClass, DomainsClass

from src.config import DOMAINS, DATASET_DOMAIN_MAP
from src.register_domains import build_domain_mcps, build_dataset_domain_mcps, register_domains


def test_build_domain_mcps_count():
    mcps = build_domain_mcps()
    assert len(mcps) == len(DOMAINS)


def test_build_domain_mcps_have_correct_urns():
    mcps = build_domain_mcps()
    for mcp in mcps:
        assert "urn:li:domain:" in mcp.entityUrn
        assert isinstance(mcp.aspect, DomainPropertiesClass)


def test_build_dataset_domain_mcps_count():
    mcps = build_dataset_domain_mcps()
    assert len(mcps) == len(DATASET_DOMAIN_MAP)


def test_build_dataset_domain_mcps_have_domains_aspect():
    mcps = build_dataset_domain_mcps()
    for mcp in mcps:
        assert "urn:li:dataset:" in mcp.entityUrn
        assert isinstance(mcp.aspect, DomainsClass)
        assert len(mcp.aspect.domains) == 1


def test_register_domains_calls_emitter():
    emitter = MagicMock()
    result = register_domains(emitter)
    expected_count = len(DOMAINS) + len(DATASET_DOMAIN_MAP)
    assert len(result) == expected_count
    assert emitter.emit.call_count == expected_count
