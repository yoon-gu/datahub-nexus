"""DataHub 데이터셋 메타데이터 등록 (스키마, 설명, 태그, 용어 연결)."""

from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.mce_builder import (
    make_dataset_urn, make_data_platform_urn, make_tag_urn, make_term_urn,
)
from datahub.metadata.schema_classes import (
    DatasetPropertiesClass,
    SchemaMetadataClass,
    SchemaFieldClass,
    SchemaFieldDataTypeClass,
    StringTypeClass,
    NumberTypeClass,
    BooleanTypeClass,
    DateTypeClass,
    TimeTypeClass,
    MySqlDDLClass,
    GlobalTagsClass,
    TagAssociationClass,
    GlossaryTermsClass,
    GlossaryTermAssociationClass,
)

from src.config import PLATFORM, ENV, setup_logging

logger = setup_logging()


def _tags(*tag_names):
    """태그 목록을 GlobalTagsClass로 변환한다."""
    return GlobalTagsClass(
        tags=[TagAssociationClass(tag=make_tag_urn(t)) for t in tag_names]
    )


def _terms(*term_names):
    """용어 목록을 GlossaryTermsClass로 변환한다."""
    return GlossaryTermsClass(
        terms=[GlossaryTermAssociationClass(urn=make_term_urn(t)) for t in term_names],
        auditStamp=None,
    )


def _field(path, dtype_class, native_type, description, nullable=True,
           is_key=False, tags=None, terms=None):
    """SchemaField 헬퍼."""
    return SchemaFieldClass(
        fieldPath=path,
        type=SchemaFieldDataTypeClass(type=dtype_class()),
        nativeDataType=native_type,
        description=description,
        nullable=nullable,
        isPartOfKey=is_key,
        globalTags=tags,
        glossaryTerms=terms,
    )


S = StringTypeClass
N = NumberTypeClass
B = BooleanTypeClass
D = DateTypeClass
T = TimeTypeClass


# ============================================================
# 테이블별 스키마 정의
# ============================================================

