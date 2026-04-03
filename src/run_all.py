"""DataHub 메타데이터 전체 등록 실행 스크립트.

실행 순서:
  1. 도메인 등록
  2. 태그 등록
  3. 용어사전 등록
  4. 데이터셋 등록 (스키마, 속성, 태그, 용어 연결)
  5. 리니지 등록
  6. ML 모델 등록
"""

import sys

from datahub.emitter.rest_emitter import DatahubRestEmitter

from src.config import DATAHUB_GMS_URL, DATAHUB_TOKEN, setup_logging
from src.register_domains import register_domains
from src.register_tags import register_tags
from src.register_glossary import register_glossary
from src.register_datasets import register_datasets
from src.register_lineage import register_lineage
from src.register_ml_models import register_ml_models

logger = setup_logging()


def create_emitter():
    """DataHub REST Emitter를 생성한다."""
    extra_headers = {}
    if DATAHUB_TOKEN:
        extra_headers["Authorization"] = f"Bearer {DATAHUB_TOKEN}"

    return DatahubRestEmitter(
        gms_server=DATAHUB_GMS_URL,
        extra_headers=extra_headers,
    )


STEPS = [
    ("도메인", register_domains),
    ("태그", register_tags),
    ("용어사전", register_glossary),
    ("데이터셋", register_datasets),
    ("리니지", register_lineage),
    ("ML 모델", register_ml_models),
]


def run_all():
    """전체 메타데이터 등록을 순서대로 실행한다."""
    logger.info("DataHub 메타데이터 등록 시작 (서버: %s)", DATAHUB_GMS_URL)

    emitter = create_emitter()
    total_mcps = 0

    for step_name, step_func in STEPS:
        logger.info("=== %s 등록 시작 ===", step_name)
        try:
            mcps = step_func(emitter)
            total_mcps += len(mcps)
            logger.info("=== %s 등록 완료 (%d건) ===", step_name, len(mcps))
        except Exception:
            logger.exception("=== %s 등록 실패 ===", step_name)
            raise

    logger.info("전체 등록 완료: 총 %d개 MCP 발행", total_mcps)
    return total_mcps


if __name__ == "__main__":
    try:
        run_all()
    except Exception:
        logger.exception("메타데이터 등록 중 오류 발생")
        sys.exit(1)
