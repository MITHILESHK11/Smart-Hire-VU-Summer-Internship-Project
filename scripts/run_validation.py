# run_validation.py
# Script to run the validation pipeline for Phase 3 and generate scoring_validation.md

import os
from backend.modules.ingestion import extract_text_from_pdf
from backend.modules.ner import extract_entities
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import build_ranking_output

def main():
    test_dir = r"d:\VU Internship Project\test_data"
    resumes_dir = os.path.join(test_dir, "resumes")
    
    # Load Job Description
    with open(os.path.join(test_dir, "jd.txt"), "r", encoding="utf-8") as f:
        jd_text = f.read()
        
    filenames = [f"resume_{i}.pdf" for i in range(1, 6)]
    resume_paths = [os.path.join(resumes_dir, name) for name in filenames]
    
    # 1. Ingest resumes
    resume_texts = [extract_text_from_pdf(path) for path in resume_paths]
    
    # 2. Extract NER entities
    ner_results = [extract_entities(text) for text in resume_texts]
    
    # 3. Compute scores at different alphas (0.2, 0.3, 0.4, 0.6, 0.8)
    alphas = [0.2, 0.3, 0.4, 0.6, 0.8]
    alpha_results = {}
    
    for alpha in alphas:
        scored = compute_hybrid_scores(jd_text, resume_texts, alpha=alpha)
        ranked = build_ranking_output(
            session_id="validation",
            filenames=filenames,
            scored_resumes=scored,
            resume_texts=resume_texts,
            jd_text=jd_text,
            ner_results=ner_results
        )
        alpha_results[alpha] = ranked

    # 4. Generate the Markdown Validation report
    report_content = []
    report_content.append("# Scoring Engine Validation Report\n\n")
    report_content.append("This report validates the ranking pipeline output for the 5 synthetic resumes against the Job Description.\n\n")
    report_content.append("## Expected Order vs. Actual Order\n\n")
    report_content.append("Expected Rank Order: `resume_1.pdf` > `resume_2.pdf` > `resume_3.pdf` > `resume_4.pdf` > `resume_5.pdf`\n\n")
    
    # Add Default alpha=0.3 results table
    default_ranked = alpha_results[0.3]
    report_content.append("### Default Alpha Results (α = 0.3)\n\n")
    report_content.append("| Rank | Filename | TF-IDF Score | SBERT Score | Final Score | Experience (Yrs) | Skills Matched |\n")
    report_content.append("|------|----------|--------------|-------------|-------------|------------------|----------------|\n")
    for item in default_ranked:
        skills = ", ".join(item["skills_matched"])
        exp = item["experience_years"] if item["experience_years"] is not None else "None"
        report_content.append(f"| {item['rank']} | {item['filename']} | {item['tfidf_score']:.4f} | {item['sbert_score']:.4f} | {item['final_score']:.4f} | {exp} | {skills} |\n")
        
    # Check if actual ranks match expected order
    actual_order = [item["filename"] for item in default_ranked]
    expected_order = [f"resume_{i}.pdf" for i in range(1, 6)]
    order_matches = actual_order == expected_order
    
    report_content.append(f"\n**Validation Status:** {'PASSED ✅' if order_matches else 'FAILED ❌'}\n\n")
    if order_matches:
        report_content.append("The actual ranking matches the expected rank order: 1 > 2 > 3 > 4 > 5.\n\n")
    else:
        report_content.append(f"Deviations detected. Actual order: {' > '.join(actual_order)}\n\n")
        
    # Alpha Sensitivity Table
    report_content.append("## Alpha Sensitivity Analysis\n\n")
    report_content.append("We evaluated the impact of varying the alpha weight (α) on final scores and ranking orders:\n\n")
    
    headers = ["Filename"] + [f"Score (α={a})" for a in alphas]
    report_content.append("| " + " | ".join(headers) + " |\n")
    report_content.append("|" + "|".join(["---"] * len(headers)) + "|\n")
    
    # Display each resume and its score across all alphas
    for name in expected_order:
        row = [name]
        for alpha in alphas:
            for item in alpha_results[alpha]:
                if item["filename"] == name:
                    row.append(f"{item['final_score']:.4f}")
                    break
        report_content.append("| " + " | ".join(row) + " |\n")
        
    # Rank order comparison across different alphas
    report_content.append("\n### Rank Order under Different Alpha Settings:\n\n")
    for alpha in alphas:
        order = [item["filename"] for item in alpha_results[alpha]]
        report_content.append(f"- **α = {alpha}:** {' > '.join(order)}\n")
        
    report_content.append("\n## Recommendations & Conclusion\n\n")
    report_content.append("At the default weight of α = 0.3, SBERT semantic matching is weighted heavily (70%) while TF-IDF lexical matching is weighted 30%.\n\n")
    if order_matches:
        report_content.append("The current default α = 0.3 successfully generates the expected ordering without any ranking deviations. SBERT handles semantic parsing of experience and machine learning domains effectively, while TF-IDF ensures specific keyword overlap counts.\n")
    else:
        report_content.append("An adjustment is recommended to align with the expected ordering. See the ranks above.\n")
        
    # Write to file
    out_path = os.path.join(test_dir, "scoring_validation.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(report_content)
        
    print(f"Generated validation report at: {out_path}")

if __name__ == "__main__":
    main()
