# LaTeX reports (PDF)

## Files

| Source | Contents |
|--------|----------|
| `LEGO_Case_Study_Report.tex` | Formal case study: diagrams, role-aligned keywords, tables |
| `Project_Development_Report.tex` | **Narrative:** what was built and why, development (needs / in place / gaps), tests & examples, results |

Both are **single-file** projects (no extra `.sty`). Compiler: **pdfLaTeX**.

## Compile locally

Requires TeX Live / MacTeX / MiKTeX with `pdflatex`.

```bash
cd report
./build_pdf.sh
```

Build only one file:

```bash
./build_pdf.sh Project_Development_Report.tex
```

Manual:

```bash
pdflatex -interaction=nonstopmode Project_Development_Report.tex
pdflatex -interaction=nonstopmode Project_Development_Report.tex
```

Outputs: `LEGO_Case_Study_Report.pdf`, `Project_Development_Report.pdf`

## Overleaf

Upload `LEGO_Case_Study_Report.tex` and/or `Project_Development_Report.tex` from `report/` (or use the **`overleaf/`** folder copies). Set compiler to **pdfLaTeX**. See `overleaf/README.txt`.

## Case study keywords (`LEGO_Case_Study_Report.tex`)

Highlighted terms (`\JD{...}`) map to Analytics Engineering themes: evaluation frameworks, LLM outputs, observability, governance, quality gates, regression, Python, SQL, REST API, lifecycle, campaign optimisation, CI/CD, Databricks (as future work), etc.
