# generate_test_data.py
# Python script to generate synthetic test resumes and job descriptions using PyMuPDF

import os
import fitz

def create_pdf(filename: str, text: str):
    doc = fitz.open()
    page = doc.new_page()
    # Write text in a structured layout
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, text, fontsize=10, fontname="helv")
    doc.save(filename)
    doc.close()
    print(f"Created PDF: {filename}")

def main():
    test_dir = r"d:\VU Internship Project\test_data"
    resumes_dir = os.path.join(test_dir, "resumes")
    os.makedirs(resumes_dir, exist_ok=True)

    # 1. Create Job Description
    jd_content = (
        "Role: Senior Software Engineer (Python & Machine Learning)\n\n"
        "We are looking for a Senior Software Engineer with strong experience in Python, Machine Learning, "
        "and Deep Learning to build our AI-powered applications.\n\n"
        "Key Requirements:\n"
        "- 5+ years of experience in professional software development.\n"
        "- Strong proficiency in Python, SQL, and Git.\n"
        "- Practical experience with Machine Learning models, Deep Learning, and PyTorch.\n"
        "- Experience building APIs with FastAPI and containerizing services using Docker.\n"
        "- Degree: B.Tech or M.Tech in Computer Science or a related technical field."
    )
    
    jd_path = os.path.join(test_dir, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(jd_content)
    print(f"Created JD: {jd_path}")

    # 2. Create Resume 1 (Strong Match)
    resume1 = (
        "Mithilesh Kolhapurkar\n"
        "Email: mithilesh@example.com | Phone: 1234567890\n"
        "Senior Software Engineer\n\n"
        "Summary:\n"
        "Highly experienced Software Engineer with 6 years of experience specializing in Python, "
        "Machine Learning, and Deep Learning applications. Proven track record of deploying containerized microservices.\n\n"
        "Experience:\n"
        "Senior AI Engineer | Tech Corp (2022 - Present)\n"
        "- Designed and built ML and Deep Learning pipelines using PyTorch for resume processing.\n"
        "- Developed scalable REST APIs using FastAPI and deployed them via Docker containers.\n"
        "- Wrote complex SQL queries for database optimization and worked with Git for version control.\n\n"
        "Education:\n"
        "M.Tech in Computer Science | Stanford University (2020 - 2022)\n"
        "B.Tech in Computer Science | Indian Institute of Technology (2016 - 2020)\n\n"
        "Skills:\n"
        "Python, Machine Learning, Deep Learning, PyTorch, FastAPI, Docker, SQL, Git, AWS"
    )
    create_pdf(os.path.join(resumes_dir, "resume_1.pdf"), resume1)

    # 3. Create Resume 2 (Good Match)
    resume2 = (
        "Ankita Patil\n"
        "Email: ankita@example.com | Phone: 0987654321\n"
        "Software Developer\n\n"
        "Summary:\n"
        "Professional developer with 4 years of experience building Python and web applications. "
        "Skilled in SQL, Docker containerization, and Machine Learning.\n\n"
        "Experience:\n"
        "Software Engineer | Solutions Inc (2022 - Present)\n"
        "- Developed backend services using Python and Django.\n"
        "- Integrated Machine Learning models for predictive analytics.\n"
        "- Deployed Docker containers for hosting services and managed version control with Git.\n"
        "- Managed relational databases with SQL Server and PostgreSQL.\n\n"
        "Education:\n"
        "B.Tech in Computer Science | Pune University (2018 - 2022)\n\n"
        "Skills:\n"
        "Python, Django, SQL, Docker, Git, Machine Learning, PostgreSQL, HTML, CSS"
    )
    create_pdf(os.path.join(resumes_dir, "resume_2.pdf"), resume2)

    # 4. Create Resume 3 (Partial Match)
    resume3 = (
        "John Doe\n"
        "Email: john@example.com\n"
        "Full Stack Engineer\n\n"
        "Summary:\n"
        "Full Stack Developer with 2 years of experience. Experienced with Python web frameworks and database management.\n\n"
        "Experience:\n"
        "Junior Engineer | WebDev Lab (2024 - Present)\n"
        "- Built website frontends using HTML, CSS, and JavaScript.\n"
        "- Wrote basic backend scripts in Python.\n"
        "- Maintained SQLite database tables using SQL and managed repositories with Git.\n\n"
        "Education:\n"
        "Bachelor of Engineering in Information Technology | Mumbai University (2020 - 2024)\n\n"
        "Skills:\n"
        "Python, JavaScript, HTML, CSS, SQL, Git, SQLite, Bootstrap"
    )
    create_pdf(os.path.join(resumes_dir, "resume_3.pdf"), resume3)

    # 5. Create Resume 4 (Weak Match)
    resume4 = (
        "Carol Smith\n"
        "Email: carol@example.com\n"
        "Software Developer\n\n"
        "Summary:\n"
        "Software developer with 1 year of experience in enterprise development, specializing in Java and databases.\n\n"
        "Experience:\n"
        "Associate Developer | Enterprise Ltd (2025 - Present)\n"
        "- Developed desktop and web services using Java and Spring Boot.\n"
        "- Wrote SQL scripts for data migrations.\n"
        "- Used Git for source control management.\n\n"
        "Education:\n"
        "Bachelor of Science in Mathematics | Delhi University (2021 - 2024)\n\n"
        "Skills:\n"
        "Java, Spring Boot, SQL, Git, Linux, C++"
    )
    create_pdf(os.path.join(resumes_dir, "resume_4.pdf"), resume4)

    # 6. Create Resume 5 (Near-Zero Match)
    resume5 = (
        "David Miller\n"
        "Email: david@example.com\n"
        "Sales and Marketing Manager\n\n"
        "Summary:\n"
        "Dynamic Sales Professional with 5 years of experience in B2B sales and digital marketing. "
        "Proven expertise in CRM tools and lead generation.\n\n"
        "Experience:\n"
        "Sales Manager | Retail Solutions (2021 - Present)\n"
        "- Managed client relationships and drove B2B sales cycles.\n"
        "- Optimized digital marketing campaigns to increase lead generation by 40%.\n"
        "- Used Salesforce CRM and Microsoft Excel for tracking sales performance.\n\n"
        "Education:\n"
        "MBA in Marketing | Business School (2019 - 2021)\n\n"
        "Skills:\n"
        "B2B Sales, Digital Marketing, Customer Relationship Management, Salesforce CRM, Microsoft Excel, Negotiation, Team Management"
    )
    create_pdf(os.path.join(resumes_dir, "resume_5.pdf"), resume5)

if __name__ == "__main__":
    main()
