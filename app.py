import streamlit as st
import tempfile
import os
from backend import (
    extract_text_ocr,
    clean_resume,
    extract_skills,
    calculate_skill_match,
    calculate_resume_similarity,
    hiring_recommendation,
    get_missing_skills,
    get_weaknesses,
    generate_resume_feedback,
    generate_interview_questions,
    ai_summary_for_score,
    recruiter_chatbot,
    generate_pdf_report,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HireGenius AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# JOB DESCRIPTIONS
# ============================================================

JOB_DESCRIPTIONS = {
    "Data Analyst": "python sql excel power bi tableau data analysis pandas numpy communication leadership teamwork",
    "Software Engineer": "python java c++ javascript react node.js git sql problem solving teamwork communication",
    "ML Engineer": "python machine learning deep learning tensorflow keras numpy pandas sql git communication",
    "HR Manager": "recruitment onboarding employee relations interviewing talent acquisition hr management communication leadership",
    "Frontend Developer": "html css javascript react node.js git communication teamwork problem solving",
}

REQUIRED_SKILLS_MAP = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "data analysis"],
    "Software Engineer": ["python", "java", "javascript", "react", "git", "sql"],
    "ML Engineer": ["python", "machine learning", "deep learning", "tensorflow"],
    "HR Manager": ["recruitment", "onboarding", "employee relations", "interviewing", "talent acquisition", "hr management"],
    "Frontend Developer": ["html", "css", "javascript", "react", "node.js", "git"],
}

# ============================================================
# CUSTOM ENTERPRISE CSS
# ============================================================

