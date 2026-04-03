-- ============================================================
-- 피처/집계 레이어 (Feature Layer)
-- 고객 거래 데이터를 기반으로 가공된 AI 모델 입력 피처
-- ============================================================

-- 고객 피처 테이블 (AI 모델 입력용)
CREATE TABLE customer_features (
    customer_id         VARCHAR(20)     NOT NULL REFERENCES customer(customer_id),
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
);

-- ============================================================
-- 샘플 데이터 (기준일: 2026-03-01)
-- ============================================================

INSERT INTO customer_features VALUES
('CUST001', '2026-03-01', 4455500.00, 1485166.67, 4, '항공',      0.0000, 0.5000, 7, 1, 0.4200, 0),
('CUST002', '2026-03-01', 311600.00,  103866.67,  3, '온라인쇼핑', 0.0000, 0.3333, 15, 2, 0.1800, 0),
('CUST003', '2026-03-01', 4930000.00, 1643333.33, 4, '백화점',     0.2500, 0.2500, 4, 1, 0.3500, 0),
('CUST004', '2026-03-01', 43250.00,   14416.67,   2, '드럭스토어', 0.0000, 0.0000, 40, 2, 0.0800, 0),
('CUST005', '2026-03-01', 75000.00,   25000.00,   1, '주유',       0.0000, 0.0000, 58, 1, 0.0500, 1),
('CUST006', '2026-03-01', 609000.00,  203000.00,  2, '해외온라인', 1.0000, 0.0000, 9, 1, 0.2200, 0),
('CUST007', '2026-03-01', 65000.00,   21666.67,   1, '주유',       0.0000, 0.0000, 48, 1, 0.0900, 0),
('CUST008', '2026-03-01', 17000.00,   5666.67,    1, '온라인구독', 0.0000, 0.0000, 46, 1, 0.0300, 0),
('CUST009', '2026-03-01', 6880000.00, 2293333.33, 4, '백화점',     0.0000, 0.5000, 4, 2, 0.2800, 0),
('CUST010', '2026-03-01', 3200.00,    1066.67,    1, '편의점',     0.0000, 0.0000, 51, 1, 0.0100, 0);
