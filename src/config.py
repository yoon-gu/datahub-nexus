"""DataHub 신용카드 마케팅 플랫폼 - 공통 설정 및 상수."""

import os
import logging

from dotenv import load_dotenv

load_dotenv()

# DataHub 연결 설정
DATAHUB_GMS_URL = os.getenv("DATAHUB_GMS_URL", "http://localhost:8080")
DATAHUB_TOKEN = os.getenv("DATAHUB_TOKEN", "")

# 플랫폼 및 환경
PLATFORM = "mysql"
PLATFORM_INSTANCE = "credit_card_dw"
ENV = "PROD"

# 데이터셋 이름 (platform.instance.table 형태로 DataHub에 등록)
DATASET_NAMES = [
    "customer",
    "card_product",
    "transaction",
    "customer_features",
    "model_metadata",
    "model_scores",
    "campaign",
    "campaign_target",
    "campaign_response",
    "campaign_performance",
]

# 도메인 정의
DOMAINS = {
    "Customer": "고객 관련 데이터 도메인 (고객 프로필, 카드 상품)",
    "Marketing": "마케팅 캠페인 관련 데이터 도메인 (캠페인, 타겟, 응답, 성과)",
    "Risk": "리스크 및 신용 관리 데이터 도메인",
    "Analytics": "분석 및 ML 관련 데이터 도메인 (피처, 모델 스코어, 모델 메타데이터)",
}

# 데이터셋 → 도메인 매핑
DATASET_DOMAIN_MAP = {
    "customer": "Customer",
    "card_product": "Customer",
    "transaction": "Customer",
    "customer_features": "Analytics",
    "model_metadata": "Analytics",
    "model_scores": "Analytics",
    "campaign": "Marketing",
    "campaign_target": "Marketing",
    "campaign_response": "Marketing",
    "campaign_performance": "Marketing",
}

# 태그 정의
TAGS = {
    "PII": "개인식별정보 (이름, 전화번호, 이메일, 주소 등)",
    "Financial": "금융 정보 (거래금액, 소득, 한도 등)",
    "ML_Feature": "ML 모델 입력 피처",
    "ML_Output": "ML 모델 출력 (예측 스코어, 세그먼트 등)",
    "KPI": "핵심 성과 지표",
    "Realtime": "실시간 처리 대상 데이터",
    "Daily_Batch": "일배치 처리 대상 데이터",
}

# ML 모델 정의
ML_MODELS = {
    "churn_prediction": {
        "name": "이탈예측모델",
        "description": "고객의 카드 이탈(해지) 가능성을 예측하는 분류 모델. 최근 거래 패턴, 이용 빈도 변화, 민원 이력 등을 기반으로 이탈 위험도를 스코어링한다.",
        "type": "Classification",
        "algorithm": "XGBoost",
        "model_id": "MDL_CHURN",
    },
    "cross_sell": {
        "name": "교차판매모델",
        "description": "기존 고객에게 추가 카드 상품을 판매할 가능성을 예측하는 모델. 고객의 소비 패턴과 보유 상품을 분석하여 교차판매 잠재력을 스코어링한다.",
        "type": "Classification",
        "algorithm": "LightGBM",
        "model_id": "MDL_XSELL",
    },
    "credit_scoring": {
        "name": "신용스코어링모델",
        "description": "고객의 신용 위험도를 평가하는 모델. 거래 이력, 연체 여부, 신용 이용률 등을 종합하여 내부 신용 스코어를 산출한다.",
        "type": "Regression",
        "algorithm": "Logistic Regression",
        "model_id": "MDL_CREDIT",
    },
    "customer_segmentation": {
        "name": "고객세그멘테이션",
        "description": "고객을 소비 행동 기반으로 세그먼트로 분류하는 군집화 모델. premium_traveler, smart_shopper, vip_spender, budget_conscious, dormant 등으로 분류한다.",
        "type": "Clustering",
        "algorithm": "K-Means",
        "model_id": "MDL_SEG",
    },
    "response_prediction": {
        "name": "응답예측모델",
        "description": "마케팅 캠페인 발송 시 고객의 응답(오픈/클릭/전환) 확률을 예측하는 모델. 과거 캠페인 반응 이력과 고객 특성을 기반으로 응답 가능성을 스코어링한다.",
        "type": "Classification",
        "algorithm": "Random Forest",
        "model_id": "MDL_RESP",
    },
}

