# 🤖 SmartHire GenAI

An AI-powered career intelligence platform that analyzes resumes, calculates job match scores, recommends relevant jobs using semantic search, provides AI-generated resume feedback, and offers a RAG-based AI career mentor.

---

## 🚀 Features

### 📄 Resume Analysis
- Upload resumes in PDF format
- Extract candidate information such as:
  - Name
  - Email
  - Phone number
  - Technical skills
- Extract and preprocess resume text

### 📊 Job Match Scoring
- Compare a resume with a target job description
- Calculate:
  - Overall Match Score
  - Semantic Match Score
  - Skill Match Score
- Identify matched and missing skills

### 💼 Semantic Job Search
- Search relevant jobs using vector embeddings
- FAISS-based similarity search
- Displays:
  - Job title
  - Company
  - Location
  - Job type
  - Category
  - Job description
  - Semantic match score
  - Original job posting link

### 🤖 AI Resume Review
Uses Google Gemini to generate:

- Strengths
- Missing Skills
- Weaknesses
- Suggestions for improvement

### 🎓 AI Career Mentor
A Retrieval-Augmented Generation (RAG) based career assistant that provides guidance about:

- Career paths
- Jobs and roles
- Resume improvement
- Skills to learn
- Interview preparation
- Internships
- Projects
- Professional development

### 🛡️ Safety Guardrails
The Career Mentor is restricted to career-related topics such as:

- Jobs
- Careers
- Resumes
- Interviews
- Skills
- Internships
- Projects
- Professional development

### 📥 Professional Report Export
Generate and download complete analysis reports containing:

- Candidate information
- Match scores
- Skill analysis
- Matching jobs
- AI resume review
- Career mentor conversation
- Target job description

Reports can be downloaded in:

- Markdown (`.md`)
- Text (`.txt`)

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Google Gemini API | AI resume review |
| LangChain | RAG pipeline |
| FAISS | Vector similarity search |
| Sentence Transformers | Text embeddings |
| Hugging Face | Embedding model |
| PyPDF | PDF resume text extraction |
| NumPy | Numerical operations |
| Python-dotenv | Environment variable management |

---

## 🏗️ Project Architecture

```text
SmartHire-GenAI
│
├── app/
│   └── main.py                 # Streamlit application
│
├── data/
│   ├── career_notes/           # Knowledge base for AI Career Mentor
│   └── jobs/                   # Job dataset
│
├── src/
│   ├── parsing/                # Resume parsing and preprocessing
│   ├── generate/               # Match scoring and AI review
│   ├── search/                 # Semantic job search
│   ├── mentor/                 # RAG-based career mentor
│   ├── safety/                 # Career question guardrails
│   └── vectorstore/            # Embeddings and FAISS indexing
│
├── tests/                      # Project test files
│
├── vectorstore/                # FAISS indexes and metadata
│
├── requirements.txt
├── .gitignore
└── README.md

Application Workflow

                ┌─────────────────┐
                │   Upload Resume │
                │      PDF        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Resume Parsing  │
                │ & Text Extraction│
                └────────┬────────┘
                         │
                         ▼
          ┌─────────────────────────────┐
          │ Enter Target Job Description│
          └──────────────┬──────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Match Scoring     │
              │ Semantic + Skills   │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
 ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
 │ Skill        │ │ Job Search   │ │ Gemini AI    │
 │ Analysis     │ │ FAISS Search │ │ Resume Review│
 └──────────────┘ └──────────────┘ └──────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ AI Career Mentor│
                │   RAG + Safety  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Professional    │
                │ Report Export   │
                └─────────────────┘