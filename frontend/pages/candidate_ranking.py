import streamlit as st
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

from backend.services.ranking_service import (
    get_all_candidates,
    rank_candidates
)

from backend.services.status_service import (
    save_candidate_status
)

st.title(
    "🏆 Candidate Ranking Engine"
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button(
    "Rank Candidates"
):

    candidates = (
        get_all_candidates()
    )

    skills = [

        skill.strip()

        for skill in
        job_description.split(",")

        if skill.strip()
    ]

    st.session_state["ranked_candidates"] = (
        rank_candidates(
            candidates,
            job_description,
            skills
        )
    )

if "ranked_candidates" in st.session_state:

    ranked = (
        st.session_state[
            "ranked_candidates"
        ]
    )

    st.subheader(
        "Top Candidates"
    )

    for i, candidate in enumerate(
        ranked,
        start=1
    ):

        st.markdown("---")

        st.write(
            f"#{i}"
        )

        st.write(
            candidate["name"]
        )

        st.write(
            candidate["email"]
        )

        st.metric(
            "Final Score",
            f"{candidate['score']}%"
        )

        st.write(
            f"Semantic Match: {candidate['semantic']}%"
        )

        st.write(
            f"Skill Match: {candidate['skills']}%"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "✅ Shortlist",
                key=f"shortlist_{i}"
            ):

                save_candidate_status({

                    "candidate_name":
                        candidate["name"],

                    "candidate_email":
                        candidate["email"],

                    "status":
                        "Shortlisted",

                    "notes":
                        ""
                })

                st.toast(
                    "Candidate status saved"
                )

                st.success(
                    "Candidate Shortlisted"
                )

        with col2:

            if st.button(
                "⏳ Hold",
                key=f"hold_{i}"
            ):

                save_candidate_status({

                    "candidate_name":
                        candidate["name"],

                    "candidate_email":
                        candidate["email"],

                    "status":
                        "Hold",

                    "notes":
                        ""
                })

                st.toast(
                    "Candidate status saved"
                )

                st.warning(
                    "Candidate Put On Hold"
                )

        with col3:

            if st.button(
                "❌ Reject",
                key=f"reject_{i}"
            ):

                save_candidate_status({

                    "candidate_name":
                        candidate["name"],

                    "candidate_email":
                        candidate["email"],

                    "status":
                        "Rejected",

                    "notes":
                        ""
                })

                st.toast(
                    "Candidate status saved"
                )

                st.error(
                    "Candidate Rejected"
                )