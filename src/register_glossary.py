"""DataHub 용어사전(Glossary) 등록."""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import make_term_urn
from datahub.metadata.schema_classes import (
    GlossaryTermInfoClass,
    GlossaryNodeInfoClass,
)

from src.config import GLOSSARY_NODES, GLOSSARY_TERMS, setup_logging

logger = setup_logging()


def _make_glossary_node_urn(node_name):
    return f"urn:li:glossaryNode:{node_name}"


def build_glossary_node_mcps():
    """용어 그룹(Glossary Node) MCP 목록을 반환한다."""
    mcps = []
    for node_name, definition in GLOSSARY_NODES.items():
        node_urn = _make_glossary_node_urn(node_name)
        mcp = MetadataChangeProposalWrapper(
            entityUrn=node_urn,
            aspect=GlossaryNodeInfoClass(
                definition=definition,
                name=node_name,
            ),
        )
        mcps.append(mcp)
    return mcps


def build_glossary_term_mcps():
    """용어(Glossary Term) MCP 목록을 반환한다."""
    mcps = []
    for term_name, info in GLOSSARY_TERMS.items():
        term_urn = make_term_urn(term_name)
        parent_node_urn = _make_glossary_node_urn(info["group"])
        mcp = MetadataChangeProposalWrapper(
            entityUrn=term_urn,
            aspect=GlossaryTermInfoClass(
                definition=info["definition"],
                termSource="INTERNAL",
                name=term_name,
                parentNode=parent_node_urn,
            ),
        )
        mcps.append(mcp)
    return mcps


def register_glossary(emitter):
    """용어 그룹 및 용어를 DataHub에 등록한다."""
    node_mcps = build_glossary_node_mcps()
    for mcp in node_mcps:
        emitter.emit(mcp)
    logger.info("용어 그룹 %d개 등록 완료", len(node_mcps))

    term_mcps = build_glossary_term_mcps()
    for mcp in term_mcps:
        emitter.emit(mcp)
    logger.info("용어 %d개 등록 완료", len(term_mcps))

    return node_mcps + term_mcps
