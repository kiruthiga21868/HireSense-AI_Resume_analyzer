from backend.utils.supabase_client import (
    supabase
)

def save_ats_result(data):

    supabase.table(
        "ats_results"
    ).insert(
        data
    ).execute()