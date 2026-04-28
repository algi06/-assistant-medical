from flask import Flask, request, jsonify
from assistant_medical_ai import AssistantMedicalAI

app = Flask(__name__)
assistant = AssistantMedicalAI()

@app.route("/")
def home():
    return "Assistant médical en ligne OK"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("message", "")
    reponse = assistant.ask(question)
    return jsonify({"response": reponse})
