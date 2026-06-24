'''import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\suyas\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text


def extract_text_ocr(pdf_path):
    try:
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        text = ""
        for page in pages:
            page_text = pytesseract.image_to_string(page)
            text += page_text + "\n"
        return text
    except Exception as e:
        # Fallback to pdfplumber if OCR fails
        return extract_text_from_pdf(pdf_path)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_resume(text):
    text = str(text)
    text = re.sub(r'http\S+|www\S+', ' ', text)       # remove URLs
    text = re.sub(r'\S+@\S+', ' ', text)               # remove emails
    text = re.sub(r'\d{10,}', ' ', text)               # remove phone numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)           # remove special chars
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ============================================================
# SKILL EXTRACTION
# ============================================================

SKILLS_DB = [
    # Programming
    "python", "java", "c++", "javascript", "html", "css",
    "react", "node.js", "sql", "mysql", "git",
    # Data
    "excel", "power bi", "tableau", "data analysis", "pandas", "numpy",
    # AI/ML
    "machine learning", "deep learning", "tensorflow", "keras",
    # HR
    "recruitment", "onboarding", "employee relations", "interviewing",
    "talent acquisition", "hr management",
    # Soft Skills
    "communication", "leadership", "teamwork", "problem solving"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))


# ============================================================
# SCORING
# ============================================================

def calculate_skill_match(candidate_skills, required_skills):
    if not required_skills:
        return 0.0
    candidate_set = set(candidate_skills)
    required_set = set(required_skills)
    matched = candidate_set.intersection(required_set)
    score = (len(matched) / len(required_set)) * 100
    return round(score, 2)


def calculate_resume_similarity(resume_text, job_description):
    try:
        documents = [str(resume_text), str(job_description)]
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(documents)
        similarity = cosine_similarity(matrix[0:1], matrix[1:2])
        return round(similarity[0][0] * 100, 2)
    except Exception:
        return 0.0


def hiring_recommendation(score):
    if score >= 80:
        return "Strongly Recommend"
    elif score >= 65:
        return "Recommend"
    elif score >= 50:
        return "Consider"
    else:
        return "Reject"


# ============================================================
# SKILLS ANALYSIS
# ============================================================

def get_missing_skills(candidate_skills, required_skills):
    return list(set(required_skills) - set(candidate_skills))


def get_strengths(candidate_skills):
    return candidate_skills[:5]


def get_weaknesses(missing_skills):
    if len(missing_skills) >= 4:
        return "Several Important Skills Missing"
    elif len(missing_skills) >= 2:
        return "Moderate Skill Gaps"
    else:
        return "Minor Skill Gaps"


# ============================================================
# FEEDBACK
# ============================================================

def generate_resume_feedback(candidate_skills, required_skills, final_score):
    feedback = []
    matched = list(set(candidate_skills) & set(required_skills))
    missing = list(set(required_skills) - set(candidate_skills))

    feedback.append("=== STRENGTHS ===")
    if matched:
        for skill in matched:
            feedback.append(f"✓ Strong in {skill}")
    else:
        feedback.append("No matching skills found.")

    feedback.append("")
    feedback.append("=== IMPROVEMENT AREAS ===")
    if missing:
        for skill in missing:
            feedback.append(f"✗ Learn {skill}")
    else:
        feedback.append("✓ No critical skill gaps detected.")

    feedback.append("")
    feedback.append("=== RECOMMENDATIONS ===")
    if final_score >= 80:
        feedback.append("Candidate is highly aligned with the role.")
    elif final_score >= 60:
        feedback.append("Candidate should strengthen missing skills.")
    else:
        feedback.append("Candidate requires significant upskilling.")
    feedback.append("Add real-world projects.")
    feedback.append("Maintain GitHub portfolio.")

    return "\n".join(feedback)


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

def generate_interview_questions(skills):
    questions = []
    skills_lower = [s.lower() for s in skills]

    if "python" in skills_lower:
        questions.append("Explain List vs Tuple in Python.")
    if "sql" in skills_lower:
        questions.append("What is the difference between JOIN and UNION?")
    if "power bi" in skills_lower:
        questions.append("How do you create dashboards in Power BI?")
    if "machine learning" in skills_lower:
        questions.append("Explain Bias vs Variance in machine learning.")
    if "excel" in skills_lower:
        questions.append("How do you use VLOOKUP and Pivot Tables in Excel?")
    if "data analysis" in skills_lower:
        questions.append("Describe your data analysis workflow from raw data to insights.")
    if "react" in skills_lower:
        questions.append("What is the Virtual DOM and how does React use it?")
    if "javascript" in skills_lower:
        questions.append("Explain the difference between let, const, and var.")
    if "java" in skills_lower:
        questions.append("What is the difference between an interface and an abstract class in Java?")
    if "tensorflow" in skills_lower:
        questions.append("How do you build and train a neural network using TensorFlow?")

    if not questions:
        questions.append("Tell us about yourself and your relevant experience.")

    return questions


# ============================================================
# AI SUMMARY
# ============================================================

def ai_summary_for_score(final_score):
    if final_score >= 80:
        return "Excellent candidate with strong alignment to the job requirements. Recommended for technical interview."
    elif final_score >= 65:
        return "Good candidate with relevant skills. Recommended for further screening."
    else:
        return "Candidate has notable skill gaps. Additional training is recommended."


# ============================================================
# RECRUITER CHATBOT
# ============================================================

def recruiter_chatbot(question, candidate_skills, required_skills,
                      final_score, skill_match, recommendation):
    q = question.lower()
    missing = list(set(required_skills) - set(candidate_skills))

    if "score" in q:
        return f"Candidate Final Score: {round(final_score, 2)}%\nRecommendation: {recommendation}"
    elif "missing" in q:
        if not missing:
            return "No critical skill gaps detected."
        return "Missing Skills:\n\n" + ", ".join(missing)
    elif "skills" in q:
        return "Detected Skills:\n\n" + ", ".join(candidate_skills)
    elif "why" in q:
        return (f"Candidate possesses {len(candidate_skills)} identified skills.\n"
                f"Skill Match: {round(skill_match, 2)}%\n"
                f"Final Score: {round(final_score, 2)}%\n"
                f"Recommendation: {recommendation}")
    elif "interview" in q:
        questions = generate_interview_questions(candidate_skills)
        return "\n".join(questions)
    elif "feedback" in q:
        return generate_resume_feedback(candidate_skills, required_skills, final_score)
    else:
        return "You can ask about: score, skills, missing skills, why recommended, interview questions, feedback."


# ============================================================
# PDF REPORT GENERATOR
# ============================================================

def clean_txt_for_pdf(text):
    """Removes emoji characters right before PDF compilation so ReportLab doesn't crash."""
    if not text:
        return ""
    # Strips away non-ASCII characters (like emojis)
    return re.sub(r'[^\x00-\x7F]+', '', str(text))


def generate_pdf_report(
    filename,
    job_role,
    skill_match,
    similarity,
    final_score,
    recommendation,
    candidate_skills,
    missing_skills
):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # Emojis are filtered out here safely for the PDF document only
    job_role = clean_txt_for_pdf(job_role)
    recommendation = clean_txt_for_pdf(recommendation)
    detected_str = clean_txt_for_pdf(', '.join(candidate_skills))
    missing_str = clean_txt_for_pdf(', '.join(missing_skills))

    content.append(
        Paragraph("HireGenius AI Candidate Report", styles['Title'])
    )
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Job Role:</b> {job_role}", styles['Normal']))
    content.append(Paragraph(f"<b>Skill Match:</b> {skill_match}%", styles['Normal']))
    content.append(Paragraph(f"<b>Resume Similarity:</b> {similarity}%", styles['Normal']))
    content.append(Paragraph(f"<b>Final Score:</b> {final_score}%", styles['Normal']))
    content.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", styles['Normal']))
    
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"<b>Detected Skills:</b> {detected_str}", styles['Normal']))
    
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"<b>Missing Skills:</b> {missing_str}", styles['Normal']))

    doc.build(content)'''


