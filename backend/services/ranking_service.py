from backend.utils.supabase_client import (
    supabase
)

from backend.services.ats_service import (
    calculate_skill_score,
    calculate_project_score,
    calculate_education_score,
    calculate_experience_score,
    calculate_certification_score,
    calculate_semantic_score
)


def get_all_candidates():

    response = (
        supabase
        .table("candidates")
        .select("*")
        .execute()
    )

    return response.data


def rank_candidates(
    candidates,
    jd_text,
    jd_skills
):

    ranked = []

    for candidate in candidates:

        skills = (
            candidate.get(
                "skills",
                []
            )
            or []
        )

        projects = (
            candidate.get(
                "projects",
                []
            )
            or []
        )

        education = (
            candidate.get(
                "education",
                []
            )
            or []
        )

        experience_years = (
            candidate.get(
                "years_of_experience",
                0
            )
            or 0
        )

        certifications = (
            candidate.get(
                "certifications",
                []
            )
            or []
        )

        candidate_profile = f"""
        Skills:
        {skills}

        Projects:
        {projects}

        Education:
        {education}

        Experience:
        {experience_years}

        Certifications:
        {certifications}
        """

        semantic_score = (
            calculate_semantic_score(
                candidate_profile,
                jd_text
            )
        )

        skill_score = (
            calculate_skill_score(
                skills,
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

        ranked.append({

            "id":
                candidate.get("id"),

            "name":
                candidate.get("name"),

            "email":
                candidate.get("email"),

            "score":
                final_score,

            "semantic":
                semantic_score,

            "skills":
                skill_score

        })

    unique_candidates = {}

    for candidate in ranked:

        email = candidate["email"]

        if email not in unique_candidates:

            unique_candidates[email] = candidate

    ranked = list(
        unique_candidates.values()
    )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked