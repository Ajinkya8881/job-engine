import os

# Use environment variables for security
# On your laptop, you can set these or just keep them here for local use 
# BUT for GitHub, we will use "Secrets"
BOT_TOKEN = os.getenv("BOT_TOKEN", "8772510865:AAGqfz_5J2zrqO1FJtixQ3PzUbQWc__EXso")
CHAT_ID = os.getenv("CHAT_ID", "860544852")

# Resume Data
RESUME_DATA = {
    "first_name": "Ajinkya",
    "last_name": "Kolhe",
    "email": "aj.kolhe9657@gmail.com",
    "phone": "+919657817634",
    "linkedin": "https://www.linkedin.com/in/ajinkya-kolhe-9543b9263",
    "github": "https://github.com/Ajinkya8881",
    "portfolio": "",
    "resume_path": os.path.join(os.getcwd(), "resume.pdf")
}

# ... rest of config ...
# (keeping the rest of the logic same)
LOCATIONS = ["Hyderabad", "Pune", "Bangalore", "Gurgaon", "Remote", "India"]
EXPERIENCE_LEVEL = "Fresher"
SEEN_JOBS_FILE = "storage/seen_jobs.txt"
JOBS_DB_FILE = "storage/jobs_db.json"
GREENHOUSE_COMPANIES_FILE = "company_lists/greenhouse_companies.txt"
LEVER_COMPANIES_FILE = "company_lists/lever_companies.txt"
YC_COMPANIES_FILE = "company_lists/yc_companies.txt"

BACKEND_KEYWORDS = [
    "backend", "software engineer", "java", "spring", "api", 
    "microservices", "platform engineer", "developer", "engineer",
    "fresher", "junior", "associate", "graduate", "trainee", "intern",
    "sde", "sde-1", "sde-i", "sde-ii", "software development engineer"
]

EXCLUDE_KEYWORDS = [
    "senior", "lead", "principal", "manager", "staff", "head of", "director", "architect",
    "frontend", "front-end", "react", "angular", "vue", "ios", "android",
    "mobile", "qa", "quality assurance", "test", "sales", "marketing",
    "product manager", "designer", "contract", "hr", "talent acquisition", "recruiter",
    "communications", "mba", "phd", "audit", "tax", "finance", "legal", "sourcing",
    "business development", "content", "video", "treasury", "controller", "auditor"
]

SKILLS = ["Java", "Spring", "Spring Boot", "MySQL", "SQL", "Git", "GitHub", "Postman", "REST API", "Docker", "Kafka", "Microservices", "DSA"]

WEIGHTS = {"resume_match": 0.4, "recency": 0.2, "reputation": 0.1, "backend_relevance": 0.2, "remote": 0.1, "location_match": 0.3}
MIN_SCORE_TO_ALERT = 40
