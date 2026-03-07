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
    
    # Organize by status
    dashboard_data = {
        "new": [],
        "applied": [],
        "interview": [],
        "offer": [],
        "rejected": []
    }
    
    for job in all_jobs:
        status = job.get('status', 'new')
        dashboard_data[status].append(job)
        
    # Sort New jobs by score
    dashboard_data["new"].sort(key=lambda x: (x.get('score', 0), x.get('is_preferred_location', False), x.get('is_high_salary', False)), reverse=True)
    
    return render_template('index.html', data=dashboard_data, resume=RESUME_DATA)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    company = data.get('company')
    title = data.get('title')
    new_status = data.get('status')
    
    jobs = load_jobs()
    for job in jobs:
        if job['company'] == company and job['title'] == title:
            job['status'] = new_status
            break
    save_jobs(jobs)
    return jsonify({"success": True})

@app.route('/generate_cover_letter/<company>/<title>')
def generate_cover_letter(company, title):
    # Template-based "AI" generation
    letter = (
        f"Dear Hiring Manager at {company},\n\n"
        f"I am writing to express my strong interest in the {title} position. "
        f"As a Backend Engineer specializing in Java, Spring Boot, and Microservices, "
        f"I have been following {company}'s work and admire your engineering culture.\n\n"
        f"In my recent projects, I have architected scalable APIs using Spring Boot and deployed them via Docker, "
        f"reducing deployment time by 40%. My experience with Kafka for event-driven architecture "
        f"aligns well with the requirements of this role.\n\n"
        f"I am eager to bring my problem-solving skills (honed through DSA) and my passion for clean code to your team. "
        f"Thank you for considering my application.\n\n"
        f"Sincerely,\n{RESUME_DATA['first_name']} {RESUME_DATA['last_name']}\n{RESUME_DATA['linkedin']}"
    )
    return jsonify({"letter": letter})

@app.route('/interview_prep/<role>')
def interview_prep(role):
    # Static "AI" Knowledge Base
    questions = [
        "Explain the internal working of HashMap in Java.",
        "What is the difference between @Controller and @RestController in Spring Boot?",
        "How do you handle database transactions in Microservices? (Saga Pattern)",
        "Explain the Bean Lifecycle in Spring.",
        "What are the differences between SQL and NoSQL? When to use which?",
        "How does Kafka ensure message ordering?",
        "Design a URL Shortener (System Design basic).",
        "What is the difference between Process and Thread?"
    ]
    return jsonify({"questions": questions})

@app.route('/auto_apply_top', methods=['POST'])
def auto_apply_top():
    all_jobs = load_jobs()
    # Filter for new, high-score jobs
    to_apply = [j for j in all_jobs if j.get('status', 'new') == 'new' and j.get('score', 0) >= 50]
    to_apply.sort(key=lambda x: x['score'], reverse=True)
    
    applied_count = 0
    # Import the auto_apply function (we'll need to modify it slightly for this use case)
    from automation.auto_apply import fill_greenhouse, fill_lever
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    options = EdgeOptions()
    # options.add_argument("--headless") # Run in background if you want
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    for job in to_apply[:5]: # Top 5 only
        try:
            driver.get(job['url'])
            if "greenhouse.io" in driver.current_url:
                fill_greenhouse(driver)
            elif "lever.co" in driver.current_url:
                fill_lever(driver)
            
            # Update status in our DB
            job['status'] = 'applied'
            applied_count += 1
            time.sleep(2) # Breath
        except:
            continue
            
    driver.quit()
    save_jobs(all_jobs)
    return jsonify({"success": True, "applied": applied_count})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
