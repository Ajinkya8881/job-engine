import re
from filters.resume_matcher import get_matched_skills
from config import SKILLS

def calculate_application_score(job):
    desc = job.get('description', '').lower()
    title = job.get('title', '').lower()
    loc = job.get('location', '').lower()
    
    # --- 1. EXPERIENCE HARD FILTER (Allowed: 0-3 years) ---
    exp_found = re.search(r"(\d+)\s*\+?\s*years", desc)
    if exp_found:
        years = int(exp_found.group(1))
        if years > 3: return 0 

    # --- 2. SKILL INTELLIGENCE ---
    matched = get_matched_skills(desc)
    job['matched_skills'] = matched
    
    # Identify Missing Skills (Skills in config NOT in desc)
    job['missing_skills'] = [s for s in SKILLS if s.lower() not in desc]

    # --- 3. SCORING LOGIC ---
    # Skills are worth 10 points each
    score = len(matched) * 10 
    
    # Role / Fresher Bonus
    if any(k in title for k in ["fresher", "intern", "graduate", "junior", "trainee", "sde-1", "sde-i"]):
        score += 30
    
    # --- 4. PREFERENCES & BADGES ---
    job['is_preferred_location'] = any(city.lower() in loc for city in ["hyderabad", "pune", "bangalore", "india", "gurgaon"])
    
    # Salary Detection (LPA / Lakh / $)
    salary_match = re.search(r"(\d+)\s*(lpa|lakh|k|USD|\$)", desc)
    job['salary_est'] = salary_match.group(0) if salary_match else "N/A"
    
    # Visa Sponsorship Detection
    job['visa_sponsorship'] = any(k in desc for k in ["sponsorship", "visa", "relocation", "h1b", "tier 2"])

    # --- 5. BOOSTS ---
    if job['is_preferred_location']: score += 20
    if job['visa_sponsorship']: score += 15
    if job['salary_est'] != "N/A": score += 10

    return min(100, score)
