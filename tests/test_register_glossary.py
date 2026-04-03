"""register_glossary 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import GlossaryNodeInfoClass, GlossaryTermInfoClass

from src.config import GLOSSARY_NODES, GLOSSARY_TERMS
from src.register_glossary import (
    build_glossary_node_mcps, build_glossary_term_mcps, register_glossary,
)


def test_build_glossary_node_mcps_count():
    mcps = build_glossary_node_mcps()
    assert len(mcps) == len(GLOSSARY_NODES)


def test_build_glossary_node_mcps_have_correct_type():
    mcps = build_glossary_node_mcps()
    for mcp in mcps:
        assert "urn:li:glossaryNode:" in mcp.entityUrn
        assert isinstance(mcp.aspect, GlossaryNodeInfoClass)


def test_build_glossary_term_mcps_count():
    mcps = build_glossary_term_mcps()
    assert len(mcps) == len(GLOSSARY_TERMS)


def test_build_glossary_term_mcps_have_parent_node():
    mcps = build_glossary_term_mcps()
    for mcp in mcps:
        assert "urn:li:glossaryTerm:" in mcp.entityUrn
        assert isinstance(mcp.aspect, GlossaryTermInfoClass)
        assert mcp.aspect.parentNode is not None
        assert "urn:li:glossaryNode:" in mcp.aspect.parentNode


def test_register_glossary_calls_emitter():
    emitter = MagicMock()
    result = register_glossary(emitter)
    expected = len(GLOSSARY_NODES) + len(GLOSSARY_TERMS)
    assert len(result) == expected
    assert emitter.emit.call_count == expected
