import json
import google.generativeai as genai

def generate_ai_feedback(
    resume_text,
    job_description
):

    prompt = f"""
    You are an expert ATS recruiter.

    Analyze the resume against the job description.

    Return JSON only.

    Format:

    {{
      "strengths": [],
      "weaknesses": [],
      "recommendations": [],
      "hiring_decision": ""
    }}

    Resume:

    {resume_text}

    Job Description:

    {job_description}
    """

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    try:

        response = model.generate_content(
            prompt
        )

    except Exception as e:

        print(
            f"Gemini Error: {e}"
        )

        return {
            "strengths": [
                "AI feedback unavailable"
            ],
            "weaknesses": [
                "Gemini quota exceeded"
            ],
            "recommendations": [
                "Try again later"
            ],
            "hiring_decision":
                "Pending Review"
        }

    cleaned = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(
        cleaned
    )