#!/bin/bash
# DataHub에 메타데이터를 등록하는 스크립트
# Usage: ./scripts/ingest_metadata.sh [GMS_URL]

set -e

GMS_URL="${1:-http://localhost:8080}"
export DATAHUB_GMS_URL="$GMS_URL"
export DATAHUB_TOKEN=""

echo "=== DataHub 메타데이터 등록 ==="
echo "GMS URL: $GMS_URL"
echo ""

# GMS 헬스체크 대기
echo "DataHub GMS 서버 대기 중..."
for i in $(seq 1 60); do
    if curl -s "$GMS_URL/health" | grep -q "UP"; then
        echo "GMS 서버 준비 완료!"
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "ERROR: GMS 서버가 60초 내에 시작되지 않았습니다."
        exit 1
    fi
    sleep 2
done

echo ""
echo "메타데이터 등록 시작..."
cd "$(dirname "$0")/.."
python3 -m src.run_all

echo ""
echo "=== 등록 완료 ==="
echo "DataHub UI: http://localhost:9002"
echo "로그인: datahub / datahub"
