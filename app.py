from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from ai_engine import generate_curriculum
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Import our OpenAI-powered curriculum generator as a distinct alias
from openai_curriculum import generate_curriculum as generate_ai_curriculum

import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    print("Request Recieved")
    user_data = request.json
    print(user_data)
    # curriculum = generate_curriculum(user_data)
    # Call the new OpenAI generator (production-safe)
    curriculum = generate_ai_curriculum(user_data)
    return jsonify(curriculum)

@app.route("/api/download", methods=["POST"])
def download_pdf():
    data = request.json
    filename = "CurricuForge_Output.pdf"

    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(data["program_title"], styles["Heading1"]))
    elements.append(Spacer(1, 10))

    for sem in data["semesters"]:
        elements.append(Paragraph(f"Semester {sem['semester_id']}", styles["Heading2"]))
        elements.append(Spacer(1, 5))

        for course in sem["courses"]:
            elements.append(Paragraph(course["course_name"], styles["Normal"]))
            elements.append(Spacer(1, 4))

    doc.build(elements)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)