#---------------------------------------------------------

import re
import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ReportLab Layout & Styling Engines
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\suyas\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"

# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def extract_text_ocr(pdf_path):
    try:
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        text = ""
        for page in pages:
            page_text = pytesseract.image_to_string(page)
            text += page_text + "\n"
        return text
    except Exception:
        return extract_text_from_pdf(pdf_path)

# ============================================================
# TEXT CLEANING
# ============================================================

def clean_resume(text):
    text = str(text)
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\d{10,}', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ============================================================
# SKILL EXTRACTION
# ============================================================

SKILLS_DB = [
    "python", "java", "c++", "javascript", "html", "css",
    "react", "node.js", "sql", "mysql", "git",
    "excel", "power bi", "tableau", "data analysis", "pandas", "numpy",
    "machine learning", "deep learning", "tensorflow", "keras",
    "recruitment", "onboarding", "employee relations", "interviewing",
    "talent acquisition", "hr management",
    "communication", "leadership", "teamwork", "problem solving"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)
    return list(set(found_skills))

# ============================================================
# SCORING & LOGIC BALANCE
# ============================================================

def calculate_skill_match(candidate_skills, required_skills):
    if not required_skills:
        return 0.0
    candidate_set = set(candidate_skills)
    required_set = set(required_skills)
    matched = candidate_set.intersection(required_set)
    score = (len(matched) / len(required_set)) * 100
    return round(score, 2)

