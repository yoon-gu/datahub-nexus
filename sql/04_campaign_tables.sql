-- ============================================================
-- 캠페인 레이어 (Campaign Layer)
-- 마케팅 캠페인 관리, 타겟팅, 응답, 성과
-- ============================================================

-- 캠페인 마스터
CREATE TABLE campaign (
    campaign_id     VARCHAR(30)     PRIMARY KEY,
    campaign_name   VARCHAR(100)    NOT NULL,
    campaign_type   VARCHAR(30)     NOT NULL CHECK (campaign_type IN ('cross_sell', 'retention', 'activation', 'upsell', 'winback')),
    channel         VARCHAR(30)     NOT NULL CHECK (channel IN ('SMS', 'PUSH', 'EMAIL', 'APP', 'LMS')),
    start_date      DATE            NOT NULL,
    end_date        DATE            NOT NULL,
    target_model_id VARCHAR(30)     REFERENCES model_metadata(model_id),
    target_segment  VARCHAR(20),
    offer_description VARCHAR(200),
    budget          DECIMAL(15,2)   NOT NULL DEFAULT 0,
    status          VARCHAR(20)     NOT NULL DEFAULT 'planned'
);

-- 캠페인 타겟 고객
CREATE TABLE campaign_target (
    campaign_id     VARCHAR(30)     NOT NULL REFERENCES campaign(campaign_id),
    customer_id     VARCHAR(20)     NOT NULL REFERENCES customer(customer_id),
    model_score     DECIMAL(7,4),
    target_rank     INT,
    is_control_group BOOLEAN        NOT NULL DEFAULT FALSE,
    sent_date       TIMESTAMP,
    PRIMARY KEY (campaign_id, customer_id)
);

-- 캠페인 응답
CREATE TABLE campaign_response (
    campaign_id         VARCHAR(30)     NOT NULL REFERENCES campaign(campaign_id),
    customer_id         VARCHAR(20)     NOT NULL REFERENCES customer(customer_id),
    response_type       VARCHAR(20)     NOT NULL CHECK (response_type IN ('open', 'click', 'convert')),
    response_date       TIMESTAMP       NOT NULL,
    conversion_amount   DECIMAL(15,2)   DEFAULT 0
);

-- 캠페인 성과 집계
CREATE TABLE campaign_performance (
    campaign_id     VARCHAR(30)     PRIMARY KEY REFERENCES campaign(campaign_id),
    total_target    INT             NOT NULL DEFAULT 0,
    total_sent      INT             NOT NULL DEFAULT 0,
    total_open      INT             NOT NULL DEFAULT 0,
    total_click     INT             NOT NULL DEFAULT 0,
    total_conversion INT            NOT NULL DEFAULT 0,
    conversion_rate DECIMAL(5,4)    NOT NULL DEFAULT 0,
    total_revenue   DECIMAL(15,2)   NOT NULL DEFAULT 0,
    roi             DECIMAL(7,4)    NOT NULL DEFAULT 0,
    lift            DECIMAL(7,4)    NOT NULL DEFAULT 0
);

-- ============================================================
-- 샘플 데이터
-- ============================================================

INSERT INTO campaign VALUES
('CMP_2026_001', '프리미엄카드 교차판매 3월', 'cross_sell', 'EMAIL', '2026-03-01', '2026-03-31', 'MDL_XSELL', 'high_potential', '여행 시그니처 카드 연회비 첫해 면제', 5000000.00, 'completed'),
('CMP_2026_002', '이탈위험 고객 리텐션', 'retention', 'SMS', '2026-03-05', '2026-03-20', 'MDL_CHURN', 'high_risk', '포인트 2배 적립 이벤트 + 연회비 할인', 3000000.00, 'completed'),
('CMP_2026_003', '휴면고객 활성화', 'winback', 'PUSH', '2026-03-10', '2026-03-31', 'MDL_CHURN', 'dormant', '첫 이용 시 캐시백 50,000원', 2000000.00, 'active'),
('CMP_2026_004', 'VIP 업셀 캠페인', 'upsell', 'APP', '2026-03-15', '2026-04-15', 'MDL_SEG', 'vip_spender', '블랙카드 업그레이드 특별 오퍼', 8000000.00, 'active'),
('CMP_2026_005', '디지털 전환 캠페인', 'activation', 'LMS', '2026-03-20', '2026-04-20', 'MDL_RESP', 'very_likely', '앱 결제 시 추가 1% 적립', 1500000.00, 'planned');

