import requests
import json
import os
from config import GREENHOUSE_COMPANIES_FILE
from filters.backend_filter import is_backend

def get_greenhouse_companies():
    if not os.path.exists(GREENHOUSE_COMPANIES_FILE):
        return []
    with open(GREENHOUSE_COMPANIES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def greenhouse_jobs():
    companies = get_greenhouse_companies()
    all_jobs = []
    
    # Using a session for slightly faster connection reuse
    session = requests.Session()
    
    for company in companies:
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            response = session.get(url, timeout=4)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                
                for job in jobs:
                    title = job.get('title')
                    
                    # 1. First Pass Filter: Title Only
                    # If title looks irrelevant (HR, Marketing), skip fetching description
                    if not is_backend(title):
                        continue
                        
                    # 2. Fetch Description (The "Reading" part)
                    # Greenhouse API provides 'content' if we fetch specific job ID
                    # or we can rely on title for speed.
                    # But user wants "match with description".
                    # The list endpoint DOES NOT give content. We must fetch individual job.
                    # This is slow: 1 request per job.
                    # Optimization: Only fetch if title is HIGHLY promising.
                    
                    job_id = job.get('id')
                    detail_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs/{job_id}"
                    
                    try:
                        detail_resp = session.get(detail_url, timeout=3)
                        if detail_resp.status_code == 200:
                            detail = detail_resp.json()
                            description = (detail or {}).get('content', '') or title # Fallback if content is None
                        else:
                            description = title # Fallback
                    except:
                        description = title
                        
                    all_jobs.append({
                        "company": company,
                        "title": title,
                        "location": job.get('location', {}).get('name', ''),
                        "url": job.get('absolute_url'),
                        "description": description, 
                        "source": "Greenhouse"
                    })
        except Exception as e:
            pass
            
    return all_jobs
