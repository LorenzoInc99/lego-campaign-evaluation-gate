#!/usr/bin/env bash
# Build LEGO_Case_Study_Report.pdf (run from repo root or this directory).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
if ! command -v pdflatex >/dev/null 2>&1; then
  echo "pdflatex not found. Install MacTeX/TeX Live/MiKTeX, or use Overleaf with LEGO_Case_Study_Report.tex"
  exit 1
fi
pdflatex -interaction=nonstopmode LEGO_Case_Study_Report.tex
pdflatex -interaction=nonstopmode LEGO_Case_Study_Report.tex
echo "OK: $DIR/LEGO_Case_Study_Report.pdf"
