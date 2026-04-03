-- ============================================================
-- 원천 데이터 레이어 (Raw Data Layer)
-- 신용카드 마케팅 플랫폼 - 고객, 카드상품, 거래 데이터
-- ============================================================

-- 고객 프로필
CREATE TABLE customer (
    customer_id     VARCHAR(20)     PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    birth_date      DATE            NOT NULL,
    gender          CHAR(1)         NOT NULL CHECK (gender IN ('M', 'F')),
    phone           VARCHAR(20),
    email           VARCHAR(100),
    address         VARCHAR(200),
    registration_date DATE          NOT NULL,
    credit_grade    VARCHAR(10)     NOT NULL,
    annual_income   DECIMAL(15,2),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE
);

-- 카드 상품
CREATE TABLE card_product (
    product_id      VARCHAR(20)     PRIMARY KEY,
    product_name    VARCHAR(100)    NOT NULL,
    card_type       VARCHAR(20)     NOT NULL CHECK (card_type IN ('CREDIT', 'CHECK')),
    annual_fee      DECIMAL(10,2)   NOT NULL DEFAULT 0,
    benefit_category VARCHAR(50)    NOT NULL,
    reward_rate     DECIMAL(5,2)    NOT NULL DEFAULT 0,
    launch_date     DATE            NOT NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE
);

-- 카드 거래
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
);

-- ============================================================
-- 샘플 데이터
-- ============================================================

INSERT INTO customer VALUES
('CUST001', '김민수', '1985-03-15', 'M', '010-1234-5678', 'minsu.kim@email.com', '서울시 강남구 역삼동 123', '2018-01-10', '1등급', 85000000.00, TRUE),
('CUST002', '이서연', '1990-07-22', 'F', '010-2345-6789', 'seoyeon.lee@email.com', '서울시 서초구 반포동 456', '2019-05-20', '2등급', 62000000.00, TRUE),
('CUST003', '박지훈', '1978-11-08', 'M', '010-3456-7890', 'jihoon.park@email.com', '경기도 성남시 분당구 정자동 789', '2017-03-01', '1등급', 120000000.00, TRUE),
('CUST004', '최유진', '1995-02-14', 'F', '010-4567-8901', 'yujin.choi@email.com', '서울시 마포구 합정동 101', '2021-08-15', '3등급', 38000000.00, TRUE),
('CUST005', '정태현', '1982-09-30', 'M', '010-5678-9012', 'taehyun.jung@email.com', '부산시 해운대구 우동 202', '2016-11-25', '2등급', 72000000.00, FALSE),
('CUST006', '한소희', '1992-04-18', 'F', '010-6789-0123', 'sohee.han@email.com', '서울시 송파구 잠실동 303', '2020-02-28', '2등급', 55000000.00, TRUE),
('CUST007', '윤성민', '1988-12-05', 'M', '010-7890-1234', 'sungmin.yoon@email.com', '인천시 연수구 송도동 404', '2019-07-10', '3등급', 45000000.00, TRUE),
('CUST008', '강예린', '1993-06-25', 'F', '010-8901-2345', 'yerin.kang@email.com', '대전시 유성구 봉명동 505', '2022-01-05', '4등급', 32000000.00, TRUE),
('CUST009', '송준혁', '1975-01-20', 'M', '010-9012-3456', 'junhyuk.song@email.com', '서울시 강동구 천호동 606', '2015-06-30', '1등급', 150000000.00, TRUE),
('CUST010', '임수빈', '1998-08-12', 'F', '010-0123-4567', 'subin.lim@email.com', '경기도 용인시 수지구 707', '2023-03-20', '4등급', 28000000.00, TRUE);

INSERT INTO card_product VALUES
('PROD001', '프리미엄 플래티넘', 'CREDIT', 300000.00, '항공마일리지', 1.50, '2020-01-15', TRUE),
('PROD002', '캐시백 골드', 'CREDIT', 50000.00, '캐시백', 1.00, '2019-06-01', TRUE),
('PROD003', '쇼핑 리워드', 'CREDIT', 30000.00, '쇼핑할인', 2.00, '2021-03-10', TRUE),
('PROD004', '비즈니스 블랙', 'CREDIT', 500000.00, '라운지/호텔', 2.50, '2018-09-01', TRUE),
('PROD005', '일상 체크', 'CHECK', 0.00, '교통/통신', 0.50, '2022-01-01', TRUE),
('PROD006', '여행 시그니처', 'CREDIT', 150000.00, '해외결제', 3.00, '2021-07-20', TRUE),
('PROD007', '주유 할인', 'CREDIT', 20000.00, '주유할인', 1.20, '2020-05-15', TRUE),
('PROD008', '디지털 라이프', 'CREDIT', 10000.00, '온라인구독', 1.80, '2023-02-01', TRUE);

