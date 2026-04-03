"""신용카드 데이터 드리븐 마케팅 플랫폼 - DataHub 메타데이터 대시보드."""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# 데이터 정의
# ============================================================

DATASETS = {
    "raw": [
        {"table": "customer", "rows": "10M", "columns": 11, "description": "고객 프로필 마스터", "update": "Daily"},
        {"table": "card_product", "rows": "50", "columns": 8, "description": "카드 상품 마스터", "update": "Daily"},
        {"table": "transaction", "rows": "500M", "columns": 10, "description": "카드 거래 내역", "update": "Realtime"},
    ],
    "feature": [
        {"table": "customer_features", "rows": "10M", "columns": 12, "description": "AI 모델 입력 피처", "update": "Daily Batch"},
    ],
    "model": [
        {"table": "model_metadata", "rows": "5", "columns": 11, "description": "AI 모델 관리 정보", "update": "On Train"},
        {"table": "model_scores", "rows": "50M", "columns": 7, "description": "모델 예측 스코어", "update": "Daily Batch"},
    ],
    "campaign": [
        {"table": "campaign", "rows": "1K", "columns": 11, "description": "캠페인 마스터", "update": "Daily"},
        {"table": "campaign_target", "rows": "5M", "columns": 6, "description": "캠페인 타겟 고객", "update": "Per Campaign"},
        {"table": "campaign_response", "rows": "2M", "columns": 5, "description": "캠페인 응답", "update": "Realtime"},
        {"table": "campaign_performance", "rows": "1K", "columns": 10, "description": "캠페인 성과 집계", "update": "Daily Batch"},
    ],
}

ML_MODELS = [
    {"model": "이탈예측모델", "id": "MDL_CHURN", "type": "Classification", "algorithm": "XGBoost", "auc": 0.872, "precision": 0.815, "recall": 0.783, "status": "Active"},
    {"model": "교차판매모델", "id": "MDL_XSELL", "type": "Classification", "algorithm": "LightGBM", "auc": 0.845, "precision": 0.792, "recall": 0.756, "status": "Active"},
    {"model": "신용스코어링모델", "id": "MDL_CREDIT", "type": "Regression", "algorithm": "Logistic Regression", "auc": 0.901, "precision": 0.867, "recall": 0.834, "status": "Active"},
    {"model": "고객세그멘테이션", "id": "MDL_SEG", "type": "Clustering", "algorithm": "K-Means", "auc": None, "precision": None, "recall": None, "status": "Active"},
    {"model": "응답예측모델", "id": "MDL_RESP", "type": "Classification", "algorithm": "Random Forest", "auc": 0.813, "precision": 0.768, "recall": 0.741, "status": "Active"},
]

DOMAINS = [
    {"domain": "Customer", "description": "고객 관련 데이터 (고객 프로필, 카드 상품, 거래)", "datasets": 3},
    {"domain": "Marketing", "description": "캠페인 관련 데이터 (캠페인, 타겟, 응답, 성과)", "datasets": 4},
    {"domain": "Risk", "description": "리스크 및 신용 관리 데이터", "datasets": 0},
    {"domain": "Analytics", "description": "분석/ML 관련 데이터 (피처, 스코어, 모델 메타)", "datasets": 3},
]

TAGS = [
    {"tag": "PII", "description": "개인식별정보", "count": 5, "color": "#e74c3c"},
    {"tag": "Financial", "description": "금융 정보", "count": 8, "color": "#f39c12"},
    {"tag": "ML_Feature", "description": "ML 모델 입력 피처", "count": 9, "color": "#3498db"},
    {"tag": "ML_Output", "description": "ML 모델 출력", "count": 3, "color": "#9b59b6"},
    {"tag": "KPI", "description": "핵심 성과 지표", "count": 5, "color": "#2ecc71"},
    {"tag": "Realtime", "description": "실시간 처리", "count": 2, "color": "#e67e22"},
    {"tag": "Daily_Batch", "description": "일배치 처리", "count": 7, "color": "#1abc9c"},
]

