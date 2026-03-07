import re
from filters.resume_matcher import get_matched_skills
from filters.backend_filter import is_backend
from config import SKILLS

def calculate_application_score(job):
    desc = job.get('description', '').lower()
    
    # --- 1. Experience Check (Strict) ---
    exp_found = re.search(r"(\d+)\s*\+?\s*years", desc)
    if exp_found:
        years = int(exp_found.group(1))
        if years > 3:
            return 0 

    # --- 2. Skill Analysis ---
    matched = get_matched_skills(desc)
    
    # Calculate Missing Skills (Simple set difference)
    # We check for all skills in our config. If it's in the desc but NOT in matched (which is same),
    # Wait, 'matched' finds skills FROM config that ARE in desc.
    # Missing would be: Important keywords in desc that are NOT in config? 
    # Or Skills in Config that are NOT in desc? 
    # Usually users want to know: "Job wants React, I don't have it."
    # But we don't know what the job wants unless we parse the whole text.
    # Let's flip it: We look for common tech keywords in the description.
    # If they are present but NOT in your Resume Skills list (config), that's a "Missing Skill".
    
    common_tech = ["aws", "kubernetes", "docker", "react", "angular", "python", "node", "golang", "redis", "kafka", "cloud", "azure"]
    missing = []
    for tech in common_tech:
        if tech in desc and tech not in [s.lower() for s in SKILLS]:
            missing.append(tech)
            
    job['missing_skills'] = missing
    job['matched_skills'] = matched

    # Base Score
    skill_score = len(matched) * 10 
    
    # --- 3. Role/Fresher Match ---
    title = job.get('title', '').lower()
    role_bonus = 0
    if any(k in title for k in ["fresher", "intern", "graduate", "junior", "trainee"]):
        role_bonus = 30
    elif any(k in title for k in ["software engineer", "sde", "developer"]):
        role_bonus = 15

    final_score = skill_score + role_bonus
    
    # --- 4. Location/Salary Preference ---
    job['is_preferred_location'] = any(city.lower() in job.get('location', '').lower() for city in ["hyderabad", "pune", "india"])
    job['is_high_salary'] = bool(re.search(r"(\d+)\s*(lpa|lakh)", desc))
    
    # Boost for India/Salary
    if job['is_preferred_location']: final_score += 20
    if job['is_high_salary']: final_score += 20
    
    return min(100, final_score) 
