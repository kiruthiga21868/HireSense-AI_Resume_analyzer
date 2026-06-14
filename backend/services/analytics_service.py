from backend.utils.supabase_client import (
    supabase
)

def get_candidates():

    return (
        supabase
        .table("candidates")
        .select("*")
        .execute()
    ).data


def get_ats_results():

    return (
        supabase
        .table("ats_results")
        .select("*")
        .execute()
    ).data


def get_candidate_status():

    return (
        supabase
        .table("candidate_status")
        .select("*")
        .execute()
    ).data