import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

from backend.services.analytics_service import (
    get_candidates,
    get_ats_results,
    get_candidate_status
)

st.title(
    "📈 Recruitment Analytics Center"
)

# -----------------------------
# Load Data
# -----------------------------

candidates = pd.DataFrame(
    get_candidates()
)

ats_results = pd.DataFrame(
    get_ats_results()
)

statuses = pd.DataFrame(
    get_candidate_status()
)

# -----------------------------
# Handle Empty Data
# -----------------------------

if candidates.empty:

    st.warning(
        "No candidate records found."
    )

    st.stop()

# -----------------------------
# KPI Cards
# -----------------------------

total_candidates = len(
    candidates
)

average_ats = 0

if (
    not ats_results.empty
    and "final_score" in ats_results.columns
):

    average_ats = round(
        ats_results[
            "final_score"
        ].mean(),
        2
    )

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Candidates",
        total_candidates
    )

with col2:

    st.metric(
        "Average ATS Score",
        average_ats
    )

# -----------------------------
# Hiring Funnel
# -----------------------------

shortlisted = 0
hold = 0
rejected = 0

if (
    not statuses.empty
    and "status" in statuses.columns
):

    shortlisted = len(
        statuses[
            statuses["status"]
            ==
            "Shortlisted"
        ]
    )

    hold = len(
        statuses[
            statuses["status"]
            ==
            "Hold"
        ]
    )

    rejected = len(
        statuses[
            statuses["status"]
            ==
            "Rejected"
        ]
    )

st.markdown("---")

funnel_df = pd.DataFrame(
    {
        "Status": [
            "Shortlisted",
            "Hold",
            "Rejected"
        ],
        "Count": [
            shortlisted,
            hold,
            rejected
        ]
    }
)

st.subheader(
    "📊 Hiring Funnel"
)

fig = px.pie(
    funnel_df,
    names="Status",
    values="Count",
    title="Candidate Status Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Top Skills
# -----------------------------

all_skills = []

if "skills" in candidates.columns:

    for skills in candidates["skills"]:

        if not skills:
            continue

        for skill in skills:

            if isinstance(
                skill,
                dict
            ):

                all_skills.append(
                    skill.get(
                        "name",
                        str(skill)
                    )
                )

            else:

                all_skills.append(
                    str(skill)
                )

# Debug Output
st.write(
    "Skills Debug:",
    all_skills
)

skill_counts = Counter(
    all_skills
)

top_skills = (
    pd.DataFrame(
        skill_counts.items(),
        columns=[
            "Skill",
            "Count"
        ]
    )
    .sort_values(
        by="Count",
        ascending=False
    )
    .head(10)
)

st.markdown("---")

st.subheader(
    "🏆 Top Skills"
)

if not top_skills.empty:

    fig = px.bar(
        top_skills,
        x="Skill",
        y="Count",
        title="Top Skills Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No skills data available."
    )

# -----------------------------
# Top Certifications
# -----------------------------

all_certs = []

if "certifications" in candidates.columns:

    for certs in candidates["certifications"]:

        if not certs:
            continue

        for cert in certs:

            if isinstance(
                cert,
                dict
            ):

                all_certs.append(
                    cert.get(
                        "name",
                        cert.get(
                            "title",
                            str(cert)
                        )
                    )
                )

            else:

                all_certs.append(
                    str(cert)
                )

# Debug Output
st.write(
    "Certifications Debug:",
    all_certs
)

cert_counts = Counter(
    all_certs
)

top_certs = (
    pd.DataFrame(
        cert_counts.items(),
        columns=[
            "Certification",
            "Count"
        ]
    )
    .sort_values(
        by="Count",
        ascending=False
    )
    .head(10)
)

st.markdown("---")

st.subheader(
    "📜 Top Certifications"
)

if not top_certs.empty:

    fig = px.bar(
        top_certs,
        x="Certification",
        y="Count",
        title="Certification Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No certification data available."
    )

st.markdown("---")

st.subheader(
    "📈 ATS Score Distribution"
)

if (
    not ats_results.empty
    and "final_score" in ats_results.columns
):

    fig = px.histogram(
        ats_results,
        x="final_score",
        nbins=10,
        title="ATS Score Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

if (
    not ats_results.empty
    and "final_score" in ats_results.columns
    and "candidate_name" in ats_results.columns
):

    top_candidates = (
        ats_results
        .sort_values(
            by="final_score",
            ascending=False
        )
        .head(10)
    )

    st.subheader(
        "🏅 Top Candidates"
    )

    fig = px.bar(
        top_candidates,
        x="candidate_name",
        y="final_score",
        title="Top Candidate Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
       

st.markdown("---")

st.subheader(
    "🎯 Skill Gap Analysis"
)

least_common = (
    pd.DataFrame(
        skill_counts.items(),
        columns=[
            "Skill",
            "Count"
        ]
    )
    .sort_values(
        by="Count"
    )
    .head(10)
)

if not least_common.empty:

    fig = px.bar(
        least_common,
        x="Skill",
        y="Count",
        title="Rare Skills In Talent Pool"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# -----------------------------
# Recruiter Insight
# -----------------------------

st.markdown("---")

st.subheader(
    "🧠 Recruiter Insight"
)

if not top_skills.empty:

    st.success(
        f"""
Most common skill in your talent pool:
{top_skills.iloc[0]['Skill']}
"""
    )

else:

    st.info(
        "Not enough data to generate insights."
    )