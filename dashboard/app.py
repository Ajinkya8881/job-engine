from flask import Flask, render_template, request, jsonify
import sys
import os

# Add path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RESUME_DATA
import storage.database as db

app = Flask(__name__)

@app.route('/')
def index():
    jobs = db.get_all_jobs()
    
    # Kanban Columns
    columns = {
        "new": [], 
        "applied": [], 
        "interview": [], 
        "offer": [], 
        "rejected": []
    }
    
    for job in jobs:
        status = job.get('status', 'new')
        if status not in columns:
            status = 'new' # Default fallback
        columns[status].append(job)
    
    # Sort 'new' by match_score desc
    columns["new"].sort(key=lambda x: x.get('match_score', 0), reverse=True)
    
    return render_template('index.html', columns=columns, resume=RESUME_DATA)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    job_id = data.get('id')
    new_status = data.get('status')
    
    if job_id and new_status:
        db.update_job_status(job_id, new_status)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/generate_cover_letter/<id>')
def generate_cover_letter(id):
    # TODO: Use LLM for this
    # For now, return a template
    jobs = db.get_all_jobs()
    job = next((j for j in jobs if j['id'] == id), None)
    if not job: return jsonify({"letter": "Job not found"})
    
    letter = (f"Dear Hiring Manager at {job['company']},\n\n"
              f"I am writing to express my interest in the {job['title']} position. "
              f"As a Backend Engineer with experience in Java, Spring Boot, and Microservices, "
              f"I have built scalable solutions that align with your team's needs.\n\n"
              f"Best regards,\n{RESUME_DATA['first_name']} {RESUME_DATA['last_name']}\n{RESUME_DATA['linkedin']}")
    return jsonify({"letter": letter})

if __name__ == '__main__':
    # Listen on all interfaces for Docker access
    app.run(debug=True, host='0.0.0.0', port=5000)
