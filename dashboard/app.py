from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Add path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import JOBS_DB_FILE, RESUME_DATA

app = Flask(__name__)

def load_jobs():
    if not os.path.exists(JOBS_DB_FILE):
        return []
    with open(JOBS_DB_FILE, 'r') as f:
        return json.load(f)

def save_jobs(jobs):
    with open(JOBS_DB_FILE, 'w') as f:
        json.dump(jobs, f, indent=4)

@app.route('/')
def index():
    all_jobs = load_jobs()
    dashboard_data = {"new": [], "applied": [], "ignored": [], "interview": [], "offer": [], "rejected": []}
    for job in all_jobs:
        status = job.get('status', 'new')
        if status in dashboard_data: dashboard_data[status].append(job)
        else: dashboard_data["new"].append(job)
    
    # Sort: High score first, India first
    dashboard_data["new"].sort(key=lambda x: (x.get('score', 0), x.get('is_preferred_location', False)), reverse=True)
    return render_template('index.html', data=dashboard_data, resume=RESUME_DATA)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    jobs = load_jobs()
    for job in jobs:
        if job['company'] == data.get('company') and job['title'] == data.get('title'):
            job['status'] = data.get('status')
            break
    save_jobs(jobs)
    return jsonify({"success": True})

@app.route('/generate_cover_letter/<company>/<title>')
def generate_cover_letter(company, title):
    letter = (f"Dear Hiring Manager at {company},\n\n"
              f"I am writing to express my interest in the {title} position. "
              f"As a Java Backend Engineer with experience in Spring Boot and Microservices, "
              f"I have built scalable solutions that align with your team's needs.\n\n"
              f"Best regards,\n{RESUME_DATA['first_name']} {RESUME_DATA['last_name']}\n{RESUME_DATA['linkedin']}")
    return jsonify({"letter": letter})

@app.route('/interview_prep/<role>')
def interview_prep(role):
    questions = ["Working of HashMap", "Spring Bean Lifecycle", "Microservices Saga Pattern", "SQL vs NoSQL"]
    return jsonify({"questions": questions})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
