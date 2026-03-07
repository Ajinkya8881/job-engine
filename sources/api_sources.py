import requests

def get_remotive_jobs():
    try:
        url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=150"
        response = requests.get(url, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get('jobs', []):
                # NO MORE FILTERS. We take everything.
                jobs.append({
                    "company": item.get('company_name', 'Unknown'),
                    "title": item.get('title', 'Unknown'),
                    "location": item.get('candidate_required_location', 'Remote'),
                    "url": item.get('url', ''),
                    "description": item.get('description', ''),
                    "source": "Remotive"
                })
        return jobs
    except Exception as e:
        print(f"Error fetching Remotive jobs: {e}")
    return []

def get_arbeitnow_jobs():
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, timeout=10)
        jobs = []
        if response.status_code == 200:
            data = response.json()
            for item in data.get('data', []):
                # Taking everything from Arbeitnow
                jobs.append({
                    "company": item.get('company_name', 'Unknown'),
                    "title": item.get('title', 'Unknown'),
                    "location": item.get('location', 'Remote'),
                    "url": item.get('url', ''),
                    "description": item.get('description', ''),
                    "source": "Arbeitnow"
                })
        return jobs
    except Exception as e:
        print(f"Error fetching Arbeitnow jobs: {e}")
    return []

def get_jobicy_jobs():
    # Placeholder for future Jobicy API integration
    return []
