from config import SKILLS

def score_job(text):
    if not text:
        return 0
        
    text_lower = text.lower()
    score = 0
    matched_skills = []

    for skill in SKILLS:
        # Simple whole-word match attempt or just string inclusion
        # "java" in "javascript" is a problem. 
        # But for MVP, string match is okay. Better: Check boundaries.
        if skill.lower() in text_lower:
            score += 5  # 5 points per skill match
            matched_skills.append(skill)
            
    # Normalize score? E.g. 10 skills = 50 points.
    return score

def get_matched_skills(text):
    if not text:
        return []
        
    text_lower = text.lower()
    matched = []
    
    for skill in SKILLS:
        if skill.lower() in text_lower:
            matched.append(skill)
            
    return matched
