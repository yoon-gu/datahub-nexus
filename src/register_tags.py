"""DataHub 태그 등록."""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import make_tag_urn
from datahub.metadata.schema_classes import TagPropertiesClass

from src.config import TAGS, setup_logging

logger = setup_logging()


def build_tag_mcps():
    """태그 생성 MCP 목록을 반환한다."""
    mcps = []
    for tag_name, description in TAGS.items():
        tag_urn = make_tag_urn(tag_name)
        mcp = MetadataChangeProposalWrapper(
            entityUrn=tag_urn,
            aspect=TagPropertiesClass(
                name=tag_name,
                description=description,
            ),
        )
        mcps.append(mcp)
    return mcps


def register_tags(emitter):
    """태그를 DataHub에 등록한다."""
    mcps = build_tag_mcps()
    for mcp in mcps:
        emitter.emit(mcp)
    logger.info("태그 %d개 등록 완료", len(mcps))
    return mcps