# 용어사전 그룹 정의
GLOSSARY_NODES = {
    "고객": "고객 관련 비즈니스 용어",
    "거래": "카드 거래 관련 비즈니스 용어",
    "피처": "AI 모델 입력 피처 관련 용어",
    "모델": "AI/ML 모델 관련 용어",
    "캠페인": "마케팅 캠페인 관련 용어",
}

# 용어사전 상세 정의
GLOSSARY_TERMS = {
    "고객ID": {"group": "고객", "definition": "고객을 식별하는 고유 번호. 시스템 전반에서 고객을 참조하는 키 값이다."},
    "신용등급": {"group": "고객", "definition": "외부 신용평가기관(CB)의 등급 또는 내부 산출 등급. 1등급(최우수)부터 10등급(최하위)까지 분류된다."},
    "연소득": {"group": "고객", "definition": "고객이 신고한 연간 총소득. 한도 산정 및 상품 추천에 활용된다."},
    "활성여부": {"group": "고객", "definition": "고객 계정의 활성 상태. 최근 6개월 내 거래 또는 로그인 이력이 있으면 활성으로 판단한다."},
    "거래금액": {"group": "거래", "definition": "개별 카드 결제 건의 승인 금액(원화 환산). 해외거래의 경우 결제일 환율 적용 금액이다."},
    "업종코드": {"group": "거래", "definition": "가맹점의 업종 분류 코드(MCC). 항공, 호텔, 백화점, 주유 등 표준 분류 체계를 따른다."},
    "할부거래": {"group": "거래", "definition": "거래금액을 2개월 이상에 걸쳐 분할 납부하는 거래 방식."},
    "해외거래": {"group": "거래", "definition": "해외 가맹점에서 발생한 결제 거래. 원화 외 통화로 결제된 건을 의미한다."},
    "월평균이용금액": {"group": "피처", "definition": "최근 N개월간 총 이용금액을 월수로 나눈 평균값. 고객의 소비 수준을 나타내는 핵심 지표이다."},
    "이용건수": {"group": "피처", "definition": "특정 기간 내 카드 결제 총 건수. 이용 활성도를 측정하는 기본 지표이다."},
    "해외이용비율": {"group": "피처", "definition": "전체 이용금액 대비 해외거래 이용금액의 비율. 글로벌 소비 성향을 측정한다."},
    "한도이용률": {"group": "피처", "definition": "승인된 신용한도 대비 실제 이용 잔액의 비율. 신용 위험도 판단의 핵심 지표이다."},
    "AUC": {"group": "모델", "definition": "Area Under the ROC Curve. 분류 모델의 판별력을 0~1 사이 값으로 나타내는 성능 지표."},
    "예측스코어": {"group": "모델", "definition": "AI 모델이 산출한 0~1 사이의 확률값. 이벤트(이탈, 구매, 응답 등) 발생 가능성을 나타낸다."},
    "세그먼트": {"group": "모델", "definition": "고객을 유사 특성 그룹으로 분류한 결과 라벨. 세그멘테이션 모델의 출력이다."},
    "전환율": {"group": "캠페인", "definition": "캠페인 타겟 대비 실제 목표 행동(구매, 가입 등)을 수행한 고객의 비율."},
    "ROI": {"group": "캠페인", "definition": "Return on Investment. 캠페인 투입 비용 대비 발생 수익의 비율."},
    "Lift": {"group": "캠페인", "definition": "대조군(Control Group) 대비 실험군(Treatment Group)의 성과 향상 비율. 캠페인 순수 효과를 측정한다."},
    "타겟세그먼트": {"group": "캠페인", "definition": "캠페인 발송 대상으로 선정된 고객 세그먼트. AI 모델 스코어 기반으로 선정된다."},
    "대조군": {"group": "캠페인", "definition": "캠페인 효과 측정을 위해 의도적으로 캠페인을 발송하지 않는 비교 집단."},
}

# 로깅 설정
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("datahub-marketing")
