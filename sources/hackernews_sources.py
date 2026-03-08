import requests
import re
from datetime import datetime

def get_hackernews_jobs():
    jobs = []
    try:
        # 1. Find the latest "Who is hiring" thread
        stories_url = "https://hacker-news.firebaseio.com/v0/user/whoishiring/submitted.json"
        stories = requests.get(stories_url).json()
        
        latest_hiring_id = None
        for story_id in stories[:5]:
            resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            if resp.status_code != 200: continue
            item = resp.json()
            if not item: continue
            if "who is hiring" in (item.get('title') or '').lower():
                latest_hiring_id = story_id
                break
        
        if not latest_hiring_id:
            return []

        # 2. Fetch comments (job posts)
        # Only fetching top 50 for speed, can increase
        resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{latest_hiring_id}.json")
        if resp.status_code != 200: return []
        item_data = resp.json()
        if not item_data: return []
        kids = item_data.get('kids', [])
        
        for comment_id in kids[:60]: 
            try:
                resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{comment_id}.json")
                if resp.status_code != 200: continue
                comment = resp.json()
                if not comment: continue
                text = comment.get('text', '')
                if not text: continue
                
                # Simple filter before processing
                if any(k in text.lower() for k in ["java", "backend", "engineer", "sde", "software"]):
                    
                    # Extract Company (First line often)
                    lines = text.split('<p>')
                    first_line = lines[0].replace("&#x2F;", "/").replace("&#x27;", "'")
                    company = first_line.split('|')[0][:50]
                    
                    # Heuristic for URL
                    url_match = re.search(r'href="(.*?)"', text)
                    url = url_match.group(1) if url_match else f"https://news.ycombinator.com/item?id={comment_id}"
                    
                    jobs.append({
                        "company": company,
                        "title": "Software Engineer (HN)", # Generic title as HN posts vary
                        "location": "Remote / Global",
                        "url": url,
                        "description": text, # Raw HTML text
                        "source": "HackerNews"
                    })
            except:
                continue

    except Exception as e:
        print(f"Error fetching HackerNews jobs: {e}")
        
    return jobs
