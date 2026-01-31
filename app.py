from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Career Guide API is running 🚀"

@app.route("/career", methods=["POST"])
def career_guide():
    data = request.json
    interest = data.get("interest")

    response = f"You should explore careers related to {interest}"

    return jsonify({"suggestion": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
