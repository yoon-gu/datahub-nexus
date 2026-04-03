#!/bin/bash
# =============================================================
# DataHub 신용카드 마케팅 플랫폼 - 원클릭 배포 스크립트
#
# 사용법:
#   curl -sSL <이 스크립트 URL> | bash
#   또는
#   git clone <repo> && cd datahub-nexus && bash scripts/deploy.sh
#
# 사전 요구사항:
#   - Docker + Docker Compose
#   - Python 3.9+
#   - pip install acryl-datahub python-dotenv
#
# 포트:
#   - 9002: DataHub UI (브라우저 접속)
#   - 8080: DataHub GMS API
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=============================================="
echo "  DataHub 마케팅 플랫폼 배포"
echo "=============================================="
echo ""

# 1. 의존성 확인
echo "[1/5] 의존성 확인..."
command -v docker >/dev/null 2>&1 || { echo "ERROR: docker가 필요합니다."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3가 필요합니다."; exit 1; }

# pip 패키지 확인/설치
python3 -c "import datahub" 2>/dev/null || {
    echo "acryl-datahub 설치 중..."
    pip install -q acryl-datahub python-dotenv
}

echo "  Docker: $(docker --version | head -1)"
echo "  Python: $(python3 --version)"
echo "  DataHub CLI: $(datahub version 2>/dev/null | head -1 || echo 'N/A')"
echo ""

# 2. DataHub 시작
echo "[2/5] DataHub 시작 중 (첫 실행 시 5~10분 소요)..."
if command -v datahub >/dev/null 2>&1; then
    datahub docker quickstart
else
    echo "datahub CLI가 없습니다. pip install acryl-datahub 후 다시 시도하세요."
    exit 1
fi
echo ""

# 3. GMS 대기
echo "[3/5] GMS 서버 준비 대기..."
GMS_URL="http://localhost:8080"
for i in $(seq 1 60); do
    if curl -s "$GMS_URL/health" 2>/dev/null | grep -q "UP"; then
        echo "  GMS 준비 완료!"
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "ERROR: GMS 서버가 시작되지 않았습니다."
        echo "  docker logs datahub-datahub-gms-quickstart-1 으로 로그를 확인하세요."
        exit 1
    fi
    sleep 3
done
echo ""

# 4. 메타데이터 등록
echo "[4/5] 메타데이터 등록 중..."
export DATAHUB_GMS_URL="$GMS_URL"
export DATAHUB_TOKEN=""
python3 -m src.run_all
echo ""

# 5. 완료
HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
echo "=============================================="
echo "  배포 완료!"
echo "=============================================="
echo ""
echo "  DataHub UI:  http://${HOST_IP}:9002"
echo "  로그인:       datahub / datahub"
echo "  GMS API:     http://${HOST_IP}:8080"
echo ""
echo "  등록된 메타데이터:"
echo "    - 데이터셋 10개 (고객, 거래, 카드상품, 피처, 모델, 캠페인)"
echo "    - 도메인 4개 (Customer, Marketing, Risk, Analytics)"
echo "    - 태그 7개 (PII, Financial, ML_Feature 등)"
echo "    - 용어사전 20개 비즈니스 용어"
echo "    - 리니지 5개 (원천 → 피처 → 스코어 → 타겟 → 성과)"
echo "    - ML 모델 5개 (이탈, 교차판매, 신용, 세그먼테이션, 응답)"
echo ""
echo "  외부 접속 시 방화벽에서 포트 9002, 8080을 열어주세요."
echo ""
echo "  종료: datahub docker quickstart --stop"
echo "=============================================="
