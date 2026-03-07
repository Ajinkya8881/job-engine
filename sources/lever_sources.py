import requests
import json
import os
from config import LEVER_COMPANIES_FILE
from filters.backend_filter import is_backend

def get_lever_companies():
    if not os.path.exists(LEVER_COMPANIES_FILE): return []
    with open(LEVER_COMPANIES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def lever_jobs():
    companies = get_lever_companies()
    all_jobs = []
    session = requests.Session()
    
    for company in companies:
        try:
            url = f"https://api.lever.co/v0/postings/{company}?mode=json"
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                jobs = response.json()
                for job in jobs:
                    title = job.get('text')
                    # Pre-filter to save memory
                    if not is_backend(title): continue
                    
                    # Lever mode=json includes description in 'descriptionPlain' or 'description'
                    desc = job.get('descriptionPlain', '') + " " + job.get('additionalPlain', '')
                    
                    all_jobs.append({
                        "company": company,
                        "title": title,
                        "location": job.get('categories', {}).get('location', 'Remote'),
                        "url": job.get('hostedUrl'),
                        "description": desc, # FULL description captured
                        "source": "Lever"
                    })
        except: pass
    return all_jobs
