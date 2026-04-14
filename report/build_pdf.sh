#!/usr/bin/env bash
# Build LaTeX PDFs in this directory (run from repo root or this directory).
# Usage: ./build_pdf.sh              # builds both default reports
#        ./build_pdf.sh MyFile.tex   # builds only listed .tex files
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
if ! command -v pdflatex >/dev/null 2>&1; then
  echo "pdflatex not found. Install MacTeX/TeX Live/MiKTeX, or use Overleaf."
  exit 1
fi

if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  FILES=(LEGO_Case_Study_Report.tex Project_Development_Report.tex)
fi

for tex in "${FILES[@]}"; do
  if [[ ! -f "$tex" ]]; then
    echo "Skip (not found): $tex"
    continue
  fi
  base="${tex%.tex}"
  pdflatex -interaction=nonstopmode "$tex"
  pdflatex -interaction=nonstopmode "$tex"
  echo "OK: $DIR/${base}.pdf"
done
