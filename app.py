from utils.resume_vs_job import analyze_resume_vs_job
from utils.bullet_point_improver import improve_bullet_point
from utils.ai_analyzer import suggest_resume_improvements
from utils.ai_analyzer import match_job_role
from utils.ai_analyzer import analyze_resume
from utils.resume_parser import extract_resume_text
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

# upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

        resume_text = extract_resume_text(filepath)

        # AI analysis
        analysis = analyze_resume(resume_text)

        return jsonify({
        "message": "Resume analyzed successfully",
        **analysis
        })

@app.route("/match_job", methods=["POST"])
def match_job():

    job_role = request.form.get("job_role")
    resume_file = request.files.get("resume")

    if not job_role or not resume_file:
        return jsonify({"error": "Job role and resume required"})

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(filepath)

    resume_text = extract_resume_text(filepath)

    result = match_job_role(resume_text, job_role)

    return jsonify({
        **result,
        "message": "Job match analysis completed"
    })
    
@app.route("/improve_resume", methods=["POST"])
def improve_resume():

    resume_file = request.files.get("resume")

    if not resume_file:
        return jsonify({"error": "Resume required"})

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(filepath)

    resume_text = extract_resume_text(filepath)

    result = suggest_resume_improvements(resume_text)

    return jsonify({
        **result,
        "message": "Resume improvement suggestions generated"
    })
    
@app.route("/full_analysis", methods=["POST"])
def full_analysis():

    file = request.files["resume"]
    job_role = request.form["job_role"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    resume_text = extract_resume_text(filepath)

    # run all analyses
    ats = analyze_resume(resume_text)
    job_match = match_job_role(resume_text, job_role)
    improvements = suggest_resume_improvements(resume_text)

    result = {
        "ATS_analysis": ats,
        "job_match": job_match,
        "improvements": improvements
    }

    return render_template("analysis_result.html", data=result)

@app.route("/bullet_improver", methods=["GET", "POST"])
def bullet_improver():

    if request.method == "GET":
        return render_template("bullet_improver.html")

    bullet_point = request.form.get("bullet_point")

    if not bullet_point:
        return jsonify({"error": "Bullet point required"})

    result = improve_bullet_point(bullet_point)

    
    return render_template(
        "bullet_improver.html",
        improved=result["improved_bullet_point"]
    )
    
@app.route("/resume_vs_job", methods=["GET","POST"])
def resume_vs_job():

    if request.method == "GET":
        return render_template("resume_vs_job.html")

    job_description = request.form.get("job_description")
    resume_file = request.files.get("resume")

    if not job_description or not resume_file:
        return jsonify({"error": "Resume and job description required"})

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
    resume_file.save(filepath)

    resume_text = extract_resume_text(filepath)

    result = analyze_resume_vs_job(resume_text, job_description)

    return jsonify({
        **result,
        "message": "Resume vs Job analysis completed"
    })
    
if __name__ == "__main__":
    app.run(debug=True)