GLOSSARY = [
    {"term": "고객ID", "group": "고객", "definition": "고객을 식별하는 고유 번호"},
    {"term": "신용등급", "group": "고객", "definition": "1등급(최우수)~10등급(최하위) 분류"},
    {"term": "연소득", "group": "고객", "definition": "고객이 신고한 연간 총소득"},
    {"term": "활성여부", "group": "고객", "definition": "최근 6개월 내 거래/로그인 여부"},
    {"term": "거래금액", "group": "거래", "definition": "개별 카드 결제 승인 금액"},
    {"term": "업종코드", "group": "거래", "definition": "가맹점 업종 분류 코드(MCC)"},
    {"term": "할부거래", "group": "거래", "definition": "2개월 이상 분할 납부 거래"},
    {"term": "해외거래", "group": "거래", "definition": "해외 가맹점 결제 거래"},
    {"term": "월평균이용금액", "group": "피처", "definition": "최근 N개월 총 이용금액의 월평균"},
    {"term": "이용건수", "group": "피처", "definition": "특정 기간 내 카드 결제 총 건수"},
    {"term": "해외이용비율", "group": "피처", "definition": "전체 이용금액 대비 해외거래 비율"},
    {"term": "한도이용률", "group": "피처", "definition": "신용한도 대비 이용 잔액 비율"},
    {"term": "AUC", "group": "모델", "definition": "분류 모델 판별력 (0~1)"},
    {"term": "예측스코어", "group": "모델", "definition": "AI 모델이 산출한 확률값 (0~1)"},
    {"term": "세그먼트", "group": "모델", "definition": "고객 유사 특성 그룹 분류 라벨"},
    {"term": "전환율", "group": "캠페인", "definition": "타겟 대비 목표 행동 수행 비율"},
    {"term": "ROI", "group": "캠페인", "definition": "투입 비용 대비 발생 수익 비율"},
    {"term": "Lift", "group": "캠페인", "definition": "대조군 대비 성과 향상 비율"},
    {"term": "타겟세그먼트", "group": "캠페인", "definition": "AI 모델 기반 캠페인 발송 대상 그룹"},
    {"term": "대조군", "group": "캠페인", "definition": "캠페인 미발송 비교 집단"},
]

CAMPAIGNS = [
    {"campaign": "프리미엄카드 교차판매 3월", "type": "cross_sell", "channel": "EMAIL", "model": "MDL_XSELL", "target": 4, "conversion": 2, "rate": 0.50, "revenue": 300000, "roi": 0.06, "lift": 1.85},
    {"campaign": "이탈위험 고객 리텐션", "type": "retention", "channel": "SMS", "model": "MDL_CHURN", "target": 4, "conversion": 1, "rate": 0.25, "revenue": 42000, "roi": 0.014, "lift": 1.42},
    {"campaign": "휴면고객 활성화", "type": "winback", "channel": "PUSH", "model": "MDL_CHURN", "target": 2, "conversion": 0, "rate": 0.0, "revenue": 0, "roi": 0.0, "lift": 0.0},
    {"campaign": "VIP 업셀 캠페인", "type": "upsell", "channel": "APP", "model": "MDL_SEG", "target": 2, "conversion": 0, "rate": 0.0, "revenue": 0, "roi": 0.0, "lift": 0.0},
    {"campaign": "디지털 전환 캠페인", "type": "activation", "channel": "LMS", "model": "MDL_RESP", "target": 0, "conversion": 0, "rate": 0.0, "revenue": 0, "roi": 0.0, "lift": 0.0},
]

