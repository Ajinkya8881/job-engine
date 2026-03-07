import requests
import re

GITHUB_REPOS = [
    "SimplifyJobs/New-Grad-Positions",
    "SimplifyJobs/Summer2026-Internships"
]

def get_github_jobs():
    jobs = []
    for repo in GITHUB_REPOS:
        try:
            # Using GitHub API to get README content or raw file
            # Easier to use raw content
            url = f"https://raw.githubusercontent.com/{repo}/dev/README.md" # attempting dev branch first
            response = requests.get(url)
            if response.status_code != 200:
                 url = f"https://raw.githubusercontent.com/{repo}/main/README.md"
                 response = requests.get(url)
            
            if response.status_code == 200:
                content = response.text
                # Simple parsing logic - assuming table structure often used in these repos
                # | Company | Role | Location | Application/Link |
                # This is fragile but better than nothing without complex HTML parsing
                
                # Regex to find links in table rows
                # \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|
                
                rows = content.split('\n')
                for row in rows:
                    if "|" in row and "Company" not in row and "---" not in row:
                        parts = [p.strip() for p in row.split('|')]
                        if len(parts) >= 5:
                            company = parts[1]
                            # Remove markdown links from company name
                            company = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', company)
                            
                            role = parts[2]
                            location = parts[3]
                            link_match = re.search(r'\((http.*?)\)', parts[4])
                            link = link_match.group(1) if link_match else ""
                            
                            if link:
                                jobs.append({
                                    "company": company,
                                    "title": role,
                                    "location": location,
                                    "url": link,
                                    "description": f"From {repo}",
                                    "source": "GitHub"
                                })
        except Exception as e:
            print(f"Error fetching from {repo}: {e}")
            
    return jobs
