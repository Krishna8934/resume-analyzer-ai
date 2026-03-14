from utils.resume_parser import extract_resume_text
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

# upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# allowed file types
ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    if file and allowed_file(file.filename):

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Extract resume text
        resume_text = extract_resume_text(filepath)

        return jsonify({
            "message": "Resume uploaded successfully",
            "extracted_text_preview": resume_text[:500]   # first 500 characters
        })

    return jsonify({"error": "Only PDF and DOCX allowed"})



if __name__ == "__main__":
    app.run(debug=True)