CUSTOMER_SCORES = [
    {"id": "CUST001", "name": "김민수", "segment": "premium_traveler", "churn": 0.12, "xsell": 0.78, "response": 0.65},
    {"id": "CUST002", "name": "이서연", "segment": "smart_shopper", "churn": 0.24, "xsell": 0.62, "response": 0.72},
    {"id": "CUST003", "name": "박지훈", "segment": "vip_spender", "churn": 0.08, "xsell": 0.31, "response": 0.48},
    {"id": "CUST004", "name": "최유진", "segment": "budget_conscious", "churn": 0.56, "xsell": 0.45, "response": 0.81},
    {"id": "CUST005", "name": "정태현", "segment": "dormant", "churn": 0.89, "xsell": 0.15, "response": None},
    {"id": "CUST006", "name": "한소희", "segment": "global_shopper", "churn": 0.18, "xsell": 0.85, "response": 0.92},
    {"id": "CUST007", "name": "윤성민", "segment": "dormant", "churn": 0.67, "xsell": None, "response": None},
    {"id": "CUST008", "name": "강예린", "segment": "digital_native", "churn": 0.72, "xsell": None, "response": None},
    {"id": "CUST009", "name": "송준혁", "segment": "vip_spender", "churn": 0.05, "xsell": 0.20, "response": 0.35},
    {"id": "CUST010", "name": "임수빈", "segment": "budget_conscious", "churn": 0.81, "xsell": None, "response": 0.55},
]


# ============================================================
# 시각화 함수
# ============================================================

