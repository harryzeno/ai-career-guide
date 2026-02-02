from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "AI Career Guide API is running 🚀"

@app.route("/api/recommend", methods=["POST"])
def career_guide():

    data = request.json

    interest = data.get("interest", [])
    experience = data.get("experience", "")
    skills = data.get("skills", [])

    # RULE ENGINE (FAST FILTER)
    if experience == "beginner" and "automation" in interest:
        base_career = "AI Automation Specialist"
    elif experience == "advanced" and "python" in skills:
        base_career = "Machine Learning Engineer"
    else:
        base_career = "Prompt Engineer"

    # GPT PROMPT
    prompt = f"""
User info:
Experience: {experience}
Skills: {skills}
Interests: {interest}

Suggested base career: {base_career}

Generate:
1) Short explanation
2) Learning roadmap (5 steps)
3) Estimated time to job ready
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_reply = response.choices[0].message.content

    except Exception as e:
        ai_reply = "AI service temporarily unavailable."

    return jsonify({
        "rule_based_career": base_career,
        "ai_recommendation": ai_reply,
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
