# Phase 2 Completion Report
**Project:** AI-Powered Resume Ranking System
**Status:** Completed

We have successfully completed Phase 2 (Backend Core and NLP Pipeline). We set up the FastAPI router infrastructure, configured project environment variables, implemented document ingestion, preprocessing pipelines, and NER extraction. All 20 unit tests are passing successfully.

---

## 1. Created Files & Structure

The following files were created or updated in this phase:

```text
d:\VU Internship Project
├── backend/
│   ├── config.py                  # Configurations (Alpha, SBERT models, upload limits)
│   ├── main.py                    # FastAPI main entrypoint and model cache loader
│   ├── api/
│   │   └── routes/
│   │       ├── __init__.py        # Router routing registrations
│   │       ├── export.py          # Placeholder export router
│   │       ├── rank.py            # Placeholder rank router
│   │       └── results.py         # Placeholder results router
│   ├── modules/
│   │   ├── ingestion.py           # Module 1 (PDF & DOCX parsing + validation)
│   │   ├── preprocessing.py       # Module 2 (spaCy NLP text normalisation)
│   │   └── ner.py                 # Module 3 (Information extraction - skills, experience)
│   └── tests/
│       ├── fixtures/              # Created valid/invalid resume fixtures for tests
│       │   ├── corrupt.pdf
│       │   ├── unsupported.png
│       │   ├── valid_resume.docx
│       │   └── valid_resume.pdf
│       ├── test_ingestion.py      # Unit tests for Ingestion module
│       ├── test_preprocessing.py  # Unit tests for Preprocessing module
│       └── test_ner.py            # Unit tests for NER module
```

---

## 2. Module Function Signatures

### Module 1: Document Ingestion (`backend/modules/ingestion.py`)
* `extract_text_from_pdf(file_path: str) -> str`
  * Extracts plain text from PDF files using PyMuPDF (`fitz`).
* `extract_text_from_docx(file_path: str) -> str`
  * Extracts plain text from DOCX documents and tables using `python-docx`.
* `validate_file(file: UploadFile) -> bool`
  * Validates file format (only `.pdf` and `.docx`), sizes ($\leq 5$ MB), and checks that the file is not empty.
* `save_upload(file: UploadFile, upload_dir: str) -> str`
  * Persists uploaded files to disk.
* `process_uploads(files: list[UploadFile], upload_dir: str) -> list[dict]`
  * Batch entry point that handles multiple files and processes failures gracefully.

### Module 2: NLP Preprocessing (`backend/modules/preprocessing.py`)
* `load_nlp_model() -> Language`
  * Singleton loader for spaCy `en_core_web_sm`.
* `clean_text(text: str) -> str`
  * Normalises case, strips special characters (retaining alphanumeric), and normalises whitespace.
* `tokenise(text: str) -> list[str]`
  * Splits text into tokenized string items.
* `remove_stopwords(tokens: list[str]) -> list[str]`
  * Filters standard English stopwords.
* `lemmatise(tokens: list[str]) -> list[str]`
  * Normalises tokens to their base forms (lemmas).
* `preprocess(text: str) -> dict`
  * Single pipeline wrapper returning `{raw, cleaned, tokens, lemmas}`.

### Module 3: NER Extraction (`backend/modules/ner.py`)
* `extract_entities(text: str) -> dict`
  * Identifies skill keywords, education institutions/degrees, and calculates years of experience from plain text.
* `extract_jd_requirements(jd_text: str) -> dict`
  * Runs the extraction logic specifically on job description text.

---

## 3. Unit Test Results Summary

We ran 20 tests spanning ingestion, preprocessing, and NER modules. All tests passed.

```text
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.0, pluggy-1.6.0
rootdir: D:\VU Internship Project\backend
configfile: pyproject.toml
plugins: anyio-4.13.0
collected 20 items

backend\tests\test_ingestion.py ........                                 [ 40%]
backend\tests\test_ner.py ......                                         [ 70%]
backend\tests\test_preprocessing.py ......                               [100%]

============================= 20 passed in 13.87s =============================
```

### Edge Cases Handled:
1. **Oversized & Empty Files:** Mocked `UploadFile` size calculations to reject files larger than 5MB or containing 0 bytes.
2. **Corrupt Files:** Created custom corrupt fixtures, asserting extraction processes crash cleanly or return failure keys instead of breaking.
3. **Special Character Boundaries:** Formulated regex rules for skill keyword matches (e.g. `c++`, `next.js`) so that characters like `+` or dots are captured without matching unrelated substrings.

---

## 4. Phase 3 Readiness Checklist

Before proceeding to Phase 3 (Scoring Engine):
- [x] FastAPI skeleton runs correctly.
- [x] Preprocessing and entity parsing returns normalized keywords.
- [x] Pinned virtual environment set up and operational.
- [x] Version control commit and push protocol executed.

> [!NOTE]
> **Orchestrator Status:** Phase 2 complete. Ready to begin Phase 3 once developer instructs.