def create_lineage_diagram():
    """데이터 리니지 Sankey 다이어그램."""
    labels = [
        "customer", "card_product", "transaction",  # 0, 1, 2
        "customer_features",  # 3
        "model_scores",  # 4
        "campaign", # 5
        "campaign_target",  # 6
        "campaign_response",  # 7
        "campaign_performance",  # 8
        "model_metadata",  # 9
    ]
    colors = [
        "#3498db", "#3498db", "#3498db",  # raw - blue
        "#e67e22",  # feature - orange
        "#9b59b6",  # model scores - purple
        "#2ecc71",  # campaign - green
        "#2ecc71", "#2ecc71", "#2ecc71",  # campaign - green
        "#9b59b6",  # model metadata - purple
    ]

    source = [0, 1, 2, 3, 9, 4, 5, 6, 7, 5]
    target = [3, 3, 3, 4, 4, 6, 6, 7, 8, 8]
    value =  [3, 1, 5, 4, 1, 3, 2, 2, 2, 1]

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="white", width=1),
            label=labels,
            color=colors,
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(150,150,150,0.3)",
        ),
    ))
    fig.update_layout(
        title_text="Data Lineage: 원천 → 피처 → 모델 → 캠페인 → 성과",
        font_size=13,
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def create_model_performance_chart():
    """ML 모델 성능 비교 차트."""
    models_with_metrics = [m for m in ML_MODELS if m["auc"] is not None]
    df = pd.DataFrame(models_with_metrics)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="AUC", x=df["model"], y=df["auc"], marker_color="#3498db"))
    fig.add_trace(go.Bar(name="Precision", x=df["model"], y=df["precision"], marker_color="#2ecc71"))
    fig.add_trace(go.Bar(name="Recall", x=df["model"], y=df["recall"], marker_color="#e67e22"))

    fig.update_layout(
        title="AI 모델 성능 비교",
        barmode="group",
        yaxis_title="Score",
        yaxis_range=[0.6, 1.0],
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_campaign_chart():
    """캠페인 성과 차트."""
    active = [c for c in CAMPAIGNS if c["target"] > 0]
    df = pd.DataFrame(active)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="타겟 수", x=df["campaign"], y=df["target"],
        marker_color="#3498db",
    ))
    fig.add_trace(go.Bar(
        name="전환 수", x=df["campaign"], y=df["conversion"],
        marker_color="#2ecc71",
    ))

    fig.update_layout(
        title="캠페인 성과 (타겟 vs 전환)",
        barmode="group",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_segment_distribution():
    """고객 세그먼트 분포 차트."""
    segments = [c["segment"] for c in CUSTOMER_SCORES]
    segment_counts = pd.Series(segments).value_counts()

    colors = {
        "premium_traveler": "#3498db",
        "smart_shopper": "#2ecc71",
        "vip_spender": "#9b59b6",
        "budget_conscious": "#e67e22",
        "dormant": "#e74c3c",
        "global_shopper": "#1abc9c",
        "digital_native": "#f39c12",
    }

    fig = go.Figure(go.Pie(
        labels=segment_counts.index,
        values=segment_counts.values,
        marker=dict(colors=[colors.get(s, "#95a5a6") for s in segment_counts.index]),
        hole=0.4,
        textinfo="label+percent",
    ))
    fig.update_layout(
        title="고객 세그먼트 분포",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def create_churn_risk_chart():
    """고객별 이탈 위험도 차트."""
    df = pd.DataFrame(CUSTOMER_SCORES)

    colors = ["#2ecc71" if s < 0.3 else "#f39c12" if s < 0.6 else "#e74c3c" for s in df["churn"]]

    fig = go.Figure(go.Bar(
        x=df["name"],
        y=df["churn"],
        marker_color=colors,
        text=[f"{s:.0%}" for s in df["churn"]],
        textposition="outside",
    ))
    fig.update_layout(
        title="고객별 이탈 위험 스코어",
        yaxis_title="이탈 확률",
        yaxis_range=[0, 1.1],
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def create_tag_distribution():
    """태그별 컬럼 분포 차트."""
    df = pd.DataFrame(TAGS)
    fig = go.Figure(go.Bar(
        x=df["tag"],
        y=df["count"],
        marker_color=df["color"],
        text=df["count"],
        textposition="outside",
    ))
    fig.update_layout(
        title="태그별 적용 컬럼 수",
        yaxis_title="컬럼 수",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


# ============================================================
# Gradio UI
# ============================================================

HEADER_MD = """
# 신용카드 데이터 드리븐 마케팅 플랫폼

**DataHub 메타데이터 대시보드** | 데이터 → AI 모델 → 캠페인 타겟팅 → 성과 관리

---
"""

OVERVIEW_MD = """
### 플랫폼 구성 요약

| 구성 요소 | 수량 | 설명 |
|-----------|------|------|
| **데이터셋** | 10개 | 고객, 거래, 상품, 피처, 모델스코어, 캠페인 |
| **도메인** | 4개 | Customer, Marketing, Risk, Analytics |
| **태그** | 7개 | PII, Financial, ML_Feature, ML_Output, KPI 등 |
| **용어사전** | 20개 | 5개 그룹 (고객/거래/피처/모델/캠페인) |
| **리니지** | 5개 | 원천 → 피처 → 스코어 → 타겟 → 성과 |
| **AI 모델** | 5개 | 이탈예측, 교차판매, 신용스코어링, 세그멘테이션, 응답예측 |
"""


def build_app():
    with gr.Blocks(
        title="신용카드 마케팅 플랫폼 DataHub",
    ) as app:
        gr.Markdown(HEADER_MD)

        with gr.Tab("Overview"):
            gr.Markdown(OVERVIEW_MD)
            with gr.Row():
                gr.Plot(create_lineage_diagram)

        with gr.Tab("Data Lake"):
            for layer_name, layer_label in [("raw", "Raw Layer (원천)"), ("feature", "Feature Layer (피처)"), ("model", "Model Layer (모델)"), ("campaign", "Campaign Layer (캠페인)")]:
                gr.Markdown(f"#### {layer_label}")
                df = pd.DataFrame(DATASETS[layer_name])
                gr.Dataframe(df, label=None, interactive=False)

        with gr.Tab("AI Models"):
            with gr.Row():
                gr.Plot(create_model_performance_chart)
            gr.Markdown("#### 모델 상세 정보")
            model_df = pd.DataFrame(ML_MODELS)
            gr.Dataframe(model_df, label=None, interactive=False)

        with gr.Tab("Scores & Segments"):
            with gr.Row():
                with gr.Column():
                    gr.Plot(create_churn_risk_chart)
                with gr.Column():
                    gr.Plot(create_segment_distribution)
            gr.Markdown("#### 고객별 스코어 상세")
            score_df = pd.DataFrame(CUSTOMER_SCORES)
            gr.Dataframe(score_df, label=None, interactive=False)

        with gr.Tab("Campaigns"):
            with gr.Row():
                gr.Plot(create_campaign_chart)
            gr.Markdown("#### 캠페인 상세")
            campaign_df = pd.DataFrame(CAMPAIGNS)
            gr.Dataframe(campaign_df, label=None, interactive=False)

        with gr.Tab("Governance"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Domains")
                    domain_df = pd.DataFrame(DOMAINS)
                    gr.Dataframe(domain_df, label=None, interactive=False)
                with gr.Column():
                    gr.Plot(create_tag_distribution)

            gr.Markdown("#### Glossary (용어사전)")
            glossary_df = pd.DataFrame(GLOSSARY)
            gr.Dataframe(glossary_df, label=None, interactive=False)

        with gr.Tab("Schema"):
            gr.Markdown("#### 테이블 스키마 (SQL DDL)")
            gr.Markdown("원천 데이터, 피처, 모델, 캠페인 레이어의 DDL을 확인할 수 있습니다.")

            with gr.Accordion("01. Raw Tables (고객, 카드상품, 거래)", open=False):
                gr.Code(
                    label="01_raw_tables.sql",
                    language="sql",
                    value="""CREATE TABLE customer (
    customer_id     VARCHAR(20)     PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    birth_date      DATE            NOT NULL,
    gender          CHAR(1)         NOT NULL,
    phone           VARCHAR(20),
    email           VARCHAR(100),
    address         VARCHAR(200),
    registration_date DATE          NOT NULL,
    credit_grade    VARCHAR(10)     NOT NULL,
    annual_income   DECIMAL(15,2),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE
);

CREATE TABLE card_product (
    product_id      VARCHAR(20)     PRIMARY KEY,
    product_name    VARCHAR(100)    NOT NULL,
    card_type       VARCHAR(20)     NOT NULL,
    annual_fee      DECIMAL(10,2)   NOT NULL DEFAULT 0,
    benefit_category VARCHAR(50)    NOT NULL,
    reward_rate     DECIMAL(5,2)    NOT NULL DEFAULT 0,
    launch_date     DATE            NOT NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE
);

CREATE TABLE transaction (
    transaction_id      VARCHAR(30)     PRIMARY KEY,
    customer_id         VARCHAR(20)     NOT NULL REFERENCES customer(customer_id),
    product_id          VARCHAR(20)     NOT NULL REFERENCES card_product(product_id),
    transaction_date    TIMESTAMP       NOT NULL,
    merchant_name       VARCHAR(100)    NOT NULL,
    merchant_category   VARCHAR(50)     NOT NULL,
    amount              DECIMAL(15,2)   NOT NULL,
    is_installment      BOOLEAN         NOT NULL DEFAULT FALSE,
    installment_months  INT             DEFAULT 0,
    is_overseas         BOOLEAN         NOT NULL DEFAULT FALSE
);""",
                )
            with gr.Accordion("02. Feature Tables (고객 피처)", open=False):
                gr.Code(
                    label="02_feature_tables.sql",
                    language="sql",
                    value="""CREATE TABLE customer_features (
    customer_id         VARCHAR(20)     NOT NULL,
    feature_date        DATE            NOT NULL,
    total_spend_3m      DECIMAL(15,2)   NOT NULL DEFAULT 0,
    avg_spend_monthly   DECIMAL(15,2)   NOT NULL DEFAULT 0,
    transaction_count_3m INT            NOT NULL DEFAULT 0,
    top_merchant_category VARCHAR(50),
    overseas_ratio      DECIMAL(5,4)    NOT NULL DEFAULT 0,
    installment_ratio   DECIMAL(5,4)    NOT NULL DEFAULT 0,
    days_since_last_txn INT             NOT NULL DEFAULT 0,
    active_cards_count  INT             NOT NULL DEFAULT 0,
    credit_utilization  DECIMAL(5,4)    NOT NULL DEFAULT 0,
    complaint_count_6m  INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (customer_id, feature_date)
);""",
                )
            with gr.Accordion("03. Model Tables (모델 메타/스코어)", open=False):
                gr.Code(
                    label="03_model_tables.sql",
                    language="sql",
                    value="""CREATE TABLE model_metadata (
    model_id        VARCHAR(30)     PRIMARY KEY,
    model_name      VARCHAR(100)    NOT NULL,
    model_type      VARCHAR(50)     NOT NULL,
    algorithm       VARCHAR(50)     NOT NULL,
    target_variable VARCHAR(50)     NOT NULL,
    train_date      DATE            NOT NULL,
    auc_score       DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall_score    DECIMAL(5,4),
    feature_count   INT             NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'active'
);

CREATE TABLE model_scores (
    customer_id     VARCHAR(20)     NOT NULL,
    score_date      DATE            NOT NULL,
    model_id        VARCHAR(30)     NOT NULL,
    model_version   VARCHAR(10)     NOT NULL,
    score           DECIMAL(7,4)    NOT NULL,
    segment         VARCHAR(20),
    rank_percentile DECIMAL(5,2),
    PRIMARY KEY (customer_id, score_date, model_id)
);""",
                )
            with gr.Accordion("04. Campaign Tables (캠페인/성과)", open=False):
                gr.Code(
                    label="04_campaign_tables.sql",
                    language="sql",
                    value="""CREATE TABLE campaign (
    campaign_id     VARCHAR(30)     PRIMARY KEY,
    campaign_name   VARCHAR(100)    NOT NULL,
    campaign_type   VARCHAR(30)     NOT NULL,
    channel         VARCHAR(30)     NOT NULL,
    start_date      DATE            NOT NULL,
    end_date        DATE            NOT NULL,
    target_model_id VARCHAR(30),
    target_segment  VARCHAR(20),
    offer_description VARCHAR(200),
    budget          DECIMAL(15,2)   NOT NULL DEFAULT 0,
    status          VARCHAR(20)     NOT NULL DEFAULT 'planned'
);

CREATE TABLE campaign_target (
    campaign_id     VARCHAR(30)     NOT NULL,
    customer_id     VARCHAR(20)     NOT NULL,
    model_score     DECIMAL(7,4),
    target_rank     INT,
    is_control_group BOOLEAN        NOT NULL DEFAULT FALSE,
    sent_date       TIMESTAMP,
    PRIMARY KEY (campaign_id, customer_id)
);

CREATE TABLE campaign_response (
    campaign_id         VARCHAR(30)     NOT NULL,
    customer_id         VARCHAR(20)     NOT NULL,
    response_type       VARCHAR(20)     NOT NULL,
    response_date       TIMESTAMP       NOT NULL,
    conversion_amount   DECIMAL(15,2)   DEFAULT 0
);

CREATE TABLE campaign_performance (
    campaign_id     VARCHAR(30)     PRIMARY KEY,
    total_target    INT             NOT NULL DEFAULT 0,
    total_sent      INT             NOT NULL DEFAULT 0,
    total_open      INT             NOT NULL DEFAULT 0,
    total_click     INT             NOT NULL DEFAULT 0,
    total_conversion INT            NOT NULL DEFAULT 0,
    conversion_rate DECIMAL(5,4)    NOT NULL DEFAULT 0,
    total_revenue   DECIMAL(15,2)   NOT NULL DEFAULT 0,
    roi             DECIMAL(7,4)    NOT NULL DEFAULT 0,
    lift            DECIMAL(7,4)    NOT NULL DEFAULT 0
);""",
                )

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
