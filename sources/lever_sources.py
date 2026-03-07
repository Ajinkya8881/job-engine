import requests
import json
import os
from config import LEVER_COMPANIES_FILE

def get_lever_companies():
    if not os.path.exists(LEVER_COMPANIES_FILE):
        return []
    with open(LEVER_COMPANIES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def lever_jobs():
    companies = get_lever_companies()
    all_jobs = []
    
    for company in companies:
        try:
            url = f"https://api.lever.co/v0/postings/{company}?mode=json"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                jobs = response.json()
                
                for job in jobs:
                    all_jobs.append({
                        "company": company,
                        "title": job.get('text'),
                        "location": job.get('categories', {}).get('location', ''),
                        "url": job.get('hostedUrl'),
                        "description": job.get('descriptionPlain', ''),
                        "source": "Lever"
                    })
        except Exception as e:
            pass
            
    return all_jobs
