import os
import docx
import fitz

def generate_pdf(filename: str, text: str):
    """Generates a simple single-page PDF with the given text using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page()
    # Split text into lines to avoid overflow
    lines = text.split("\n")
    y = 50
    for line in lines:
        if line.strip():
            page.insert_text((50, y), line, fontsize=10)
            y += 18
            if y > 750: # add a new page if it overflows
                page = doc.new_page()
                y = 50
        else:
            y += 10
            
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)
    doc.close()
    print(f"Generated PDF: {filename}")

def generate_docx(filename: str, text: str):
    """Generates a Word document with the given text."""
    doc = docx.Document()
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            doc.add_paragraph(line)
            
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)
    print(f"Generated DOCX: {filename}")

# Sample Texts
JD_TEXT = """
Job Title: Python Software Engineer (Machine Learning)
Experience Required: 3-5 years of experience
Required Skills: Python, Machine Learning, NLP, FastAPI, Docker, SQL, PostgreSQL, Git, AWS.
Education: Bachelor's Degree in Computer Science or equivalent.

Job Description:
We are looking for a Python Software Engineer to join our AI team. You will build and deploy machine learning models, develop REST APIs using FastAPI, and containerize applications with Docker. You will work with relational databases like PostgreSQL and deploy applications on AWS. Experience with Git for version control is required.
"""

RESUME_PERFECT = """
John Doe - Senior Software Engineer
Email: john.doe@example.com | Phone: 123-456-7890
Experience: 5 years of experience in software development.

Professional Experience:
- Software Engineer at Tech Corp (2021 - Present)
  * Developed and deployed microservices using FastAPI and Python.
  * Built and trained Machine Learning models for NLP applications.
  * Containerized services using Docker and managed deployments on AWS cloud.
- Junior Engineer at Dev Studio (2019 - 2021)
  * Worked with SQL and PostgreSQL databases to optimize query performance.
  * Used Git for source code management and CI/CD pipelines.

Skills: Python, Machine Learning, NLP, FastAPI, Docker, SQL, PostgreSQL, Git, AWS, Java, JavaScript.
Education: Bachelor's Degree in Computer Science from State University.
"""

RESUME_SEMANTIC = """
Jane Smith - Intelligent Systems Developer
Email: jane.smith@example.com | Phone: 987-654-3210
Experience: 3 years of experience in system design.

Work Experience:
- Backend Systems Engineer at Innovation Labs (2022 to present)
  * Crafted microservices in Python programming language.
  * Implemented neural networks and natural language understanding features.
  * Structured containerization using Docker for local and cloud environments.
- Software Intern at CodeCraft (2021 to 2022)
  * Managed database administration with postgresql and SQLite.
  * Used version control systems (Git) for team project collaboration.

Skills: Python, Neural Networks, NLU, SQLite, PostgreSQL, Git, Cloud Infrastructure, Docker.
Education: Master's Degree in Intelligent Systems.
"""

RESUME_WEAK = """
Bob Johnson - Creative Web Designer
Email: bob.j@example.com | Phone: 555-555-5555
Experience: 1 year of experience in design.

Work Experience:
- Web Design Associate at Media Agency (2024 - 2025)
  * Designed websites using HTML, CSS, Bootstrap, and WordPress templates.
  * Created UI/UX wireframes and mockups using Photoshop and Figma.
  * Handled client interactions and website updates.

Skills: HTML, CSS, WordPress, Photoshop, Figma, Illustrator, Web Design, UI/UX.
Education: Bachelor's Degree in Fine Arts.
"""

if __name__ == "__main__":
    # Generate JD
    os.makedirs("d:/VU Internship Project/test_data", exist_ok=True)
    with open("d:/VU Internship Project/test_data/jd.txt", "w", encoding="utf-8") as f:
        f.write(JD_TEXT.strip())
    print("Generated job description text file.")
    
    # Generate Resumes
    generate_pdf("d:/VU Internship Project/test_data/resumes/john_doe_perfect.pdf", RESUME_PERFECT.strip())
    generate_docx("d:/VU Internship Project/test_data/resumes/jane_smith_semantic.docx", RESUME_SEMANTIC.strip())
    generate_pdf("d:/VU Internship Project/test_data/resumes/bob_johnson_weak.pdf", RESUME_WEAK.strip())
