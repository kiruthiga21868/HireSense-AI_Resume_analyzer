import streamlit as st
import fitz
import sys
import os
import google.generativeai as genai
import json
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from backend.services.ats_service import (
    calculate_semantic_score,
    calculate_skill_score,
    get_missing_skills,
    calculate_project_score,
    calculate_education_score,
    calculate_experience_score,
    calculate_certification_score
)

from backend.services.ats_result_service import (
    save_ats_result
)

from backend.services.ai_feedback_service import (
    generate_ai_feedback
)

from backend.utils.gemini_parser import (
    parse_resume_with_gemini
)

st.title(
    "🎯 ATS Resume Analyzer"
)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Paste Job Description"
)

ranking_data = []

def extract_text_from_pdf(pdf_file):

    text = ""

    pdf = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    return text


if uploaded_files and job_description:

    for uploaded_file in uploaded_files:

        st.markdown("---")

        st.subheader(
            f"📄 {uploaded_file.name}"
        )

        text = extract_text_from_pdf(
            uploaded_file
        )

        candidate = parse_resume_with_gemini(
            text
        )

        resume_skills = candidate.get(
            "skills",
            []
        )

        projects = candidate.get(
            "projects",
            []
        )

        education = candidate.get(
            "education",
            []
        )

        experience_years = candidate.get(
            "years_of_experience",
            0
        )

        certifications = candidate.get(
            "certifications",
            []
        )

        st.write(
            resume_skills
        )

        jd_prompt = f"""
Extract only technical skills from this Job Description.

Return JSON only.

Format:

{{
  "skills":[]
}}

Job Description:

{job_description}
"""

        response = (
            genai.GenerativeModel(
                "gemini-2.5-flash"
            ).generate_content(
                jd_prompt
            )
        )

        cleaned = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        jd_data = json.loads(
            cleaned
        )

        jd_skills = jd_data["skills"]

        st.subheader(
            "JD Skills"
        )

        st.write(
            jd_skills
        )

        semantic_score = (
            calculate_semantic_score(
                text,
                job_description
            )
        )

        skill_score = (
            calculate_skill_score(
                resume_skills,
                jd_skills
            )
        )

        project_score = (
            calculate_project_score(
                projects
            )
        )

        education_score = (
            calculate_education_score(
                education
            )
        )

        experience_score = (
            calculate_experience_score(
                experience_years
            )
        )

        certification_score = (
            calculate_certification_score(
                certifications
            )
        )

        final_score = round(

            semantic_score * 0.30 +

            skill_score * 0.25 +

            project_score * 0.15 +

            education_score * 0.10 +

            experience_score * 0.10 +

            certification_score * 0.10,

            2
        )

        missing_skills = (
            get_missing_skills(
                resume_skills,
                jd_skills
            )
        )

        feedback = (
            generate_ai_feedback(
                text,
                job_description
            )
        )

        save_ats_result({

            "candidate_name":
                candidate.get("name"),

            "candidate_email":
                candidate.get("email"),

            "job_description":
                job_description,

            "semantic_score":
                semantic_score,

            "skill_score":
                skill_score,

            "project_score":
                project_score,

            "education_score":
                education_score,

            "experience_score":
                experience_score,

            "certification_score":
                certification_score,

            "final_score":
                final_score,

            "strengths":
                feedback["strengths"],

            "weaknesses":
                feedback["weaknesses"],

            "recommendations":
                feedback["recommendations"],

            "hiring_decision":
                feedback["hiring_decision"]

        })

        ranking_data.append({
            "Candidate":
                candidate.get("name"),
            "Match Score":
                final_score,
            "Decision":
                feedback["hiring_decision"]
        })

        st.markdown("---")

        st.header(
            f"👤 {candidate.get('name', 'Unknown Candidate')}"
        )

        st.subheader(
            "ATS Results"
        )

        st.metric(
            "Resume Match %",
            f"{final_score}%"
        )

        st.markdown("---")

        st.subheader(
            "📊 Detailed Score Breakdown"
        )

        st.write(
            f"Semantic Match: {semantic_score}%"
        )

        st.write(
            f"Skills Match: {skill_score}%"
        )

        st.write(
            f"Projects Match: {project_score}%"
        )

        st.write(
            f"Education Match: {education_score}%"
        )

        st.write(
            f"Experience Match: {experience_score}%"
        )

        st.write(
            f"Certification Match: {certification_score}%"
        )

        st.subheader(
            "Missing Skills"
        )

        st.write(
            missing_skills
        )

        st.subheader(
            "💪 Strengths"
        )

        for item in feedback["strengths"]:
            st.success(item)

        st.subheader(
            "⚠ Weaknesses"
        )

        for item in feedback["weaknesses"]:
            st.warning(item)

        st.subheader(
            "📈 Recommendations"
        )

        for item in feedback["recommendations"]:
            st.info(item)

        st.subheader(
            "🎯 Hiring Decision"
        )

        st.success(
            feedback["hiring_decision"]
        )

    if ranking_data:

        st.markdown("---")

        st.subheader(
            "🏆 Candidate Ranking Summary"
        )

        ranking_df = pd.DataFrame(
            ranking_data
        )

        ranking_df = ranking_df.sort_values(
            by="Match Score",
            ascending=False
        )

        st.dataframe(
            ranking_df,
            use_container_width=True
        )