DATASET_SCHEMAS = {
    "customer": {
        "description": "고객 프로필 마스터 테이블. 가입 고객의 인적 정보, 신용등급, 소득 정보를 관리한다.",
        "tags": ["Daily_Batch"],
        "fields": [
            _field("customer_id", S, "VARCHAR(20)", "고객 고유 식별자", False, True, terms=_terms("고객ID")),
            _field("name", S, "VARCHAR(100)", "고객 이름", False, tags=_tags("PII")),
            _field("birth_date", D, "DATE", "생년월일", False, tags=_tags("PII")),
            _field("gender", S, "CHAR(1)", "성별 (M/F)", False),
            _field("phone", S, "VARCHAR(20)", "연락처", tags=_tags("PII")),
            _field("email", S, "VARCHAR(100)", "이메일 주소", tags=_tags("PII")),
            _field("address", S, "VARCHAR(200)", "주소", tags=_tags("PII")),
            _field("registration_date", D, "DATE", "카드 최초 가입일", False),
            _field("credit_grade", S, "VARCHAR(10)", "신용등급 (1등급~10등급)", False, terms=_terms("신용등급")),
            _field("annual_income", N, "DECIMAL(15,2)", "연간 소득 (원)", tags=_tags("Financial"), terms=_terms("연소득")),
            _field("is_active", B, "BOOLEAN", "활성 고객 여부", False, terms=_terms("활성여부")),
        ],
    },
    "card_product": {
        "description": "카드 상품 마스터 테이블. 신용카드/체크카드 상품의 정보, 혜택, 적립률을 관리한다.",
        "tags": ["Daily_Batch"],
        "fields": [
            _field("product_id", S, "VARCHAR(20)", "상품 고유 식별자", False, True),
            _field("product_name", S, "VARCHAR(100)", "카드 상품명", False),
            _field("card_type", S, "VARCHAR(20)", "카드 유형 (CREDIT/CHECK)", False),
            _field("annual_fee", N, "DECIMAL(10,2)", "연회비 (원)", False, tags=_tags("Financial")),
            _field("benefit_category", S, "VARCHAR(50)", "주요 혜택 카테고리", False),
            _field("reward_rate", N, "DECIMAL(5,2)", "기본 적립률 (%)", False),
            _field("launch_date", D, "DATE", "상품 출시일", False),
            _field("is_active", B, "BOOLEAN", "현재 판매 중 여부", False),
        ],
    },
    "transaction": {
        "description": "카드 거래 내역 테이블. 모든 승인된 카드 결제 건의 상세 정보를 저장한다.",
        "tags": ["Realtime", "Financial"],
        "fields": [
            _field("transaction_id", S, "VARCHAR(30)", "거래 고유 식별자", False, True),
            _field("customer_id", S, "VARCHAR(20)", "고객 ID (FK)", False, terms=_terms("고객ID")),
            _field("product_id", S, "VARCHAR(20)", "카드 상품 ID (FK)", False),
            _field("transaction_date", T, "TIMESTAMP", "거래 일시", False),
            _field("merchant_name", S, "VARCHAR(100)", "가맹점명", False),
            _field("merchant_category", S, "VARCHAR(50)", "가맹점 업종 코드", False, terms=_terms("업종코드")),
            _field("amount", N, "DECIMAL(15,2)", "거래 금액 (원)", False, tags=_tags("Financial"), terms=_terms("거래금액")),
            _field("is_installment", B, "BOOLEAN", "할부 거래 여부", False, terms=_terms("할부거래")),
            _field("installment_months", N, "INT", "할부 개월수 (일시불=0)", False),
            _field("is_overseas", B, "BOOLEAN", "해외 거래 여부", False, terms=_terms("해외거래")),
        ],
    },
    "customer_features": {
        "description": "고객 피처 테이블. 거래 데이터를 집계/가공한 AI 모델 입력용 피처를 저장한다. 일배치로 갱신된다.",
        "tags": ["ML_Feature", "Daily_Batch"],
        "fields": [
            _field("customer_id", S, "VARCHAR(20)", "고객 ID", False, True, terms=_terms("고객ID")),
            _field("feature_date", D, "DATE", "피처 기준일", False, True),
            _field("total_spend_3m", N, "DECIMAL(15,2)", "최근 3개월 총 이용금액", False, tags=_tags("Financial", "ML_Feature")),
            _field("avg_spend_monthly", N, "DECIMAL(15,2)", "월평균 이용금액", False, tags=_tags("Financial", "ML_Feature"), terms=_terms("월평균이용금액")),
            _field("transaction_count_3m", N, "INT", "최근 3개월 거래 건수", False, tags=_tags("ML_Feature"), terms=_terms("이용건수")),
            _field("top_merchant_category", S, "VARCHAR(50)", "최다 이용 업종"),
            _field("overseas_ratio", N, "DECIMAL(5,4)", "해외 이용 비율", False, tags=_tags("ML_Feature"), terms=_terms("해외이용비율")),
            _field("installment_ratio", N, "DECIMAL(5,4)", "할부 이용 비율", False, tags=_tags("ML_Feature")),
            _field("days_since_last_txn", N, "INT", "최근 거래 후 경과일수", False, tags=_tags("ML_Feature")),
            _field("active_cards_count", N, "INT", "활성 카드 수", False, tags=_tags("ML_Feature")),
            _field("credit_utilization", N, "DECIMAL(5,4)", "신용 한도 이용률", False, tags=_tags("Financial", "ML_Feature"), terms=_terms("한도이용률")),
            _field("complaint_count_6m", N, "INT", "최근 6개월 민원 건수", False, tags=_tags("ML_Feature")),
        ],
    },
    "model_metadata": {
        "description": "AI 모델 관리 메타데이터 테이블. 모델의 이름, 유형, 알고리즘, 성능 지표, 상태 등을 관리한다.",
        "tags": ["ML_Output"],
        "fields": [
            _field("model_id", S, "VARCHAR(30)", "모델 고유 식별자", False, True),
            _field("model_name", S, "VARCHAR(100)", "모델 이름", False),
            _field("model_type", S, "VARCHAR(50)", "모델 유형 (Classification/Regression/Clustering)", False),
            _field("algorithm", S, "VARCHAR(50)", "알고리즘 (XGBoost, LightGBM 등)", False),
            _field("target_variable", S, "VARCHAR(50)", "예측 대상 변수명", False),
            _field("train_date", D, "DATE", "모델 학습일", False),
            _field("auc_score", N, "DECIMAL(5,4)", "AUC 성능 지표", terms=_terms("AUC")),
            _field("precision_score", N, "DECIMAL(5,4)", "Precision 성능 지표"),
            _field("recall_score", N, "DECIMAL(5,4)", "Recall 성능 지표"),
            _field("feature_count", N, "INT", "사용 피처 수", False),
            _field("status", S, "VARCHAR(20)", "모델 상태 (active/deprecated)", False),
        ],
    },
    "model_scores": {
        "description": "AI 모델 예측 스코어 테이블. 각 모델이 고객별로 산출한 예측 스코어와 세그먼트 정보를 저장한다.",
        "tags": ["ML_Output", "Daily_Batch"],
        "fields": [
            _field("customer_id", S, "VARCHAR(20)", "고객 ID", False, True, terms=_terms("고객ID")),
            _field("score_date", D, "DATE", "스코어 산출일", False, True),
            _field("model_id", S, "VARCHAR(30)", "모델 ID (FK)", False, True),
            _field("model_version", S, "VARCHAR(10)", "모델 버전", False),
            _field("score", N, "DECIMAL(7,4)", "예측 스코어 (0~1)", False, tags=_tags("ML_Output"), terms=_terms("예측스코어")),
            _field("segment", S, "VARCHAR(20)", "세그먼트 라벨", terms=_terms("세그먼트")),
            _field("rank_percentile", N, "DECIMAL(5,2)", "백분위 순위"),
        ],
    },
    "campaign": {
        "description": "마케팅 캠페인 마스터 테이블. 캠페인의 기본 정보, 유형, 채널, 타겟 모델, 예산 등을 관리한다.",
        "tags": ["Daily_Batch"],
        "fields": [
            _field("campaign_id", S, "VARCHAR(30)", "캠페인 고유 식별자", False, True),
            _field("campaign_name", S, "VARCHAR(100)", "캠페인 이름", False),
            _field("campaign_type", S, "VARCHAR(30)", "캠페인 유형 (cross_sell/retention/activation/upsell/winback)", False),
            _field("channel", S, "VARCHAR(30)", "발송 채널 (SMS/PUSH/EMAIL/APP/LMS)", False),
            _field("start_date", D, "DATE", "캠페인 시작일", False),
            _field("end_date", D, "DATE", "캠페인 종료일", False),
            _field("target_model_id", S, "VARCHAR(30)", "타겟 선정에 사용한 AI 모델 ID (FK)"),
            _field("target_segment", S, "VARCHAR(20)", "타겟 세그먼트", terms=_terms("타겟세그먼트")),
            _field("offer_description", S, "VARCHAR(200)", "오퍼 내용 설명"),
            _field("budget", N, "DECIMAL(15,2)", "캠페인 예산 (원)", False, tags=_tags("Financial")),
            _field("status", S, "VARCHAR(20)", "캠페인 상태 (planned/active/completed)", False),
        ],
    },
    "campaign_target": {
        "description": "캠페인 타겟 고객 테이블. AI 모델 스코어 기반으로 선정된 캠페인 발송 대상 고객 목록이다.",
        "tags": ["Daily_Batch"],
        "fields": [
            _field("campaign_id", S, "VARCHAR(30)", "캠페인 ID (FK)", False, True),
            _field("customer_id", S, "VARCHAR(20)", "고객 ID (FK)", False, True, terms=_terms("고객ID")),
            _field("model_score", N, "DECIMAL(7,4)", "타겟 선정 시 모델 스코어", terms=_terms("예측스코어")),
            _field("target_rank", N, "INT", "타겟 순위 (스코어 기반)"),
            _field("is_control_group", B, "BOOLEAN", "대조군 포함 여부", False, terms=_terms("대조군")),
            _field("sent_date", T, "TIMESTAMP", "캠페인 발송 일시"),
        ],
    },
    "campaign_response": {
        "description": "캠페인 응답 테이블. 캠페인에 대한 고객의 반응(오픈, 클릭, 전환)을 기록한다.",
        "tags": ["Realtime"],
        "fields": [
            _field("campaign_id", S, "VARCHAR(30)", "캠페인 ID (FK)", False),
            _field("customer_id", S, "VARCHAR(20)", "고객 ID (FK)", False, terms=_terms("고객ID")),
            _field("response_type", S, "VARCHAR(20)", "응답 유형 (open/click/convert)", False),
            _field("response_date", T, "TIMESTAMP", "응답 일시", False),
            _field("conversion_amount", N, "DECIMAL(15,2)", "전환 발생 금액 (원)", tags=_tags("Financial")),
        ],
    },
    "campaign_performance": {
        "description": "캠페인 성과 집계 테이블. 캠페인별 발송, 오픈, 클릭, 전환 등 성과 KPI를 집계한다.",
        "tags": ["KPI", "Daily_Batch"],
        "fields": [
            _field("campaign_id", S, "VARCHAR(30)", "캠페인 ID (FK)", False, True),
            _field("total_target", N, "INT", "총 타겟 고객 수", False),
            _field("total_sent", N, "INT", "총 발송 수", False),
            _field("total_open", N, "INT", "총 오픈 수", False),
            _field("total_click", N, "INT", "총 클릭 수", False),
            _field("total_conversion", N, "INT", "총 전환 수", False, tags=_tags("KPI")),
            _field("conversion_rate", N, "DECIMAL(5,4)", "전환율", False, tags=_tags("KPI"), terms=_terms("전환율")),
            _field("total_revenue", N, "DECIMAL(15,2)", "총 매출 (원)", False, tags=_tags("Financial", "KPI")),
            _field("roi", N, "DECIMAL(7,4)", "투자 수익률", False, tags=_tags("KPI"), terms=_terms("ROI")),
            _field("lift", N, "DECIMAL(7,4)", "대조군 대비 Lift", False, tags=_tags("KPI"), terms=_terms("Lift")),
        ],
    },
}


