# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Build
The project uses LaTeX to generate a PDF document. The main file is `Pietro_Gasparini_Informatica_2025-2026.tex`.

- **Build with latexmk (recommended):**
  ```bash
  latexmk -pdf "Pietro_Gasparini_Informatica_2025-2026.tex"
  ```
- **Build with pdflatex and bibtex:**
  ```bash
  pdflatex "Pietro_Gasparini_Informatica_2025-2026.tex"
  bibtex "Pietro_Gasparini_Informatica_2025-2026.aux"
  pdflatex "Pietro_Gasparini_Informatica_2025-2026.tex"
  pdflatex "Pietro_Gasparini_Informatica_2025-2026.tex"
  ```
- **Clean build files:**
  ```bash
  latexmk -C
  ```

## Architecture and Structure

This is a LaTeX project for a university thesis.

### Document Structure
- **Main File:** `Pietro_Gasparini_Informatica_2025-2026.tex` - The entry point that defines the document class, packages, and includes all other sections.
- **Chapters:** Located in `capitolo1.tex` through `capitolo4.tex`.
- **Front/Back Matter:**
  - `pagina_iniziale.tex`: Title page and initial information.
  - `ringraziamenti.tex`: Acknowledgements.
  - `sommario.tex`: Abstract/Summary.
  - `allegati.tex`: Appendices.
- **Bibliography:** `biblio.bib` - Contains all bibliographic references.

### Data and Statistics
The `statistiche/` directory contains experimental results and reports used in the thesis:
- Subdirectories for different models (e.g., `gpt-4o_report`, `codestral_22b_report`) contain CSV files with correlations and status data.
- `statistiche/databases_report/` contains a summary of database-related results.
