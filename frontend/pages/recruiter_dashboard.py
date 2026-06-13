import streamlit as st
import pandas as pd
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

from backend.services.dashboard_service import (
    get_candidate_statuses
)

st.title(
    "📊 Recruiter Dashboard"
)

data = (
    get_candidate_statuses()
)

df = pd.DataFrame(
    data
)

if df.empty:

    st.warning(
        "No candidate status records found."
    )

    st.stop()

# Show latest recruiter actions first
if "updated_at" in df.columns:

    df = df.sort_values(
        by="updated_at",
        ascending=False
    )

total = len(df)

shortlisted = len(
    df[
        df["status"]
        ==
        "Shortlisted"
    ]
)

hold = len(
    df[
        df["status"]
        ==
        "Hold"
    ]
)

rejected = len(
    df[
        df["status"]
        ==
        "Rejected"
    ]
)

col1, col2, col3, col4 = (
    st.columns(4)
)

with col1:

    st.metric(
        "Total",
        total
    )

with col2:

    st.metric(
        "Shortlisted",
        shortlisted
    )

with col3:

    st.metric(
        "Hold",
        hold
    )

with col4:

    st.metric(
        "Rejected",
        rejected
    )

st.markdown("---")

st.subheader(
    "✅ Shortlisted Candidates"
)

shortlisted_df = df[
    df["status"]
    ==
    "Shortlisted"
]

st.dataframe(
    shortlisted_df,
    use_container_width=True
)

st.subheader(
    "⏳ Hold Candidates"
)

hold_df = df[
    df["status"]
    ==
    "Hold"
]

st.dataframe(
    hold_df,
    use_container_width=True
)

st.subheader(
    "❌ Rejected Candidates"
)

rejected_df = df[
    df["status"]
    ==
    "Rejected"
]

st.dataframe(
    rejected_df,
    use_container_width=True
)