def build_dataset_mcps():
    """모든 데이터셋의 속성 + 스키마 MCP 목록을 반환한다."""
    mcps = []
    platform_urn = make_data_platform_urn(PLATFORM)

    for dataset_name, schema_def in DATASET_SCHEMAS.items():
        dataset_urn = make_dataset_urn(
            platform=PLATFORM,
            name=dataset_name,
            env=ENV,
        )

        # 데이터셋 속성
        props_mcp = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=DatasetPropertiesClass(
                name=dataset_name,
                description=schema_def["description"],
                customProperties={
                    "layer": _get_layer(dataset_name),
                    "tags": ",".join(schema_def["tags"]),
                },
            ),
        )
        mcps.append(props_mcp)

        # 데이터셋 레벨 태그
        if schema_def.get("tags"):
            dataset_tags_mcp = MetadataChangeProposalWrapper(
                entityUrn=dataset_urn,
                aspect=GlobalTagsClass(
                    tags=[
                        TagAssociationClass(tag=make_tag_urn(t))
                        for t in schema_def["tags"]
                    ]
                ),
            )
            mcps.append(dataset_tags_mcp)

        # 스키마 메타데이터
        schema_mcp = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=SchemaMetadataClass(
                schemaName=dataset_name,
                platform=platform_urn,
                version=0,
                hash="",
                platformSchema=MySqlDDLClass(tableSchema=""),
                fields=schema_def["fields"],
            ),
        )
        mcps.append(schema_mcp)

    return mcps


def _get_layer(dataset_name):
    """데이터셋 이름으로 레이어를 판별한다."""
    if dataset_name in ("customer", "card_product", "transaction"):
        return "raw"
    if dataset_name == "customer_features":
        return "feature"
    if dataset_name in ("model_metadata", "model_scores"):
        return "model"
    return "campaign"


def register_datasets(emitter):
    """모든 데이터셋을 DataHub에 등록한다."""
    mcps = build_dataset_mcps()
    for mcp in mcps:
        emitter.emit(mcp)
    logger.info("데이터셋 메타데이터 %d개 등록 완료", len(mcps))
    return mcps
