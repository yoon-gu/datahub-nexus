"""DataHub 도메인 등록 및 데이터셋-도메인 매핑."""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import make_domain_urn, make_dataset_urn
from datahub.metadata.schema_classes import DomainPropertiesClass, DomainsClass

from src.config import (
    DOMAINS, DATASET_DOMAIN_MAP, PLATFORM, ENV, setup_logging,
)

logger = setup_logging()


def build_domain_mcps():
    """도메인 생성 MCP 목록을 반환한다."""
    mcps = []
    for domain_name, description in DOMAINS.items():
        domain_urn = make_domain_urn(domain_name)
        mcp = MetadataChangeProposalWrapper(
            entityUrn=domain_urn,
            aspect=DomainPropertiesClass(
                name=domain_name,
                description=description,
            ),
        )
        mcps.append(mcp)
    return mcps


def build_dataset_domain_mcps():
    """데이터셋에 도메인을 할당하는 MCP 목록을 반환한다."""
    mcps = []
    for dataset_name, domain_name in DATASET_DOMAIN_MAP.items():
        dataset_urn = make_dataset_urn(
            platform=PLATFORM,
            name=dataset_name,
            env=ENV,
        )
        domain_urn = make_domain_urn(domain_name)
        mcp = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=DomainsClass(domains=[domain_urn]),
        )
        mcps.append(mcp)
    return mcps


def register_domains(emitter):
    """도메인 생성 및 데이터셋-도메인 매핑을 등록한다."""
    domain_mcps = build_domain_mcps()
    for mcp in domain_mcps:
        emitter.emit(mcp)
    logger.info("도메인 %d개 등록 완료", len(domain_mcps))

    mapping_mcps = build_dataset_domain_mcps()
    for mcp in mapping_mcps:
        emitter.emit(mcp)
    logger.info("데이터셋-도메인 매핑 %d개 등록 완료", len(mapping_mcps))

    return domain_mcps + mapping_mcps
