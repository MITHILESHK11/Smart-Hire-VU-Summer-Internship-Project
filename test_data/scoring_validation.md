# Scoring Engine Validation Report

This report validates the ranking pipeline output for the 5 synthetic resumes against the Job Description.

## Expected Order vs. Actual Order

Expected Rank Order: `resume_1.pdf` > `resume_2.pdf` > `resume_3.pdf` > `resume_4.pdf` > `resume_5.pdf`

### Default Alpha Results (α = 0.3)

| Rank | Filename | TF-IDF Score | SBERT Score | Final Score | Experience (Yrs) | Skills Matched |
|------|----------|--------------|-------------|-------------|------------------|----------------|
| 1 | resume_1.pdf | 0.3964 | 0.7480 | 0.6425 | 6 | aws, deep learning, docker, fastapi, git, machine learning, python, pytorch, sql |
| 2 | resume_2.pdf | 0.2844 | 0.6869 | 0.5662 | 4 | css, django, docker, git, html, machine learning, postgresql, python, sql |
| 3 | resume_3.pdf | 0.1116 | 0.5634 | 0.4279 | 2 | css, git, html, javascript, python, sql, sqlite |
| 4 | resume_4.pdf | 0.1033 | 0.5578 | 0.4215 | 1 | c++, git, java, spring boot, sql |
| 5 | resume_5.pdf | 0.0576 | 0.3414 | 0.2563 | 5 |  |

**Validation Status:** PASSED ✅

The actual ranking matches the expected rank order: 1 > 2 > 3 > 4 > 5.

## Alpha Sensitivity Analysis

We evaluated the impact of varying the alpha weight (α) on final scores and ranking orders:

| Filename | Score (α=0.2) | Score (α=0.3) | Score (α=0.4) | Score (α=0.6) | Score (α=0.8) |
|---|---|---|---|---|---|
| resume_1.pdf | 0.6776 | 0.6425 | 0.6073 | 0.5370 | 0.4667 |
| resume_2.pdf | 0.6064 | 0.5662 | 0.5259 | 0.4454 | 0.3649 |
| resume_3.pdf | 0.4731 | 0.4279 | 0.3827 | 0.2923 | 0.2020 |
| resume_4.pdf | 0.4669 | 0.4215 | 0.3760 | 0.2851 | 0.1942 |
| resume_5.pdf | 0.2847 | 0.2563 | 0.2279 | 0.1711 | 0.1144 |

### Rank Order under Different Alpha Settings:

- **α = 0.2:** resume_1.pdf > resume_2.pdf > resume_3.pdf > resume_4.pdf > resume_5.pdf
- **α = 0.3:** resume_1.pdf > resume_2.pdf > resume_3.pdf > resume_4.pdf > resume_5.pdf
- **α = 0.4:** resume_1.pdf > resume_2.pdf > resume_3.pdf > resume_4.pdf > resume_5.pdf
- **α = 0.6:** resume_1.pdf > resume_2.pdf > resume_3.pdf > resume_4.pdf > resume_5.pdf
- **α = 0.8:** resume_1.pdf > resume_2.pdf > resume_3.pdf > resume_4.pdf > resume_5.pdf

## Recommendations & Conclusion

At the default weight of α = 0.3, SBERT semantic matching is weighted heavily (70%) while TF-IDF lexical matching is weighted 30%.

The current default α = 0.3 successfully generates the expected ordering without any ranking deviations. SBERT handles semantic parsing of experience and machine learning domains effectively, while TF-IDF ensures specific keyword overlap counts.
