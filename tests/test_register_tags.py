"""register_tags 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import TagPropertiesClass

from src.config import TAGS
from src.register_tags import build_tag_mcps, register_tags


def test_build_tag_mcps_count():
    mcps = build_tag_mcps()
    assert len(mcps) == len(TAGS)


def test_build_tag_mcps_have_correct_urns():
    mcps = build_tag_mcps()
    for mcp in mcps:
        assert "urn:li:tag:" in mcp.entityUrn
        assert isinstance(mcp.aspect, TagPropertiesClass)
        assert mcp.aspect.name in TAGS


def test_register_tags_calls_emitter():
    emitter = MagicMock()
    result = register_tags(emitter)
    assert len(result) == len(TAGS)
    assert emitter.emit.call_count == len(TAGS)
