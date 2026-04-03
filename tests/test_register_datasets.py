"""register_datasets 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import (
    DatasetPropertiesClass, SchemaMetadataClass, GlobalTagsClass,
)

from src.config import DATASET_NAMES
from src.register_datasets import build_dataset_mcps, DATASET_SCHEMAS, register_datasets


def test_dataset_schemas_cover_all_datasets():
    assert set(DATASET_SCHEMAS.keys()) == set(DATASET_NAMES)


def test_build_dataset_mcps_not_empty():
    mcps = build_dataset_mcps()
    assert len(mcps) > 0


def test_every_dataset_has_properties_and_schema():
    mcps = build_dataset_mcps()
    urns_with_props = set()
    urns_with_schema = set()

    for mcp in mcps:
        if isinstance(mcp.aspect, DatasetPropertiesClass):
            urns_with_props.add(mcp.entityUrn)
        elif isinstance(mcp.aspect, SchemaMetadataClass):
            urns_with_schema.add(mcp.entityUrn)

    assert len(urns_with_props) == len(DATASET_NAMES)
    assert len(urns_with_schema) == len(DATASET_NAMES)
    assert urns_with_props == urns_with_schema


def test_schema_fields_not_empty():
    mcps = build_dataset_mcps()
    for mcp in mcps:
        if isinstance(mcp.aspect, SchemaMetadataClass):
            assert len(mcp.aspect.fields) > 0, (
                f"Dataset {mcp.entityUrn} has no fields"
            )


def test_customer_table_has_pii_tags():
    mcps = build_dataset_mcps()
    customer_schema = None
    for mcp in mcps:
        if isinstance(mcp.aspect, SchemaMetadataClass) and "customer" in mcp.entityUrn and "features" not in mcp.entityUrn:
            customer_schema = mcp.aspect
            break

    assert customer_schema is not None
    pii_fields = [
        f for f in customer_schema.fields
        if f.globalTags and any("PII" in t.tag for t in f.globalTags.tags)
    ]
    assert len(pii_fields) >= 4  # name, birth_date, phone, email, address


def test_register_datasets_calls_emitter():
    emitter = MagicMock()
    result = register_datasets(emitter)
    assert len(result) > 0
    assert emitter.emit.call_count == len(result)