INSERT INTO campaign_target VALUES
('CMP_2026_001', 'CUST001', 0.7800, 1, FALSE, '2026-03-01 09:00:00'),
('CMP_2026_001', 'CUST006', 0.8500, 2, FALSE, '2026-03-01 09:00:00'),
('CMP_2026_001', 'CUST002', 0.6200, 3, FALSE, '2026-03-01 09:00:00'),
('CMP_2026_001', 'CUST004', 0.4500, 4, TRUE,  '2026-03-01 09:00:00'),
('CMP_2026_002', 'CUST005', 0.8900, 1, FALSE, '2026-03-05 10:00:00'),
('CMP_2026_002', 'CUST010', 0.8100, 2, FALSE, '2026-03-05 10:00:00'),
('CMP_2026_002', 'CUST008', 0.7200, 3, FALSE, '2026-03-05 10:00:00'),
('CMP_2026_002', 'CUST007', 0.6700, 4, TRUE,  '2026-03-05 10:00:00'),
('CMP_2026_003', 'CUST005', 0.8900, 1, FALSE, '2026-03-10 11:00:00'),
('CMP_2026_003', 'CUST007', 0.6700, 2, FALSE, '2026-03-10 11:00:00'),
('CMP_2026_004', 'CUST003', 0.0000, 1, FALSE, '2026-03-15 09:00:00'),
('CMP_2026_004', 'CUST009', 0.0000, 2, FALSE, '2026-03-15 09:00:00');

INSERT INTO campaign_response VALUES
('CMP_2026_001', 'CUST001', 'open',    '2026-03-01 14:20:00', 0),
('CMP_2026_001', 'CUST001', 'click',   '2026-03-01 14:22:00', 0),
('CMP_2026_001', 'CUST001', 'convert', '2026-03-05 10:30:00', 150000.00),
('CMP_2026_001', 'CUST006', 'open',    '2026-03-01 11:15:00', 0),
('CMP_2026_001', 'CUST006', 'click',   '2026-03-01 11:18:00', 0),
('CMP_2026_001', 'CUST006', 'convert', '2026-03-03 16:00:00', 150000.00),
('CMP_2026_001', 'CUST002', 'open',    '2026-03-02 09:30:00', 0),
('CMP_2026_002', 'CUST005', 'open',    '2026-03-05 12:00:00', 0),
('CMP_2026_002', 'CUST005', 'click',   '2026-03-05 12:05:00', 0),
('CMP_2026_002', 'CUST010', 'open',    '2026-03-06 08:30:00', 0),
('CMP_2026_002', 'CUST008', 'open',    '2026-03-05 15:45:00', 0),
('CMP_2026_002', 'CUST008', 'click',   '2026-03-05 15:48:00', 0),
('CMP_2026_002', 'CUST008', 'convert', '2026-03-08 14:00:00', 42000.00),
('CMP_2026_003', 'CUST005', 'open',    '2026-03-10 14:30:00', 0),
('CMP_2026_004', 'CUST003', 'open',    '2026-03-15 10:00:00', 0),
('CMP_2026_004', 'CUST003', 'click',   '2026-03-15 10:05:00', 0);

INSERT INTO campaign_performance VALUES
('CMP_2026_001', 4, 4, 3, 2, 2, 0.5000, 300000.00, 0.0600, 1.8500),
('CMP_2026_002', 4, 4, 3, 2, 1, 0.2500, 42000.00,  0.0140, 1.4200);
