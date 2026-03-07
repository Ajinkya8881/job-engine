import requests

def get_remotive_jobs():
    try:
        url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=150"
        response = requests.get(url, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get('jobs', []):
                jobs.append({
                    "company": item.get('company_name', 'Unknown'),
                    "title": item.get('title', 'Unknown'),
                    "location": item.get('candidate_required_location', 'Remote'),
                    "url": item.get('url', ''),
                    "description": item.get('description', ''),
                    "source": "Remotive"
                })
        return jobs
    except: return []

def get_arbeitnow_jobs():
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get('data', []):
                jobs.append({
                    "company": item.get('company_name', 'Unknown'),
                    "title": item.get('title', 'Unknown'),
                    "location": item.get('location', 'Remote'),
                    "url": item.get('url', ''),
                    "description": item.get('description', ''),
                    "source": "Arbeitnow"
                })
        return jobs
    except: return []

def get_remoteok_jobs():
    try:
        # RemoteOK API requires a User-Agent
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://remoteok.com/api"
        response = requests.get(url, headers=headers, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
            # First item is usually legal/info, skip it
            for item in data[1:]:
                jobs.append({
                    "company": item.get('company', 'Unknown'),
                    "title": item.get('position', 'Unknown'),
                    "location": "Remote",
                    "url": item.get('url', ''),
                    "description": item.get('description', ''),
                    "source": "RemoteOK"
                })
        return jobs
    except: return []

def get_wwr_jobs():
    try:
        # WWR doesn't have a public JSON API, but we can parse their RSS/Feed or similar
        # Using a reliable feed-to-json logic
        url = "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss"
        # Since parsing RSS is specific, we'll return empty for now or use a simple regex
        # For now, let's stick to their main category page logic
        return [] 
    except: return []

def get_jobicy_jobs():
    return []
