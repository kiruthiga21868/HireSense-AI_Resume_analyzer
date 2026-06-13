from backend.utils.supabase_client import (
    supabase
)

def save_candidate_status(data):

    return (
        supabase
        .table("candidate_status")
        .insert(data)
        .execute()
    )