def calculate_resume_similarity(resume_text, job_description):
    try:
        documents = [str(resume_text), str(job_description)]
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(documents)
        similarity = cosine_similarity(matrix[0:1], matrix[1:2])
        return round(similarity[0][0] * 100, 2)
    except Exception:
        return 0.0

def hiring_recommendation(score):
    if score >= 70:
        return "Strongly Recommend"
    elif score >= 55:
        return "Recommend"
    elif score >= 40:
        return "Consider"
    else:
        return "Reject"

# ============================================================
# SKILLS ANALYSIS
# ============================================================

def get_missing_skills(candidate_skills, required_skills):
    return list(set(required_skills) - set(candidate_skills))

def get_strengths(candidate_skills):
    return candidate_skills[:5]

def get_weaknesses(missing_skills):
    if len(missing_skills) >= 4:
        return "Several Important Skills Missing"
    elif len(missing_skills) >= 2:
        return "Moderate Skill Gaps"
    else:
        return "Minor Skill Gaps"

# ============================================================
# FEEDBACK GENERATOR
# ============================================================

def generate_resume_feedback(candidate_skills, required_skills, final_score):
    feedback = []
    matched = list(set(candidate_skills) & set(required_skills))
    missing = list(set(required_skills) - set(candidate_skills))

    feedback.append("=== STRENGTHS ===")
    if matched:
        for skill in matched:
            feedback.append(f"✓ Strong in {skill}")
    else:
        feedback.append("No matching skills found.")

    feedback.append("\n=== IMPROVEMENT AREAS ===")
    if missing:
        for skill in missing:
            feedback.append(f"✗ Learn {skill}")
    else:
        feedback.append("✓ No critical skill gaps detected.")

    feedback.append("\n=== RECOMMENDATIONS ===")
    if final_score >= 70:
        feedback.append("Candidate is highly aligned with the role.")
    elif final_score >= 40:
        feedback.append("Candidate should strengthen missing skills.")
    else:
        feedback.append("Candidate requires significant upskilling.")
    
    feedback.append("Add real-world projects.")
    feedback.append("Maintain GitHub portfolio.")
    return "\n".join(feedback)

# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

def generate_interview_questions(skills):
    questions = []
    skills_lower = [s.lower() for s in skills]

    if "python" in skills_lower:
        questions.append("Explain List vs Tuple in Python.")
    if "sql" in skills_lower:
        questions.append("What is the difference between JOIN and UNION?")
    if "power bi" in skills_lower:
        questions.append("How do you create dashboards in Power BI?")
    if "machine learning" in skills_lower:
        questions.append("Explain Bias vs Variance in machine learning.")
    if "excel" in skills_lower:
        questions.append("How do you use VLOOKUP and Pivot Tables in Excel?")
    if "data analysis" in skills_lower:
        questions.append("Describe your data analysis workflow from raw data to insights.")
    if "react" in skills_lower:
        questions.append("What is the Virtual DOM and how does React use it?")
    if "javascript" in skills_lower:
        questions.append("Explain the difference between let, const, and var.")
    if "java" in skills_lower:
        questions.append("What is the difference between an interface and an abstract class in Java?")
    if "tensorflow" in skills_lower:
        questions.append("How do you build and train a neural network using TensorFlow?")

    if not questions:
        questions.append("Tell us about yourself and your relevant experience.")
    return questions

def ai_summary_for_score(final_score):
    if final_score >= 70:
        return "Excellent candidate with strong alignment to the job requirements. Recommended for technical interview."
    elif final_score >= 55:
        return "Good candidate with relevant skills. Recommended for further screening."
    elif final_score >= 40:
        return "Candidate has foundational qualifications with manageable gaps. Structural consideration recommended."
    else:
        return "Candidate has notable skill gaps. Additional training or upskilling is strongly recommended."

# ============================================================
# RECRUITER CHATBOT
# ============================================================

def recruiter_chatbot(question, candidate_skills, required_skills, final_score, skill_match, recommendation):
    q = question.lower()
    missing = list(set(required_skills) - set(candidate_skills))

    if "score" in q:
        return f"Candidate Final Score: {round(final_score, 2)}%\nRecommendation: {recommendation}"
    elif "missing" in q:
        if not missing:
            return "No critical skill gaps detected."
        return "Missing Skills:\n\n" + ", ".join(missing)
    elif "skills" in q:
        return "Detected Skills:\n\n" + ", ".join(candidate_skills)
    elif "why" in q:
        return (f"Candidate possesses {len(candidate_skills)} identified skills.\n"
                f"Skill Match: {round(skill_match, 2)}%\n"
                f"Final Score: {round(final_score, 2)}%\n"
                f"Recommendation: {recommendation}")
    elif "interview" in q:
        questions = generate_interview_questions(candidate_skills)
        return "\n".join(questions)
    elif "feedback" in q:
        return generate_resume_feedback(candidate_skills, required_skills, final_score)
    else:
        return "You can ask about: score, skills, missing skills, why recommended, interview questions, or feedback."

