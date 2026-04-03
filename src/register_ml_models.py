"""DataHub ML 모델 메타데이터 등록.

5개 AI 모델을 DataHub의 MLModel / MLModelGroup 엔티티로 등록하고,
모델과 데이터셋 간 리니지를 설정한다.
"""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import (
    make_ml_model_urn,
    make_ml_model_group_urn,
    make_dataset_urn,
)
from datahub.metadata.schema_classes import (
    MLModelPropertiesClass,
    MLModelGroupPropertiesClass,
)

from src.config import PLATFORM, ENV, ML_MODELS, setup_logging

logger = setup_logging()

MODEL_GROUP_NAME = "credit_card_marketing_models"
MODEL_GROUP_DESCRIPTION = (
    "신용카드 마케팅 플랫폼 AI 모델 그룹. "
    "이탈예측, 교차판매, 신용스코어링, 고객세그멘테이션, 응답예측 모델을 포함한다."
)

# 모델이 사용하는 입력 피처 테이블
MODEL_INPUT_DATASETS = ["customer_features"]
# 모델 스코어가 저장되는 테이블
MODEL_OUTPUT_DATASET = "model_scores"


def build_model_group_mcps():
    """ML 모델 그룹 MCP를 반환한다."""
    group_urn = make_ml_model_group_urn(
        platform=PLATFORM,
        group_name=MODEL_GROUP_NAME,
        env=ENV,
    )
    mcp = MetadataChangeProposalWrapper(
        entityUrn=group_urn,
        aspect=MLModelGroupPropertiesClass(
            description=MODEL_GROUP_DESCRIPTION,
            createdAt=None,
        ),
    )
    return [mcp]


def build_ml_model_mcps():
    """각 ML 모델의 속성 MCP 목록을 반환한다."""
    mcps = []
    group_urn = make_ml_model_group_urn(
        platform=PLATFORM,
        group_name=MODEL_GROUP_NAME,
        env=ENV,
    )

    for model_key, model_info in ML_MODELS.items():
        model_urn = make_ml_model_urn(
            platform=PLATFORM,
            model_name=model_key,
            env=ENV,
        )
        mcp = MetadataChangeProposalWrapper(
            entityUrn=model_urn,
            aspect=MLModelPropertiesClass(
                description=model_info["description"],
                type=model_info["type"],
                mlFeatures=None,
                groups=[group_urn],
                customProperties={
                    "algorithm": model_info["algorithm"],
                    "model_id": model_info["model_id"],
                    "display_name": model_info["name"],
                },
            ),
        )
        mcps.append(mcp)

    return mcps


def register_ml_models(emitter):
    """ML 모델 그룹 및 모델을 DataHub에 등록한다."""
    group_mcps = build_model_group_mcps()
    for mcp in group_mcps:
        emitter.emit(mcp)
    logger.info("ML 모델 그룹 등록 완료")

    model_mcps = build_ml_model_mcps()
    for mcp in model_mcps:
        emitter.emit(mcp)
    logger.info("ML 모델 %d개 등록 완료", len(model_mcps))

    return group_mcps + model_mcps
