from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

print("OPENAI KEY LOADED:", bool(openai.api_key))


@app.route("/")
def home():
    return "AI Career Guide API Running 🚀"


# -------------------------
# MAIN AI ENGINE
# -------------------------

@app.route("/api/recommend", methods=["POST"])
def ai_engine():

    try:
        data = request.get_json()

        interest = data.get("interest", [])
        experience = data.get("experience", "")
        skills = data.get("skills", [])
        resume_text = data.get("resume", "")


        # -------------------------
        # Rule Based Baseline
        # -------------------------

        if experience == "beginner" and "automation" in interest:
            base_role = "AI Automation Specialist"
        elif experience == "advanced" and "python" in skills:
            base_role = "Machine Learning Engineer"
        else:
            base_role = "Prompt Engineer"


        # -------------------------
        # AI PROMPT
        # -------------------------

        prompt = f"""
User Career Profile:

Experience Level: {experience}
Skills: {skills}
Interests: {interest}
Resume: {resume_text}

Target Role: {base_role}

Generate response in JSON with keys:

career_summary
learning_roadmap (5 steps)
skill_gaps
resume_improvements
learning_resources
job_ready_score (0-100)
time_estimate
"""


        ai_data = {
            "career_summary": "AI unavailable",
            "learning_roadmap": [],
            "skill_gaps": [],
            "resume_improvements": [],
            "learning_resources": [],
            "job_ready_score": 0,
            "time_estimate": "Unknown"
        }


        # -------------------------
        # OpenAI Call
        # -------------------------

        if openai.api_key:

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI career coach. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=500
            )

            raw = response["choices"][0]["message"]["content"]

            try:
                import json
                ai_data = json.loads(raw)
            except:
                ai_data["career_summary"] = raw


        # -------------------------
        # FINAL RESPONSE
        # -------------------------

        return jsonify({
            "base_role": base_role,
            "ai_results": ai_data,
            "status": "success"
        })


    except Exception as e:
        print("SERVER ERROR:", e)

        return jsonify({
            "status": "error",
            "message": "Backend crashed"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
