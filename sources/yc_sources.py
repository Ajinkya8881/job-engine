import requests
from config import YC_COMPANIES_FILE
import os

def get_yc_companies():
    if not os.path.exists(YC_COMPANIES_FILE):
        return []
    with open(YC_COMPANIES_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_yc_jobs():
    companies = get_yc_companies()
    jobs = []
    
    for company in companies:
        # heuristic: try greenhouse first
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                for j in data.get('jobs', []):
                    jobs.append({
                        "company": company,
                        "title": j.get('title'),
                        "location": j.get('location', {}).get('name', ''),
                        "url": j.get('absolute_url'),
                        "description": "YC Startup Job",
                        "source": "YC (Greenhouse)"
                    })
                continue # Found board, skip to next company
        except:
            pass
            
        # try lever
        try:
            url = f"https://api.lever.co/v0/postings/{company}?mode=json"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                for j in data:
                    jobs.append({
                        "company": company,
                        "title": j.get('text'),
                        "location": j.get('categories', {}).get('location', ''),
                        "url": j.get('hostedUrl'),
                        "description": "YC Startup Job",
                        "source": "YC (Lever)"
                    })
        except:
            pass

    return jobs