INSERT INTO transaction VALUES
('TXN20260101001', 'CUST001', 'PROD001', '2026-01-05 14:30:00', '대한항공', '항공', 1250000.00, TRUE, 3, FALSE),
('TXN20260101002', 'CUST001', 'PROD001', '2026-01-10 09:15:00', '스타벅스 역삼점', '카페', 5500.00, FALSE, 0, FALSE),
('TXN20260101003', 'CUST002', 'PROD002', '2026-01-08 18:45:00', '이마트 반포점', '대형마트', 87600.00, FALSE, 0, FALSE),
('TXN20260101004', 'CUST002', 'PROD003', '2026-01-12 11:20:00', '무신사', '온라인쇼핑', 156000.00, TRUE, 6, FALSE),
('TXN20260101005', 'CUST003', 'PROD004', '2026-01-03 20:00:00', 'Marriott Tokyo', '호텔', 450000.00, FALSE, 0, TRUE),
('TXN20260101006', 'CUST003', 'PROD004', '2026-01-15 13:00:00', '현대백화점 판교점', '백화점', 2300000.00, TRUE, 12, FALSE),
('TXN20260101007', 'CUST004', 'PROD005', '2026-01-07 08:30:00', '서울교통공사', '교통', 1250.00, FALSE, 0, FALSE),
('TXN20260101008', 'CUST004', 'PROD003', '2026-01-20 16:40:00', '올리브영 합정점', '드럭스토어', 42000.00, FALSE, 0, FALSE),
('TXN20260101009', 'CUST005', 'PROD002', '2026-01-02 12:10:00', 'GS칼텍스 해운대', '주유', 75000.00, FALSE, 0, FALSE),
('TXN20260101010', 'CUST006', 'PROD006', '2026-01-18 10:30:00', 'Amazon.com', '해외온라인', 89000.00, FALSE, 0, TRUE),
('TXN20260101011', 'CUST007', 'PROD007', '2026-01-11 07:45:00', 'SK에너지 송도', '주유', 65000.00, FALSE, 0, FALSE),
('TXN20260101012', 'CUST008', 'PROD008', '2026-01-14 22:15:00', 'Netflix', '온라인구독', 17000.00, FALSE, 0, FALSE),
('TXN20260101013', 'CUST009', 'PROD004', '2026-01-06 19:30:00', '정식당', '고급식당', 580000.00, FALSE, 0, FALSE),
('TXN20260101014', 'CUST009', 'PROD001', '2026-01-22 15:00:00', '루이비통 청담', '명품', 4500000.00, TRUE, 6, FALSE),
('TXN20260101015', 'CUST010', 'PROD005', '2026-01-09 13:20:00', 'CU 수지점', '편의점', 3200.00, FALSE, 0, FALSE),
('TXN20260102001', 'CUST001', 'PROD001', '2026-02-03 10:00:00', '하나투어', '여행', 3200000.00, TRUE, 6, FALSE),
('TXN20260102002', 'CUST002', 'PROD002', '2026-02-14 19:30:00', '빕스 서초점', '패밀리레스토랑', 68000.00, FALSE, 0, FALSE),
('TXN20260102003', 'CUST003', 'PROD004', '2026-02-10 11:00:00', 'Hilton Singapore', '호텔', 380000.00, FALSE, 0, TRUE),
('TXN20260102004', 'CUST006', 'PROD006', '2026-02-20 09:00:00', 'Booking.com', '해외온라인', 520000.00, FALSE, 0, TRUE),
('TXN20260102005', 'CUST009', 'PROD004', '2026-02-25 18:00:00', '갤러리아 압구정', '백화점', 1800000.00, TRUE, 3, FALSE);
