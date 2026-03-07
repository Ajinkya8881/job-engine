from config import BACKEND_KEYWORDS, EXCLUDE_KEYWORDS

def is_backend(title):
    if not title: return False
    title_lower = title.lower()
    
    # 1. Hard Excludes (No HR, No MBA, No Sales, No Success)
    for k in EXCLUDE_KEYWORDS:
        if k in title_lower: return False

    # 2. Tech Role Requirement
    # A job MUST be a coding role.
    core_roles = ["engineer", "developer", "sde", "programmer", "backend", "software", "java"]
    is_core_tech = any(role in title_lower for role in core_roles)
    
    if not is_core_tech:
        return False

    # 3. Match your specific keywords
    for k in BACKEND_KEYWORDS:
        if k in title_lower: return True

    return False
