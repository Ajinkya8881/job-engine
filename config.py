import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOT_TOKEN = os.getenv("BOT_TOKEN", "8772510865:AAGqfz_5J2zrqO1FJtixQ3PzUbQWc__EXso")
CHAT_ID = os.getenv("CHAT_ID", "860544852")

RESUME_DATA = {
    "first_name": "Ajinkya",
    "last_name": "Kolhe",
    "email": "aj.kolhe9657@gmail.com",
    "phone": "9657817634", # Removed +91 here to handle formatting in bot
    "country_code": "+91",
    "linkedin": "https://www.linkedin.com/in/ajinkya-kolhe-9543b9263",
    "github": "https://github.com/Ajinkya8881",
    "portfolio": "",
    "resume_path": os.path.join(BASE_DIR, "resume.pdf"),
    
    # Standard Answers for common questions
    "current_company": "Fresher / Student",
    "current_title": "Software Engineer",
    "work_authorization": "No", # For US companies
    "sponsorship_required": "Yes", # For global roles
    "previously_employed": "No",
    "heard_about_us": "LinkedIn",
    "gender": "Male",
    "race": "Asian",
    "specialty": "Backend"
}

SEEN_JOBS_FILE = os.path.join(BASE_DIR, "storage", "seen_jobs.txt")
JOBS_DB_FILE = os.path.join(BASE_DIR, "storage", "jobs_db.json")
GREENHOUSE_COMPANIES_FILE = os.path.join(BASE_DIR, "company_lists", "greenhouse_companies.txt")
LEVER_COMPANIES_FILE = os.path.join(BASE_DIR, "company_lists", "lever_companies.txt")
YC_COMPANIES_FILE = os.path.join(BASE_DIR, "company_lists", "yc_companies.txt")

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

MIN_SCORE_TO_ALERT = 40
