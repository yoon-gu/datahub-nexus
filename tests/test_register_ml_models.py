"""register_ml_models 모듈 테스트."""

from unittest.mock import MagicMock

from datahub.metadata.schema_classes import (
    MLModelPropertiesClass, MLModelGroupPropertiesClass,
)

from src.config import ML_MODELS
from src.register_ml_models import (
    build_model_group_mcps, build_ml_model_mcps, register_ml_models,
)


def test_build_model_group_mcps():
    mcps = build_model_group_mcps()
    assert len(mcps) == 1
    assert isinstance(mcps[0].aspect, MLModelGroupPropertiesClass)


def test_build_ml_model_mcps_count():
    mcps = build_ml_model_mcps()
    assert len(mcps) == len(ML_MODELS)


def test_ml_model_mcps_have_correct_aspect():
    mcps = build_ml_model_mcps()
    for mcp in mcps:
        assert "urn:li:mlModel:" in mcp.entityUrn
        assert isinstance(mcp.aspect, MLModelPropertiesClass)
        assert mcp.aspect.description is not None
        assert "algorithm" in mcp.aspect.customProperties


def test_ml_model_mcps_belong_to_group():
    mcps = build_ml_model_mcps()
    for mcp in mcps:
        assert mcp.aspect.groups is not None
        assert len(mcp.aspect.groups) == 1
        assert "urn:li:mlModelGroup:" in mcp.aspect.groups[0]


def test_register_ml_models_calls_emitter():
    emitter = MagicMock()
    result = register_ml_models(emitter)
    # 1 group + 5 models = 6
    expected = 1 + len(ML_MODELS)
    assert len(result) == expected
    assert emitter.emit.call_count == expected
