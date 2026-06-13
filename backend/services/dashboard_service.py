from backend.utils.supabase_client import (
    supabase
)

def get_candidate_statuses():

    response = (
        supabase
        .table(
            "candidate_status"
        )
        .select("*")
        .execute()
    )

    return response.data