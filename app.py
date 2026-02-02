from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key from Environment Variable
openai.api_key = os.getenv("OPENAI_API_KEY")


# ------------------------
# HOME ROUTE (TEST)
# ------------------------

@app.route("/")
def home():
    return "AI Career Guide API is running 🚀"


# ------------------------
# MAIN AI API ROUTE
# ------------------------

@app.route("/api/recommend", methods=["POST"])
def career_guide():

    data = request.get_json()

    interest = data.get("interest", [])
    experience = data.get("experience", "")
    skills = data.get("skills", [])

    # ------------------------
    # RULE BASED ENGINE (FAST)
    # ------------------------

    if experience == "beginner" and "automation" in interest:
        base_career = "AI Automation Specialist"

    elif experience == "advanced" and "python" in skills:
        base_career = "Machine Learning Engineer"

    else:
        base_career = "Prompt Engineer"


    # ------------------------
    # GPT PROMPT
    # ------------------------

    prompt = f"""
User Profile:
Experience: {experience}
Skills: {skills}
Interests: {interest}

Base career suggestion: {base_career}

Generate:

1) Short explanation (2 lines)
2) Learning roadmap (5 steps)
3) Time estimate to become job-ready
"""


    # ------------------------
    # OPENAI CALL
    # ------------------------

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert AI career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=400
        )

        ai_reply = response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        ai_reply = "AI service temporarily unavailable."


    # ------------------------
    # FINAL RESPONSE
    # ------------------------

    return jsonify({
        "rule_based_career": base_career,
        "ai_recommendation": ai_reply,
        "status": "success"
    })


# ------------------------
# RUN SERVER
# ------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
