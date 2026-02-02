from flask import Flask, request, jsonify

app = Flask(__name__)

# Health Check Route
@app.route("/")
def home():
    return "AI Career Guide API is running 🚀"

# Career Recommendation API
@app.route("/api/recommend", methods=["POST"])
def career_guide():

    data = request.json

    interest = data.get("interest", [])
    experience = data.get("experience", "")
    skills = data.get("skills", [])

    # RULE BASED LOGIC (Starter Engine)
    if experience == "beginner" and "automation" in interest:
        career = "AI Automation Specialist"
    elif experience == "advanced" and "python" in skills:
        career = "Machine Learning Engineer"
    elif "design" in interest:
        career = "AI UI/UX Designer"
    else:
        career = "Prompt Engineer"

    roadmap = [
        "Learn Python fundamentals",
        "Understand AI basics",
        "Practice small AI projects",
        "Build portfolio",
        "Apply for jobs/internships"
    ]

    return jsonify({
        "recommended_career": career,
        "roadmap": roadmap,
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
