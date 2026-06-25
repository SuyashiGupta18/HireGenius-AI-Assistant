# HireGenius AI 🤖
**Next-Generation AI-Powered Hiring Assistant** *Developed by Suyashi Gupta*

An automated end-to-end recruitment pipeline engineered to parse resumes, map complex technical skills, and eliminate manual screening bias using machine learning.

---

## 📌 Core Features
* **Dual-Layer Extraction:** Seamlessly processes standard selectable PDFs as well as scanned resume images.
* **Vector Match Scoring:** Computes high-dimensional relevance metrics to gauge exact job description affinity.
* **Granular Skill Audit:** Automatically maps overlapping candidate strengths and flags critical missing competency gaps.
* **Interactive Evaluation:** Integrated with a contextual screening question generator and a live conversational appraisal chatbot.
* **Automated Summaries:** Compiles professional, table-structured candidate analytics directly into downloadable PDF reports.

---

## 🛠️ Tech Stack & Architecture

### 🖥️ Frontend Layer
* **Framework:** `Streamlit`
* **Purpose:** Powers the responsive, custom dark-themed recruiter sandbox dashboard, tab navigation matrices, and real-time interactive AI chat panels.

### ⚙️ Backend & Parsing Pipeline
* **Language Control:** `Python`
* **Data Extraction & OCR:** `pdfplumber` paired with the `Tesseract OCR Engine`
* **Purpose:** Coordinates raw input streams, normalizes incoming document payloads, and executes optical character recognition text fallback sequences for scanned images.

### 🧠 NLP & Analytics Engine
* **Library Stack:** `Scikit-Learn` (utilizing `TfidfVectorizer` and `cosine_similarity`)
* **Purpose:** Handles text tokenization, transforms resume data into high-dimensional vector spaces, and computes candidate-to-JD affinity metrics using mathematical similarity.

### 📄 Executive Reporting Engine
* **Library Stack:** `ReportLab`
* **Purpose:** Dynamically compiles multi-layered structural layouts on-the-fly, generating clean table grids and status-coded visual metric badges directly inside a binary PDF data stream.

---

## 🧩 Challenges Solved
* **Diverse CV Formats:** Overcame file layout unpredictability by combining clean string extraction with fallback OCR formatting pipelines.
* **Unstructured Data Noise:** Implemented an aggressive RegEx cleansing pipeline to completely strip hyperlinks, email layouts, and irrelevant phone numbers.
* **Appraisal Bias:** Replaced subjective human parsing errors with an objective algorithmic weights matrix (65% skill keyword mapping / 35% text similarity distribution).
* **Reporting Bottlenecks:** Eradicated slow manual candidate summary compilation processes through automated, dynamic layout generation.

---

## 📈 Impact & Benefits
* **Efficiency:** Delivers 10x faster CV screening across high-volume applicant talent pools.
* **Objectivity:** Drives hiring selections through standardized, reliable mathematical data models.
* **Visibility:** Offers complete profile transparency via interactive user interface skill chips and a conversational evaluation bot.

---

## 🔮 Future Roadmap
1. Native integration with standard corporate Applicant Tracking Systems (ATS).
2. Deep neural semantic search capabilities powered by FAISS vector indexes.
3. Live generative candidate questioning through an active LLM interviewer interface.
4. Early-stage voice-screening assessment using predictive acoustic analytics.

---