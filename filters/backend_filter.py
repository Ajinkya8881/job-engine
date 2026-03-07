from config import BACKEND_KEYWORDS, EXCLUDE_KEYWORDS

def is_backend(title):
    if not title:
        return False
        
    title_lower = title.lower()
    
    # --- 1. Hard Excludes (HR, MBA, Sales, Communications) ---
    for k in EXCLUDE_KEYWORDS:
        if k in title_lower:
            return False

    # --- 2. Required Tech Check ---
    # The job MUST contain at least one core tech keyword.
    # We remove "intern" from this list here so it can't pass the filter ALONE.
    tech_keywords = [
        "backend", "software engineer", "java", "spring", "api", 
        "microservices", "developer", "engineer", "sde", "trainee"
    ]
    
    is_tech = any(k in title_lower for k in tech_keywords)
    
    if not is_tech:
        return False

    # --- 3. Final Role Match (Backend, SDE, Engineer) ---
    for k in BACKEND_KEYWORDS:
        if k in title_lower:
            return True

    return False
