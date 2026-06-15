# Phase 3 Completion Report
**Project:** AI-Powered Resume Ranking System
**Status:** Completed

We have successfully completed Phase 3 (Scoring Engine). We developed lexical similarity modules using TF-IDF, semantic similarity modules using Sentence-BERT, a hybrid scoring combiner, and a candidate ranking and keyword gap analysis module. We verified the pipeline against 5 synthetic candidate resumes, performed a sensitivity analysis on the weighting parameter $\alpha$, and ran all 26 unit tests successfully.

---

## 1. Created Files & Structure

The following files were created in this phase:

```text
d:\VU Internship Project
├── backend/
│   ├── modules/
│   │   ├── tfidf_scorer.py       # Module 4A: TF-IDF lexical matching
│   │   ├── sbert_scorer.py       # Module 4B: Sentence-BERT semantic matching
│   │   ├── hybrid_scorer.py      # Module 4C: Hybrid scoring combiner
│   │   └── ranking.py            # Module 5: Sort/Rank + Keyword Gap Analysis
│   └── tests/
│       └── test_scoring.py       # Unit tests for Phase 3 scoring engines
├── scripts/
│   ├── generate_test_data.py     # Script to build synthetic test resumes & JD
│   └── run_validation.py         # Script to run validation and output MD report
└── test_data/
    ├── jd.txt                    # Job Description text file
    ├── resumes/                  # 5 synthetic resume PDF files (resume_1.pdf -> resume_5.pdf)
    └── scoring_validation.md     # Generated validation scores & alpha sensitivity report
```

---

## 2. Validation Outputs

We ran the validation script on the 5 synthetic resumes vs. the Python/ML Job Description. The scores generated at the default weight of $\alpha = 0.3$ (30% TF-IDF, 70% SBERT) are:

| Rank | Filename | TF-IDF Score | SBERT Score | Final Score | Experience | Skills Matched |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | `resume_1.pdf` (Strong Match) | 0.3964 | 0.7480 | **0.6425** | 6 yrs | aws, deep learning, docker, fastapi, git, machine learning, python, pytorch, sql |
| **2** | `resume_2.pdf` (Good Match) | 0.2844 | 0.6869 | **0.5662** | 4 yrs | css, django, docker, git, html, machine learning, postgresql, python, sql |
| **3** | `resume_3.pdf` (Partial Match) | 0.1116 | 0.5634 | **0.4279** | 2 yrs | css, git, html, javascript, python, sql, sqlite |
| **4** | `resume_4.pdf` (Weak Match) | 0.1033 | 0.5578 | **0.4215** | 1 yr | c++, git, java, spring boot, sql |
| **5** | `resume_5.pdf` (Non-Match) | 0.0576 | 0.3414 | **0.2563** | 5 yrs (Sales) | *(None)* |

**Validation Status:** **PASSED ✅** (The actual rank order exactly matched the expected ordering of `1 > 2 > 3 > 4 > 5`).

### Final Confirmed $\alpha$ Weight:
* **$\alpha = 0.3$** (lexical weight of 30%, semantic SBERT weight of 70%) is confirmed. Sensitivity analysis shows that this weight achieves robust candidate ordering and successfully balances specific keyword requirements with conceptual semantic relevance.

---

## 3. Unit Test Pass Summary

We implemented 6 new test cases in `backend/tests/test_scoring.py` covering score boundaries, mathematical correctness of the hybrid combiner, descending ranking sorting, keyword gaps, and empty resume inputs. 

All 26 unit tests in the project now pass successfully:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.0, pluggy-1.6.0
collected 26 items

backend\tests\test_ingestion.py ........                                 [ 30%]
backend\tests\test_ner.py ......                                         [ 53%]
backend\tests\test_preprocessing.py ......                               [ 76%]
backend\tests\test_scoring.py ......                                     [100%]

============================= 26 passed in 45.97s =============================
```

---

## 4. Phase 4 Readiness Checklist

Before proceeding to Phase 4 (Database Integration & API Endpoints):
- [x] Ingestion, preprocessing, scoring, and ranking modules completed.
- [x] SBERT models load successfully and run CPU inference within 45s.
- [x] All 26 unit tests pass.
- [x] Version control commit and push protocol executed.