st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
    background-color: #0d0f1a !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 100% !important;
}
.hg-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 4px;
}
.hg-logo {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hg-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 2rem;
}
.card {
    background: #131625;
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 1.2rem;
}
.card-center { text-align: center; }
.card h3 { font-size: 1.15rem; color: #f1f5f9; margin: 12px 0 6px 0; }
.card p { font-size: 0.82rem; color: #64748b; margin: 0; }
.card-icon { font-size: 2rem; }
.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem; }
.card-teal { border-top: 2px solid #2dd4bf; }
.card-purple { border-top: 2px solid #818cf8; }
.card-banner { background: linear-gradient(135deg, #131625 0%, #1a1f3a 100%); border: 1px solid #2d3561; }
.recruiter-insight-box { background: #1e293b; border-left: 5px solid #38bdf8; border-radius: 8px; padding: 16px; margin: 1rem 0; }
.section-heading { font-size: 1.1rem; font-weight: 600; color: #e2e8f0; margin: 1.8rem 0 0.6rem 0; }
.section-sub { font-size: 0.8rem; color: #475569; margin-bottom: 1.2rem; }
.stSelectbox > div > div { background: #131625 !important; border: 1px solid #1e2540 !important; color: #e2e8f0 !important; border-radius: 10px !important; }
.stFileUploader > div { background: #131625 !important; border: 1.5px dashed #2d3561 !important; border-radius: 12px !important; }
div[data-testid="stButton"] > button { background: linear-gradient(90deg, #6366f1, #38bdf8) !important; color: #fff !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; padding: 0.6rem 2rem !important; }
.status-box { background: #131625; border: 1px solid #1e2540; border-radius: 14px; padding: 24px 28px; text-align: center; }
.score-pill { display: inline-block; padding: 4px 16px; border-radius: 999px; font-weight: 700; font-size: 1.1rem; margin-top: 6px; }
.score-green { background: #052e16; color: #4ade80; }
.score-yellow { background: #1c1a07; color: #facc15; }
.score-red { background: #2d0a0a; color: #f87171; }
.chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin: 6px 0 12px; }
.chip { background: #1e2540; border-radius: 6px; padding: 3px 10px; font-size: 0.75rem; color: #94a3b8; }
.chip-green { background: #052e16; color: #4ade80; }
.chip-red { background: #2d0a0a; color: #f87171; }
.metric-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 1rem; }
.metric-card { background: #131625; border: 1px solid #1e2540; border-radius: 10px; padding: 18px 16px; text-align: center; }
.metric-value { font-size: 1.6rem; font-weight: 700; color: #38bdf8; }
.metric-label { font-size: 0.72rem; color: #475569; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# APP HEADER VIEW
# ============================================================

st.markdown("""
<div class="hg-header">
  <span style="font-size:2.2rem">🤖</span>
  <span class="hg-logo">HireGenius AI</span>
</div>
<div class="hg-subtitle">Intelligent Enterprise Architecture &amp; Candidate Appraisal Matrix</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-center">
  <div class="card-icon">🤖</div>
  <h3>AI Recruitment Assistant</h3>
  <p>Generate hiring recommendations, interview questions and candidate insights using AI.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">🔍 Core Analytics Infrastructure</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card-grid">
  <div class="card card-teal">
    <div class="card-icon">📄</div>
    <h3>Document Extraction Layer</h3>
    <p>Automated pipeline structural normalization using custom Tesseract OCR modules.</p>
  </div>
  <div class="card card-purple">
    <div class="card-icon">🎯</div>
    <h3>Vector Feature Mapping</h3>
    <p>Calculates high-dimensional cosine spatial alignment across customized structural indexes.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">🚀 Real-time Execution Sandbox</div>', unsafe_allow_html=True)

job_role = st.selectbox("TARGET ENTERPRISE ASSIGNMENT PROFILE", options=list(JOB_DESCRIPTIONS.keys()), index=0)
uploaded_file = st.file_uploader("CANDIDATE DOCUMENT SOURCE PAYLOAD (PDF ONLY)", type=["pdf"])
analyze_clicked = st.button("🚀  Analyze Candidate")
result_area = st.empty()

if "results" not in st.session_state:
    st.session_state.results = None

# ============================================================
# BALANCED ANALYSIS PIPELINE
# ============================================================

if analyze_clicked:
    if uploaded_file is None:
        result_area.markdown("""
        <div class="status-box">
          <div class="status-icon">📁</div>
          <div class="status-title">No file uploaded</div>
          <div class="status-sub">Please upload a PDF resume before running analysis.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔍 Parsing resume and computing vectors…"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            raw_text = extract_text_ocr(tmp_path)
            cleaned = clean_resume(raw_text)

            candidate_skills = extract_skills(cleaned)
            required_skills = REQUIRED_SKILLS_MAP[job_role]
            job_desc = JOB_DESCRIPTIONS[job_role]

            skill_match = calculate_skill_match(candidate_skills, required_skills)
            similarity = calculate_resume_similarity(cleaned, job_desc)
            
            final_score = round((skill_match * 0.65) + (similarity * 0.35), 2)
            recommendation = hiring_recommendation(final_score)
            missing_skills = get_missing_skills(candidate_skills, required_skills)
            summary = ai_summary_for_score(final_score)

            if recommendation == "Strongly Recommend":
                recruiter_appraisal = "This is an exceptional candidate with high potential who exhibits all critical technical indicators. Highly strategic profile."
            elif recommendation == "Recommend":
                recruiter_appraisal = "This is a good candidate who shows clear potential and aligns well with the foundational role requirements."
            elif recommendation == "Consider":
                recruiter_appraisal = "This candidate has foundational qualities but exhibits core gaps. Proceed with consideration targeting baseline performance parameters."
            else:
                recruiter_appraisal = "This candidate does not demonstrate operational match thresholds for this target assignment matrix."

            # Generate a completely clean static local path to bypass browser caching artifacts
            report_filename = f"{job_role.replace(' ', '_')}_Appraisal_Report.pdf"
            report_path = os.path.join(tempfile.gettempdir(), report_filename)
            
            # Call the stylized Table layout function inside backend.py
            generate_pdf_report(
                filename=report_path,
                job_role=job_role,
                skill_match=skill_match,
                similarity=similarity,
                final_score=final_score,
                recommendation=recommendation,
                candidate_skills=candidate_skills,
                missing_skills=missing_skills,
            )

            # Open and read the raw binary stream of the generated layout immediately
            with open(report_path, "rb") as pdf_file:
                pdf_binary_data = pdf_file.read()

            st.session_state.results = {
                "job_role": job_role,
                "candidate_skills": candidate_skills,
                "required_skills": required_skills,
                "skill_match": skill_match,
                "similarity": similarity,
                "final_score": final_score,
                "recommendation": recommendation,
                "missing_skills": missing_skills,
                "summary": summary,
                "recruiter_appraisal": recruiter_appraisal,
                "pdf_data": pdf_binary_data,
                "report_filename": report_filename
            }
        try:
            os.unlink(tmp_path)
            os.unlink(report_path)
        except Exception:
            pass

# ============================================================
# RESULTS DISPLAY INTERFACE
# ============================================================

if st.session_state.results:
    r = st.session_state.results

    if r["final_score"] >= 70:
        pill_cls = "score-green"
    elif r["final_score"] >= 40:
        pill_cls = "score-yellow"
    else:
        pill_cls = "score-red"

    rec_icons = {"Strongly Recommend": "✅", "Recommend": "👍", "Consider": "🤔", "Reject": "❌"}
    rec_icon = rec_icons.get(r["recommendation"], "📊")

    st.markdown("---")
    st.markdown('<div class="section-heading">📊 Analysis Results</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="metric-value">{r['skill_match']}%</div><div class="metric-label">Skill Match</div></div>
      <div class="metric-card"><div class="metric-value">{r['similarity']}%</div><div class="metric-label">Resume Similarity</div></div>
      <div class="metric-card"><div class="metric-value">{r['final_score']}%</div><div class="metric-label">Final Score</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card card-center" style="margin-bottom:1rem;">
      <div class="card-icon">{rec_icon}</div>
      <h3>{r['recommendation']}</h3>
      <p>{r['summary']}</p>
      <span class="score-pill {pill_cls}">{r['final_score']}%</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="recruiter-insight-box">
        <strong style="color: #38bdf8; font-size: 0.9rem; text-transform: uppercase;">Recruiter Executive Summary:</strong>
        <p style="margin: 6px 0 0 0; font-size: 0.95rem; color: #f1f5f9; font-style: italic;">"{r['recruiter_appraisal']}"</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🛠 Skills", "📝 Feedback", "🎤 Interview Qs", "💬 AI Chatbot", "📄 Report"])

    with tab1:
        st.markdown("**Detected Skills**")
        if r["candidate_skills"]:
            chips = " ".join(f'<span class="chip chip-green">{s}</span>' for s in r["candidate_skills"])
            st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
        else:
            st.info("No skills detected.")

        st.markdown("**Missing Skills**")
        if r["missing_skills"]:
            chips = " ".join(f'<span class="chip chip-red">{s}</span>' for s in r["missing_skills"])
            st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical skill gaps detected.")
            
        st.markdown(f"**Structural Evaluation Gaps:** {get_weaknesses(r['missing_skills'])}")

    with tab2:
        st.markdown("<br><strong style='font-size:1rem; color:#f1f5f9;'>Executive Resume Feedback & Development Roadmap</strong><br><br>", unsafe_allow_html=True)
        
        matched_skills = list(set(r["candidate_skills"]) & set(r["required_skills"]))
        missing_skills = list(set(r["required_skills"]) - set(r["candidate_skills"]))
        
        st.markdown('<div style="margin-top: 5px; margin-bottom: 8px; font-weight: 600; color: #2dd4bf; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">💎 Core Strengths</div>', unsafe_allow_html=True)
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f'<span style="color: #4ade80; margin-right: 8px; font-weight:bold;">✓</span> Identified high proficiency alignment in **{skill.title()}**.', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: #64748b; font-style: italic;">No direct skill matches detected for primary target keywords.</span>', unsafe_allow_html=True)
            
        st.markdown('<div style="margin-top: 22px; margin-bottom: 8px; font-weight: 600; color: #facc15; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">🚀 Priority Improvement Areas</div>', unsafe_allow_html=True)
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f'<span style="color: #f87171; margin-right: 8px; font-weight:bold;">✗</span> Action item: Integrate and build documentation around **{skill.title()}**.', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: #4ade80; font-weight:bold;">✓ Profile demonstrates complete functional keyword coverage. No gaps detected.</span>', unsafe_allow_html=True)
            
        st.markdown('<div style="margin-top: 22px; margin-bottom: 8px; font-weight: 600; color: #818cf8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">🎯 Strategic Recommendations Roadmap</div>', unsafe_allow_html=True)
        if r["final_score"] >= 70:
            st.markdown("🔹 Candidate profile is exceptionally optimized for immediate production deployment.")
        elif r["final_score"] >= 40:
            st.markdown("🔹 Candidate shows strong baseline potential. Recommend progressing with a targeted foundational screening assessment.")
        else:
            st.markdown("🔹 Profile requires deep-level structural upskilling before advancement.")
            
        st.markdown("🔹 Advise candidate to engineer specialized real-world project blocks to back up core competencies.")
        st.markdown("🔹 Recommend providing a public live-deployment link or an active GitHub portfolio grid for verification.")

    with tab3:
        st.markdown("**Targeted Screening Interview Questions**")
        questions = generate_interview_questions(r["candidate_skills"])
        for idx, q in enumerate(questions, 1):
            st.write(f"**Q{idx}:** {q}")

    with tab4:
        st.markdown("**Interactive AI Appraisal Chatbot**")
        user_query = st.text_input("Ask a question about the candidate (e.g., 'What skills are missing?', 'Why consider?'):", key="bot_query")
        if user_query:
            response = recruiter_chatbot(user_query, r["candidate_skills"], r["required_skills"], r["final_score"], r["skill_match"], r["recommendation"])
            st.info(response)


    with tab5:
        st.markdown("**Export Executive Candidate Summary**")
        
        # We read directly from the generated file data fresh inside the tab
        if "pdf_data" in r:
            import time
            # Force a completely unique download file name using a timestamp to break browser caching
            cache_busting_filename = f"{r['job_role'].replace(' ', '_')}_Report_{int(time.time())}.pdf"
            
            st.download_button(
                label="📥 Download PDF Candidate Appraisal Report", 
                data=r["pdf_data"], 
                file_name=cache_busting_filename, 
                mime="application/pdf"
            )
        else:
            st.error("Report compilation payload not found.")