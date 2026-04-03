# datahub-nexus

신용카드 데이터 드리븐 마케팅 플랫폼을 위한 DataHub 메타데이터 관리 프로젝트입니다.

## 개요

신용카드회사의 데이터 레이크를 합성(SQL DDL + 샘플 데이터)하고, DataHub에 메타데이터를 등록하여
**원천 데이터 → 피처 가공 → AI 모델 스코어링 → 캠페인 타겟팅 → 성과 관리** 전체 흐름을 추적합니다.

### 핵심 기능

- **데이터셋 등록**: 10개 테이블 (고객, 거래, 카드상품, 피처, 모델스코어, 캠페인 등)
- **도메인 분류**: Customer, Marketing, Risk, Analytics 4개 도메인
- **태그 관리**: PII, Financial, ML_Feature, ML_Output, KPI, Realtime, Daily_Batch
- **용어사전**: 5개 그룹, 21개 비즈니스 용어
- **데이터 리니지**: 원천 → 피처 → 모델스코어 → 캠페인타겟 → 성과 전체 흐름
- **ML 모델 메타데이터**: 이탈예측, 교차판매, 신용스코어링, 고객세그멘테이션, 응답예측 5개 모델

## 프로젝트 구조

```
datahub-nexus/
├── sql/                              # 합성 데이터 레이크 (DDL + 샘플 데이터)
│   ├── 01_raw_tables.sql             #   원천 데이터 (고객, 카드상품, 거래)
│   ├── 02_feature_tables.sql         #   피처 테이블 (고객 피처)
│   ├── 03_model_tables.sql           #   모델 레이어 (모델 메타, 스코어)
│   └── 04_campaign_tables.sql        #   캠페인 레이어 (캠페인, 타겟, 응답, 성과)
├── src/                              # DataHub 메타데이터 등록 코드
│   ├── config.py                     #   공통 설정 및 상수
│   ├── register_domains.py           #   도메인 등록
│   ├── register_tags.py              #   태그 등록
│   ├── register_glossary.py          #   용어사전 등록
│   ├── register_datasets.py          #   데이터셋 등록 (스키마, 태그, 용어 연결)
│   ├── register_lineage.py           #   데이터 리니지 등록
│   ├── register_ml_models.py         #   ML 모델 메타데이터 등록
│   └── run_all.py                    #   전체 등록 실행 스크립트
├── tests/                            # 단위 테스트
├── requirements.txt
└── README.md
```

## 데이터 흐름 (Lineage)

```
[customer] ──────┐
[transaction] ───┤──→ [customer_features] ──→ [model_scores] ──→ [campaign_target]
[card_product] ──┘                                                      │
                                                                        ▼
                        [campaign] ──────────────────────→ [campaign_response]
                            │                                           │
                            └──────────────────────────→ [campaign_performance]
```

## AI 모델

| 모델 | 유형 | 알고리즘 | 용도 |
|------|------|----------|------|
| 이탈예측 | Classification | XGBoost | 고객 이탈 위험 스코어링 |
| 교차판매 | Classification | LightGBM | 추가 상품 판매 잠재력 |
| 신용스코어링 | Regression | Logistic Regression | 내부 신용 위험 평가 |
| 고객세그멘테이션 | Clustering | K-Means | 소비 행동 기반 분류 |
| 응답예측 | Classification | Random Forest | 캠페인 응답 확률 예측 |

## 시작하기

### 사전 요구사항

- Python 3.9+
- DataHub 인스턴스 (로컬 또는 원격)

### 설치

```bash
pip install -r requirements.txt
```

### 환경 변수 설정

```bash
export DATAHUB_GMS_URL=http://localhost:8080
export DATAHUB_TOKEN=<your-token>
```

### 실행

```bash
# 전체 메타데이터 등록
python -m src.run_all

# 개별 등록
python -c "from src.register_domains import register_domains; ..."
```

### 테스트

```bash
pytest tests/ -v
```

## 참고 자료

- [DataHub 공식 문서](https://datahubproject.io/docs/)
- [DataHub Python SDK](https://datahubproject.io/docs/metadata-ingestion/)
