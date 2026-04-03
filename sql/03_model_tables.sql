-- ============================================================
-- 모델 스코어/메타데이터 레이어 (Model Layer)
-- AI 모델 관리 정보 및 예측 스코어
-- ============================================================

-- 모델 관리 정보
CREATE TABLE model_metadata (
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

-- 모델 예측 스코어
CREATE TABLE model_scores (
    customer_id     VARCHAR(20)     NOT NULL REFERENCES customer(customer_id),
    score_date      DATE            NOT NULL,
    model_id        VARCHAR(30)     NOT NULL REFERENCES model_metadata(model_id),
    model_version   VARCHAR(10)     NOT NULL,
    score           DECIMAL(7,4)    NOT NULL,
    segment         VARCHAR(20),
    rank_percentile DECIMAL(5,2),
    PRIMARY KEY (customer_id, score_date, model_id)
);

-- ============================================================
-- 샘플 데이터
-- ============================================================

INSERT INTO model_metadata VALUES
('MDL_CHURN',    '이탈예측모델',       'Classification', 'XGBoost',            'is_churned',    '2026-02-15', 0.8720, 0.8150, 0.7830, 12, 'active'),
('MDL_XSELL',   '교차판매모델',       'Classification', 'LightGBM',           'will_purchase', '2026-02-20', 0.8450, 0.7920, 0.7560, 12, 'active'),
('MDL_CREDIT',  '신용스코어링모델',   'Regression',     'Logistic Regression', 'credit_score',  '2026-01-10', 0.9010, 0.8670, 0.8340, 10, 'active'),
('MDL_SEG',     '고객세그멘테이션',   'Clustering',     'K-Means',            'segment_label', '2026-02-01', NULL,   NULL,   NULL,   12, 'active'),
('MDL_RESP',    '응답예측모델',       'Classification', 'Random Forest',       'will_respond',  '2026-02-25', 0.8130, 0.7680, 0.7410, 11, 'active');

-- 이탈예측 스코어 (score가 높을수록 이탈 위험 높음)
INSERT INTO model_scores VALUES
('CUST001', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.1200, 'low_risk',     12.00),
('CUST002', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.2350, 'low_risk',     23.50),
('CUST003', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.0800, 'low_risk',     8.00),
('CUST004', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.5600, 'medium_risk',  56.00),
('CUST005', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.8900, 'high_risk',    89.00),
('CUST006', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.1800, 'low_risk',     18.00),
('CUST007', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.6700, 'medium_risk',  67.00),
('CUST008', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.7200, 'high_risk',    72.00),
('CUST009', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.0500, 'low_risk',     5.00),
('CUST010', '2026-03-01', 'MDL_CHURN', 'v2.1', 0.8100, 'high_risk',    81.00);

-- 교차판매 스코어 (프리미엄 카드 교차판매 대상)
INSERT INTO model_scores VALUES
('CUST001', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.7800, 'high_potential', 78.00),
('CUST002', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.6200, 'medium_potential', 62.00),
('CUST003', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.3100, 'low_potential', 31.00),
('CUST004', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.4500, 'medium_potential', 45.00),
('CUST005', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.1500, 'low_potential', 15.00),
('CUST006', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.8500, 'high_potential', 85.00),
('CUST009', '2026-03-01', 'MDL_XSELL', 'v1.3', 0.2000, 'low_potential', 20.00);

-- 응답예측 스코어
INSERT INTO model_scores VALUES
('CUST001', '2026-03-01', 'MDL_RESP', 'v1.0', 0.6500, 'likely',     65.00),
('CUST002', '2026-03-01', 'MDL_RESP', 'v1.0', 0.7200, 'likely',     72.00),
('CUST003', '2026-03-01', 'MDL_RESP', 'v1.0', 0.4800, 'neutral',    48.00),
('CUST004', '2026-03-01', 'MDL_RESP', 'v1.0', 0.8100, 'very_likely', 81.00),
('CUST006', '2026-03-01', 'MDL_RESP', 'v1.0', 0.9200, 'very_likely', 92.00),
('CUST009', '2026-03-01', 'MDL_RESP', 'v1.0', 0.3500, 'unlikely',   35.00),
('CUST010', '2026-03-01', 'MDL_RESP', 'v1.0', 0.5500, 'neutral',    55.00);

-- 고객 세그멘테이션 결과
INSERT INTO model_scores VALUES
('CUST001', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'premium_traveler', NULL),
('CUST002', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'smart_shopper',    NULL),
('CUST003', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'vip_spender',      NULL),
('CUST004', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'budget_conscious', NULL),
('CUST005', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'dormant',          NULL),
('CUST006', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'global_shopper',   NULL),
('CUST007', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'dormant',          NULL),
('CUST008', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'digital_native',   NULL),
('CUST009', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'vip_spender',      NULL),
('CUST010', '2026-03-01', 'MDL_SEG', 'v3.0', 0.0000, 'budget_conscious', NULL);
