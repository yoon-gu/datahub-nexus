# datahub-nexus

DataHub POC(Proof of Concept) 프로젝트입니다.

## 목적

DataHub의 핵심 기능을 검증하고, 실제 데이터 파이프라인 환경에 통합하기 위한 PoC입니다.

### 주요 검증 항목

- DataHub REST API / GraphQL API 연동
- 메타데이터 수집 및 등록 (Ingestion)
- 데이터 계보(Lineage) 추적
- 태그, 용어집, 도메인 등 메타데이터 관리
- Python SDK (`acryl-datahub`) 활용

## 프로젝트 구조

```
datahub-nexus/
├── src/                  # 소스 코드
│   └── ...
├── tests/                # 테스트 코드
│   └── ...
├── requirements.txt      # Python 의존성
└── README.md
```

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

## 참고 자료

- [DataHub 공식 문서](https://datahubproject.io/docs/)
- [DataHub Python SDK](https://datahubproject.io/docs/metadata-ingestion/)
