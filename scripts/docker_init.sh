#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "data/raw/BankChurners.csv" ]]; then
  echo "Missing data/raw/BankChurners.csv. Download the Kaggle dataset first."
  exit 1
fi

docker compose up -d postgres
docker compose up -d --build backend

docker compose run --rm backend python scripts/seed_database.py --input ../data/raw/BankChurners.csv
docker compose run --rm backend python scripts/train_model.py --input ../data/raw/BankChurners.csv --artifacts ../data/artifacts

docker compose up -d --build frontend

echo ""
echo "Dashboard: http://127.0.0.1:5173"
echo "API docs:  http://127.0.0.1:8000/docs"
