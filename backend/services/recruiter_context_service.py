from backend.utils.supabase_client import (
    supabase
)

def get_recruiter_context():

    candidates = (
        supabase
        .table("candidates")
        .select("*")
        .execute()
    )

    ats_results = (
        supabase
        .table("ats_results")
        .select("*")
        .execute()
    )

    candidate_status = (
        supabase
        .table("candidate_status")
        .select("*")
        .execute()
    )

    return {
        "candidates":
            candidates.data,

        "ats_results":
            ats_results.data,

        "candidate_status":
            candidate_status.data
    }