# ============================================================
# BEAUTIFIED PDF REPORT GENERATOR
# ============================================================

def clean_txt_for_pdf(text):
    if not text:
        return ""
    return re.sub(r'[^\x00-\x7F]+', '', str(text))

def generate_pdf_report(filename, job_role, skill_match, similarity, final_score, recommendation, candidate_skills, missing_skills):
    # Set standard page bounds with 0.5 inch (36 point) margins for optimal printable real estate
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    content = []

    # Custom Color Configurations
    PRIMARY_COLOR = colors.HexColor("#1e2540")     # Slate Corporate Dark
    ACCENT_COLOR = colors.HexColor("#38bdf8")      # Electric Blue Accent
    BG_LIGHT = colors.HexColor("#f8fafc")          # Ice White Row Background
    BORDER_COLOR = colors.HexColor("#cbd5e1")      # Structural Dividers

    # Status Recommendation Colors
    if final_score >= 70:
        rec_bg = colors.HexColor("#dcfce7")
        rec_text = colors.HexColor("#166534")
    elif final_score >= 40:
        rec_bg = colors.HexColor("#fef9c3")
        rec_text = colors.HexColor("#854d0e")
    else:
        rec_bg = colors.HexColor("#fee2e2")
        rec_text = colors.HexColor("#991b1b")

    # Custom Typography Style Injections
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=14,
        spaceAfter=6
    )

    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155")
    )

    cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=cell_style,
        fontName='Helvetica-Bold',
        textColor=PRIMARY_COLOR
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1, # Center Align
        textColor=rec_text
    )

    # 1. Document Header Section
    content.append(Paragraph("HIREGENIUS AI", title_style))
    content.append(Paragraph("Candidate Appraisal Matrix & Structural Evaluation Summary Report", subtitle_style))
    
    # Structural Top Accent Accent Bar
    accent_bar = Table([[""]], colWidths=[540], rowHeights=[4])
    accent_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_COLOR),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    content.append(accent_bar)
    content.append(Spacer(1, 15))

    # 2. Executive Analytics Metrics Block (Structured Table Data Grid)
    content.append(Paragraph("Core Alignment Parameters", section_heading))
    
    metrics_data = [
        [Paragraph("Target Profile Vector Role", cell_bold), Paragraph(clean_txt_for_pdf(job_role), cell_style)],
        [Paragraph("Functional Keyword Skill Match", cell_bold), Paragraph(f"{skill_match}%", cell_style)],
        [Paragraph("High-Dimensional Text Similarity", cell_bold), Paragraph(f"{similarity}%", cell_style)],
        [Paragraph("Weighted Comprehensive Score", cell_bold), Paragraph(f"{final_score}%", cell_style)]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[200, 340])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('BACKGROUND', (0,2), (-1,2), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    content.append(metrics_table)
    content.append(Spacer(1, 15))

    # 3. Decision Verdict Callout Box
    content.append(Paragraph("Operational Decision Recommendation", section_heading))
    
    verdict_table = Table([[Paragraph(clean_txt_for_pdf(recommendation).upper(), badge_style)]], colWidths=[540], rowHeights=[32])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), rec_bg),
        ('BOX', (0,0), (-1,-1), 1, rec_text),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    content.append(verdict_table)
    content.append(Spacer(1, 15))

    # 4. Technical Skill Inventory Coverage
    content.append(Paragraph("Technical Skill Taxonomy Profile Mapping", section_heading))
    
    detected_str = ", ".join(candidate_skills).title() if candidate_skills else "No Primary Key Skills Identified"
    missing_str = ", ".join(missing_skills).title() if missing_skills else "None. Profile Meets Complete Matrix Coverage"

    skills_data = [
        [Paragraph("Detected Technical Skills", cell_bold), Paragraph(clean_txt_for_pdf(detected_str), cell_style)],
        [Paragraph("Identified Matrix Structural Gaps", cell_bold), Paragraph(clean_txt_for_pdf(missing_str), cell_style)]
    ]
    
    skills_table = Table(skills_data, colWidths=[200, 340])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    content.append(skills_table)

    # Compile Layout Object Elements
    doc.build(content)