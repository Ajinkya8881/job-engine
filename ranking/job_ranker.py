import re
from filters.resume_matcher import get_matched_skills
from config import SKILLS

def calculate_application_score(job):
    title = (job.get('title') or '').lower()
    desc = (job.get('description') or '').lower()
    loc = (job.get('location') or '').lower()
    
    # --- 1. EXPERIENCE HARD FILTER (0-3 Years Only) ---
    exp_patterns = [
        r"(\d+)\s*\-\s*\d+\s*yrs", 
        r"(\d+)\s*\+\s*years", 
        r"(\d+)\s*to\s*\d+\s*yrs",
        r"(\d+)\s*years?\s*exp"
    ]
    
    for pattern in exp_patterns:
        match = re.search(pattern, desc + " " + title)
        if match:
            years = int(match.group(1))
            if years > 3: return 0 

    if any(k in title for k in ["senior", "lead", "principal", "staff", "architect"]):
        return 0

    # --- 2. SKILL INTELLIGENCE ---
    # Add generic tech to help entry-level roles score > 0
    matched = get_matched_skills(desc + " " + title)
    # Give points for 'Backend', 'API', 'REST' if found
    for extra in ["backend", "api", "rest", "developer"]:
        if extra in desc + " " + title and extra not in [m.lower() for m in matched]:
            matched.append(extra.capitalize())
            
    job['matched_skills'] = matched
    
    # Identify Missing Skills
    job['missing_skills'] = [s for s in ["AWS", "Kubernetes", "Docker", "Kafka", "Redis", "Microservices"] if s.lower() in desc and s.lower() not in [m.lower() for m in matched]]

    # --- 3. SCORING ---
    skill_score = len(matched) * 10 
    
    # Entry Level Bonus (Added 'Associate' and 'L1')
    role_bonus = 0
    if any(k in title for k in ["fresher", "intern", "graduate", "junior", "trainee", "sde-1", "sde-i", "associate", "engineer i"]):
        role_bonus = 40
    elif "sde" in title or "software engineer" in title:
        role_bonus = 15

    total_score = skill_score + role_bonus
    
    # --- 4. PREFERENCES (Hyper-Focused India) ---
    india_hubs = ["hyderabad", "pune", "bangalore", "bengaluru", "india", "gurgaon", "noida", 
                  "hitech city", "gachibowli", "kondapur", "madhapur", "magarpatta", "hinjewadi", "whitefield"]
    job['is_preferred_location'] = any(hub in loc for hub in india_hubs)
    
    salary_match = re.search(r"(\d+)\s*(lpa|lakh|k|USD|\$)", desc)
    job['salary_est'] = salary_match.group(0) if salary_match else "N/A"
    job['visa_sponsorship'] = any(k in desc for k in ["sponsorship", "visa", "relocation", "h1b"])

    if job['is_preferred_location']: total_score += 20
    if job['visa_sponsorship']: total_score += 15

    return min(100, total_score)
