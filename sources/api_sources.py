import requests
import re

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
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://remoteok.com/api"
        response = requests.get(url, headers=headers, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
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

def get_relocateme_jobs():
    """Great for jobs that provide Visa Sponsorship."""
    try:
        # Relocate.me doesn't have a public API, but we can search for common patterns
        # For now, we'll use a placeholder or scrape if we had selenium in CI.
        # Since we don't, we'll stick to robust APIs.
        return []
    except: return []

def get_jobspresso_jobs():
    """High quality remote jobs."""
    try:
        # Jobspresso RSS
        return [] # Placeholder for RSS logic
    except: return []

def get_workingnomads_jobs():
    """Back-end focus."""
    try:
        url = "https://www.workingnomads.com/jobsapi/job/_search?q=category:dev&size=50"
        # They have a hidden API
        resp = requests.get(url, timeout=10)
        jobs = []
        if resp.status_code == 200:
            data = resp.json()
            for hit in data.get('hits', {}).get('hits', []):
                item = hit.get('_source', {})
                jobs.append({
                    "company": item.get('company_name', 'Unknown'),
                    "title": item.get('title', 'Unknown'),
                    "location": "Remote",
                    "url": "https://www.workingnomads.com/jobs/" + str(item.get('id')),
                    "description": item.get('description', ''),
                    "source": "WorkingNomads"
                })
        return jobs
    except: return []
