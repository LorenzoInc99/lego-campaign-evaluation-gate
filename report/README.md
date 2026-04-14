# LaTeX case study report

## File

- `LEGO_Case_Study_Report.tex` — full report with TikZ process diagrams and job-keyword highlighting (`\JD{...}`).

## Compile locally

Requires a LaTeX distribution (TeX Live, MacTeX, MiKTeX) with `pdflatex` and TikZ.

```bash
cd report
./build_pdf.sh
```

Or manually:

```bash
cd report
pdflatex -interaction=nonstopmode LEGO_Case_Study_Report.tex
pdflatex -interaction=nonstopmode LEGO_Case_Study_Report.tex
```

Or:

```bash
latexmk -pdf LEGO_Case_Study_Report.tex
```

Output: `LEGO_Case_Study_Report.pdf`

## Overleaf

Use the ready-made folder **`overleaf/`** in this directory: it contains `LEGO_Case_Study_Report.tex` plus `README.txt` with upload steps. Zip **`report/overleaf`** and upload the zip to Overleaf, or upload that folder’s contents.

Alternatively, upload only `LEGO_Case_Study_Report.tex` from the `report/` folder (single-file project; no separate `.sty` needed). Compiler: **pdfLaTeX**.

## Keywords

Highlighted terms map to the Analytics Engineer posting: evaluation frameworks, LLM/agent outputs, observability, governance, quality gates, regression, Python, SQL, REST API, lifecycle, Data Office, Digital Product, campaign optimisation, CI/CD, Databricks (as future work), etc.
