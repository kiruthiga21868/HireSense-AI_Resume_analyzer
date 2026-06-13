from backend.services.embedding_service import (
    generate_embedding
)

from backend.services.chroma_service import (
    search_candidates
)

from backend.services.recruiter_context_service import (
    get_recruiter_context
)

import google.generativeai as genai


def retrieve_candidates(
    query
):

    query_embedding = (
        generate_embedding(
            query
        )
    )

    results = (
        search_candidates(
            query_embedding,
            top_k=5
        )
    )

    return results


def generate_answer(
    query,
    context
):

    prompt = f"""
You are HireSense AI.

You are an expert recruitment intelligence assistant.

Use ONLY the information provided.

You can:

- Compare candidates
- Recommend candidates
- Analyze ATS scores
- Analyze candidate status
- Analyze skills
- Analyze projects
- Analyze certifications

Question:

{query}

Context:

{context}

Provide a recruiter-focused answer.
"""

    response = (
        genai.GenerativeModel(
            "gemini-2.5-flash"
        ).generate_content(
            prompt
        )
    )

    return response.text


def ask_recruiter_bot(
    query
):

    results = (
        retrieve_candidates(
            query
        )
    )

    vector_context = "\n\n".join(
        results["documents"][0]
    )

    db_context = (
        get_recruiter_context()
    )

    context = f"""

Candidate Profiles:

{vector_context}

Candidates:

{db_context['candidates']}

ATS Results:

{db_context['ats_results']}

Candidate Status:

{db_context['candidate_status']}
"""

    answer = (
        generate_answer(
            query,
            context
        )
    )

    return answer