import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from datetime import datetime


from src.parsing.resume_parser import parse_resume
from src.generate.matcher import calculate_match_score
from src.generate.reviewer import review_resume
from src.search.job_search import search_jobs
from src.mentor.mentor import ask_career_mentor
from src.safety.guardrails import check_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartHire AI",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 SmartHire AI")

    st.caption(
        "AI-Powered Resume Analysis & Career Assistant"
    )

    st.divider()

    st.subheader("📌 Features")

    st.write("📄 Resume Analysis")
    st.write("📊 Job Match Scoring")
    st.write("💼 Dataset-Based Job Search")
    st.write("🤖 AI Resume Review")
    st.write("🎓 AI Career Mentor")
    st.write("📥 Professional Report Export")

    st.divider()

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.subheader("📊 System Status")

    st.success("Resume Analysis: Ready")
    st.success("Semantic Job Search: Ready")
    st.success("AI Career Mentor: Ready")
    st.success("Report Export: Ready")

    st.divider()

    st.subheader("ℹ️ About")

    st.caption(
        "SmartHire AI uses AI and semantic search to analyze "
        "resumes, compare them with job requirements, recommend "
        "relevant jobs from a pre-collected dataset, and provide "
        "career guidance."
    )

    st.divider()

    st.caption(
        "Built with Python • Streamlit • FAISS • Gemini"
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "mentor_answer" not in st.session_state:
    st.session_state.mentor_answer = None

if "mentor_question_saved" not in st.session_state:
    st.session_state.mentor_question_saved = ""


# ============================================================
# PROFESSIONAL HEADER
# ============================================================

st.title("🤖 SmartHire AI")

st.markdown(
    """
### Your AI-Powered Career Intelligence Platform

Analyze your resume, compare it with job requirements,
discover relevant opportunities using semantic search,
and get AI-powered career guidance.
"""
)

st.divider()


# ============================================================
# WORKFLOW BANNER
# ============================================================

st.info(
    "📌 **How it works:** "
    "1️⃣ Upload Resume → "
    "2️⃣ Add Target Job Description → "
    "3️⃣ Analyze Match → "
    "4️⃣ Explore Recommended Jobs → "
    "5️⃣ Get AI Guidance → "
    "6️⃣ Export Your Report"
)


# ============================================================
# RESUME INPUT SECTION
# ============================================================

input_col1, input_col2 = st.columns(2)

with input_col1:

    uploaded_file = st.file_uploader(
        "📄 Upload your resume",
        type=["pdf"],
        help="Upload your resume in PDF format."
    )


with input_col2:

    job_description = st.text_area(
        "💼 Enter Target Job Description",
        height=200,
        placeholder=(
            "Paste the job description you want "
            "your resume to be evaluated against..."
        )
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
):

    if uploaded_file is None:

        st.warning("Please upload a resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner(
            "Analyzing your resume with SmartHire AI..."
        ):

            # ------------------------------------------------
            # Parse Resume
            # ------------------------------------------------

            resume_data = parse_resume(
                "temp_resume.pdf"
            )

            resume_text = resume_data["text"]


            # ------------------------------------------------
            # Match Score
            # ------------------------------------------------

            match_result = calculate_match_score(
                resume_text,
                job_description
            )


            # ------------------------------------------------
            # Search Matching Jobs
            # ------------------------------------------------

            job_results = search_jobs(
                resume_text,
                k=3
            )


            # ------------------------------------------------
            # AI Resume Review
            # ------------------------------------------------

            review = review_resume(
                resume_text,
                job_description
            )


        # ----------------------------------------------------
        # Save Analysis
        # ----------------------------------------------------

        st.session_state.analysis_done = True

        st.session_state.report_data = {
            "resume_data": resume_data,
            "resume_text": resume_text,
            "job_description": job_description,
            "match_result": match_result,
            "job_results": job_results,
            "review": review
        }

        st.session_state.mentor_answer = None
        st.session_state.mentor_question_saved = ""

        st.success(
            "✅ Resume analysis completed successfully!"
        )


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.analysis_done:

    st.markdown("### 🚀 Ready to Analyze Your Resume")

    st.caption(
        "Upload your PDF resume and enter a target job description "
        "to get started."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("### 📄 Resume Analysis")

            st.write(
                "Extract your resume information and identify "
                "your technical skills."
            )


    with col2:

        with st.container(border=True):

            st.markdown("### 💼 Job Intelligence")

            st.write(
                "Discover relevant job opportunities using "
                "semantic search over the job dataset."
            )


    with col3:

        with st.container(border=True):

            st.markdown("### 🎓 Career Guidance")

            st.write(
                "Get AI-powered resume feedback and professional "
                "career guidance."
            )

    st.divider()


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.analysis_done:

    data = st.session_state.report_data

    resume_data = data["resume_data"]
    job_description = data["job_description"]
    match_result = data["match_result"]
    job_results = data["job_results"]
    review = data["review"]


    # ========================================================
    # MAIN TABS
    # ========================================================

    (
        tab_analysis,
        tab_jobs,
        tab_review,
        tab_mentor,
        tab_export
    ) = st.tabs(
        [
            "📄 Resume Analysis",
            "💼 Matching Jobs",
            "🤖 AI Resume Review",
            "🎓 Career Mentor",
            "📥 Export Report"
        ]
    )


    # ========================================================
    # TAB 1 — RESUME ANALYSIS
    # ========================================================

    with tab_analysis:

        st.header("📊 Resume Match Analysis")

        st.caption(
            "Your resume is compared against the target "
            "job description using semantic and skill matching."
        )


        # ----------------------------------------------------
        # Match Metrics
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Match",
                f"{match_result['final_score']:.2f}%"
            )

        with col2:

            st.metric(
                "Semantic Match",
                f"{match_result['semantic_score']:.2f}%"
            )

        with col3:

            st.metric(
                "Skill Match",
                f"{match_result['skill_score']:.2f}%"
            )


        # ----------------------------------------------------
        # Match Interpretation
        # ----------------------------------------------------

        overall_score = match_result["final_score"]

        if overall_score >= 75:

            match_status = "🟢 Strong Match"

            match_message = (
                "Your resume aligns well with the target job. "
                "Focus on refining your resume and highlighting "
                "your most relevant experience and skills."
            )

        elif overall_score >= 50:

            match_status = "🟡 Moderate Match"

            match_message = (
                "Your resume has relevant strengths, but some "
                "important skills or qualifications may need "
                "improvement to better match this role."
            )

        else:

            match_status = "🔴 Low Match"

            match_message = (
                "Your resume currently has significant gaps "
                "compared with the target job requirements. "
                "Review the missing skills and AI suggestions "
                "to improve your profile."
            )


        st.info(
            f"### {match_status}\n\n{match_message}"
        )


        st.divider()


        # ----------------------------------------------------
        # Resume Information
        # ----------------------------------------------------

        st.header("👤 Resume Information")

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.subheader("📋 Personal Details")

                st.write(
                    f"**Name:** "
                    f"{resume_data.get('name', 'N/A')}"
                )

                st.write(
                    f"**Email:** "
                    f"{resume_data.get('email', 'N/A')}"
                )

                st.write(
                    f"**Phone:** "
                    f"{resume_data.get('phone', 'N/A')}"
                )


        with col2:

            with st.container(border=True):

                st.subheader("🛠️ Technical Skills")

                skills = resume_data.get(
                    "skills",
                    []
                )

                if isinstance(skills, str):

                    skills = [skills]

                if skills:

                    skill_text = " • ".join(
                        [
                            f"`{skill}`"
                            for skill in skills
                        ]
                    )

                    st.markdown(skill_text)

                else:

                    st.info(
                        "No technical skills detected."
                    )


        st.divider()


        # ----------------------------------------------------
        # Skill Analysis
        # ----------------------------------------------------

        st.header("🛠️ Skill Analysis")

        col1, col2 = st.columns(2)

        matched_skills = match_result.get(
            "matched_skills",
            []
        )

        missing_skills = match_result.get(
            "missing_skills",
            []
        )


        with col1:

            with st.container(border=True):

                st.subheader("✅ Matched Skills")

                if matched_skills:

                    st.success(
                        ", ".join(matched_skills)
                    )

                else:

                    st.info(
                        "No matching skills found."
                    )


        with col2:

            with st.container(border=True):

                st.subheader("❌ Missing Skills")

                if missing_skills:

                    st.warning(
                        ", ".join(missing_skills)
                    )

                else:

                    st.success(
                        "No missing skills detected."
                    )


    # ========================================================
    # TAB 2 — MATCHING JOBS
    # ========================================================

    with tab_jobs:

        st.header("💼 Matching Job Opportunities")

        st.caption(
            "Jobs are retrieved using semantic search over the "
            "pre-collected job dataset. Lower semantic distance "
            "means a closer match."
        )


        if job_results:

            for i, result in enumerate(
                job_results,
                start=1
            ):

                job_name = result.get(
                    "job",
                    "Unknown Job"
                )

                company = result.get(
                    "company",
                    "Not available"
                )

                city = result.get(
                    "city",
                    ""
                )

                state = result.get(
                    "state",
                    ""
                )

                country = result.get(
                    "country",
                    ""
                )

                job_type = result.get(
                    "job_type",
                    "Not specified"
                )

                category = result.get(
                    "category",
                    "Not specified"
                )

                description = result.get(
                    "description",
                    ""
                )

                url = result.get(
                    "url",
                    ""
                )

                distance = result.get(
                    "distance",
                    0
                )


                # --------------------------------------------
                # Similarity Display
                # --------------------------------------------

                similarity = max(
                    0,
                    min(
                        100,
                        (1 - distance / 2) * 100
                    )
                )


                # --------------------------------------------
                # Build Location
                # --------------------------------------------

                location_parts = [
                    str(part)
                    for part in [
                        city,
                        state,
                        country
                    ]
                    if (
                        part
                        and str(part).lower() != "nan"
                    )
                ]

                location = ", ".join(
                    location_parts
                )

                if not location:

                    location = "Location not available"


                # --------------------------------------------
                # Clean Values
                # --------------------------------------------

                if (
                    not company
                    or str(company).lower() == "nan"
                ):

                    company = "Not available"


                if (
                    not job_type
                    or str(job_type).lower() == "nan"
                ):

                    job_type = "Not specified"


                if (
                    not category
                    or str(category).lower() == "nan"
                ):

                    category = "Not specified"


                # --------------------------------------------
                # JOB CARD
                # --------------------------------------------

                with st.container(border=True):

                    col1, col2 = st.columns(
                        [4, 1]
                    )

                    with col1:

                        st.subheader(
                            f"#{i} — {job_name}"
                        )

                        st.write(
                            f"🏢 **Company:** {company}"
                        )

                        st.write(
                            f"📍 **Location:** {location}"
                        )


                    with col2:

                        st.metric(
                            "Match Score",
                            f"{similarity:.1f}%"
                        )


                    st.progress(
                        similarity / 100
                    )


                    detail_col1, detail_col2 = (
                        st.columns(2)
                    )

                    with detail_col1:

                        st.write(
                            f"💼 **Job Type:** {job_type}"
                        )

                    with detail_col2:

                        st.write(
                            f"📂 **Category:** {category}"
                        )


                    if (
                        description
                        and str(description).lower() != "nan"
                    ):

                        with st.expander(
                            "📄 View Job Description"
                        ):

                            st.write(description)


                    if (
                        url
                        and str(url).startswith("http")
                    ):

                        st.link_button(
                            "🔗 View Original Job Posting",
                            str(url)
                        )


                    st.caption(
                        f"Semantic distance: "
                        f"{distance:.4f} "
                        f"• Lower is better"
                    )


        else:

            st.info(
                "No matching jobs found."
            )


    # ========================================================
    # TAB 3 — AI RESUME REVIEW
    # ========================================================

    with tab_review:

        st.header("🤖 AI Resume Review")

        st.caption(
            "AI-generated suggestions to improve your resume "
            "for the target role."
        )

        with st.container(border=True):

            st.markdown(review)


        st.divider()

        with st.expander(
            "💼 View Target Job Description"
        ):

            st.write(job_description)


    # ========================================================
    # TAB 4 — AI CAREER MENTOR
    # ========================================================

    with tab_mentor:

        st.header("🎓 AI Career Mentor")

        st.caption(
            "Ask career-related questions. Answers are generated "
            "using the project's career knowledge base."
        )


        col1, col2 = st.columns(2)

        with col1:

            st.write("🎯 Career paths")
            st.write("💼 Jobs and roles")
            st.write("📄 Resume improvement")

        with col2:

            st.write("🛠️ Skills to learn")
            st.write("🎤 Interview preparation")
            st.write("🚀 Projects and development")


        mentor_question = st.text_area(
            "💬 Ask your career question",
            height=120,
            placeholder=(
                "Example: How can I become a "
                "Machine Learning Engineer?"
            ),
            key="mentor_question_input"
        )


        if st.button(
            "🤖 Ask AI Career Mentor",
            type="primary"
        ):

            if not mentor_question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                allowed, message = check_question(
                    mentor_question
                )


                if not allowed:

                    st.warning(message)

                    st.info(
                        "The AI Career Mentor only handles "
                        "career, jobs, resumes, interviews, "
                        "skills, internships, projects, and "
                        "professional-development questions."
                    )


                else:

                    with st.spinner(
                        "AI Career Mentor is thinking..."
                    ):

                        try:

                            mentor_answer = (
                                ask_career_mentor(
                                    mentor_question
                                )
                            )

                            st.session_state.mentor_answer = (
                                mentor_answer
                            )

                            st.session_state.mentor_question_saved = (
                                mentor_question
                            )


                        except Exception as e:

                            st.error(
                                "Unable to generate mentor response."
                            )

                            st.caption(
                                f"Error: {str(e)}"
                            )


        if st.session_state.mentor_answer:

            st.success(
                "Career Mentor response generated!"
            )

            st.subheader("💡 Mentor Answer")

            with st.container(border=True):

                st.markdown(
                    st.session_state.mentor_answer
                )


    # ========================================================
    # TAB 5 — EXPORT REPORT
    # ========================================================

    with tab_export:

        st.header("📥 Download / Export Report")

        st.write(
            "Download a professional copy of your complete "
            "SmartHire AI analysis."
        )


        # ----------------------------------------------------
        # Prepare Values
        # ----------------------------------------------------

        current_time = datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )

        candidate_name = resume_data.get(
            "name",
            "Candidate"
        )

        candidate_email = resume_data.get(
            "email",
            "N/A"
        )

        candidate_phone = resume_data.get(
            "phone",
            "N/A"
        )

        overall_score = match_result[
            "final_score"
        ]

        semantic_score = match_result[
            "semantic_score"
        ]

        skill_score = match_result[
            "skill_score"
        ]


        # ----------------------------------------------------
        # Jobs Report
        # ----------------------------------------------------

        jobs_report = ""

        if job_results:

            for i, result in enumerate(
                job_results,
                start=1
            ):

                job_name = result.get(
                    "job",
                    "Unknown Job"
                )

                company = result.get(
                    "company",
                    "Not available"
                )

                distance = result.get(
                    "distance",
                    0
                )

                similarity = max(
                    0,
                    min(
                        100,
                        (1 - distance / 2) * 100
                    )
                )

                jobs_report += (
                    f"{i}. {job_name}\n"
                    f"   Company: {company}\n"
                    f"   Match Score: "
                    f"{similarity:.1f}%\n\n"
                )

        else:

            jobs_report = "No matching jobs found.\n"


        # ----------------------------------------------------
        # Skills Report
        # ----------------------------------------------------

        matched_skills_report = (
            ", ".join(matched_skills)
            if matched_skills
            else "None"
        )

        missing_skills_report = (
            ", ".join(missing_skills)
            if missing_skills
            else "None"
        )


        if isinstance(skills, list):

            technical_skills_report = (
                ", ".join(skills)
                if skills
                else "None detected"
            )

        else:

            technical_skills_report = str(skills)


        # ====================================================
        # PROFESSIONAL REPORT
        # ====================================================

        report = f"""# SmartHire AI
## Professional Resume Analysis Report

---

### Report Information

| Field | Details |
|---|---|
| Candidate | {candidate_name} |
| Email | {candidate_email} |
| Phone | {candidate_phone} |
| Generated On | {current_time} |

---

# 1. Executive Summary

SmartHire AI analyzed the candidate's resume against
the provided job description.

### Overall Match Score

**{overall_score:.2f}%**

### Semantic Match

**{semantic_score:.2f}%**

### Skill Match

**{skill_score:.2f}%**

---

# 2. Skill Analysis

## Matched Skills

{matched_skills_report}

## Missing Skills

{missing_skills_report}

---

# 3. Matching Job Opportunities

{jobs_report}

---

# 4. Resume Information

## Personal Details

**Name:** {candidate_name}

**Email:** {candidate_email}

**Phone:** {candidate_phone}

## Technical Skills

{technical_skills_report}

---

# 5. AI Resume Review

{review}

---

# 6. Career Mentor

"""

        if st.session_state.mentor_answer:

            report += (
                f"## Mentor Question\n\n"
                f"{st.session_state.mentor_question_saved}\n\n"
                f"## Mentor Answer\n\n"
                f"{st.session_state.mentor_answer}\n\n"
            )

        else:

            report += (
                "No career mentor question was submitted "
                "during this analysis session.\n\n"
            )


        report += """---

# 7. Target Job Description

"""

        report += job_description

        report += """

---

## SmartHire AI

*AI-powered resume analysis, semantic job matching,
resume review, and career guidance.*

**End of Report**
"""


        # ====================================================
        # DOWNLOAD BUTTONS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="📄 Download Markdown Report",
                data=report,
                file_name=(
                    f"SmartHire_Report_"
                    f"{candidate_name.replace(' ', '_')}.md"
                ),
                mime="text/markdown",
                use_container_width=True
            )


        with col2:

            st.download_button(
                label="📝 Download Text Report",
                data=report,
                file_name=(
                    f"SmartHire_Report_"
                    f"{candidate_name.replace(' ', '_')}.txt"
                ),
                mime="text/plain",
                use_container_width=True
            )


        with st.expander(
            "👁️ Preview Exported Report"
        ):

            st.markdown(report)