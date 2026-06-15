# SBERT Model Decision Matrix & Recommendation
**Project:** AI-Powered Resume Ranking System
**Date:** June 15, 2026
**Author:** ResearchAgent

## 1. Candidate Models Evaluated

We evaluated the three candidate Sentence-BERT (SBERT) models for semantic matching of resumes to job descriptions:

1. **`all-MiniLM-L6-v2`**
2. **`all-mpnet-base-v2`**
3. **`paraphrase-multilingual-MiniLM-L12-v2`**

---

## 2. Evaluation Matrix

| Metric | `all-MiniLM-L6-v2` | `all-mpnet-base-v2` | `paraphrase-multilingual-MiniLM-L12-v2` |
| :--- | :--- | :--- | :--- |
| **Model Size** | ~90 MB | ~420 MB | ~220 MB |
| **Dimensionality** | 384 dimensions | 768 dimensions | 384 dimensions |
| **Parameters** | ~15 Million | ~110 Million | ~30 Million |
| **Speed (CPU / GPU)**| **Fastest** (3x-5x faster than MPNet) | Slowest | Moderate |
| **Accuracy (English)**| Very High (slightly lower than MPNet) | **Highest** (MTEB leader in class) | Moderate-High (biased to paraphrase) |
| **Multilingual Support**| English-only focused | English-only focused | **Excellent** (supports 50+ languages) |
| **HuggingFace Usability**| Out-of-the-box (single line load) | Out-of-the-box (single line load) | Out-of-the-box (single line load) |

---

## 3. Detailed Assessment

### A. Speed & Efficiency
- **`all-MiniLM-L6-v2`** is the clear winner for low-resource environments (e.g., standard developer machines, CPUs, or low-cost Docker hosting). It has a footprint of only ~90MB, making initialization and inference extremely fast.
- **`all-mpnet-base-v2`** is a larger model (~420MB). On CPU-only environments, this model will introduce noticeable latency (typically 3-5 seconds to encode multiple resumes compared to less than 1 second for MiniLM).

### B. Matching Accuracy
- **`all-mpnet-base-v2`** is the gold standard for English sentence embeddings. It captures complex semantic concepts and syntactic dependencies slightly better than the distilled MiniLM, which is valuable when parsing long resumes with complex phrasing.
- **`all-MiniLM-L6-v2`** is highly optimized and captures ~95% of the quality of the larger MPNet model on standard semantic similarity benchmarks, which is more than sufficient for resume-to-job matching.

### C. Language Capabilities
- **`paraphrase-multilingual-MiniLM-L12-v2`** is only recommended if the system must handle resumes and job descriptions written in languages other than English (e.g., Spanish, French, German, Dutch). For English-only applications, its embeddings are less dense/optimized than the `all-*` series.

---

## 4. Final Recommendation: **`all-MiniLM-L6-v2`**

For the **AI-Powered Resume Ranking System**, we recommend starting with **`all-MiniLM-L6-v2`** as the default model.

### Rationale:
1. **Low Latency / CPU Friendly:** Since the application runs in a local environment or Docker containers without dedicated GPU resource guarantees, `all-MiniLM-L6-v2` offers near-instant CPU processing times.
2. **Minimal Memory Footprint:** At only ~90MB, it minimizes memory usage when running concurrently with spaCy models (NER) and FastAPI.
3. **High Return on Investment:** It captures the bulk of the semantic matching quality of larger models with a fraction of the computational cost.

*Alternative path:* If the client/developer requires maximum matching accuracy and can guarantee GPU support in deployment, **`all-mpnet-base-v2`** should be configured as a toggleable option in the config file.
