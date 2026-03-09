import os
import json
import logging
import google.generativeai as genai
from config import SKILLS, RESUME_DATA
from filters.backend_filter import is_backend

class LLMMatcher:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.logger = logging.getLogger(__name__)
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.logger.info("LLM Matcher initialized with Gemini 2.0 Flash")
            except Exception as e:
                self.logger.error(f"Failed to initialize LLM: {e}")
                self.model = None
        else:
            self.logger.warning("GEMINI_API_KEY not found. LLM features disabled.")
            self.model = None

    def match_job(self, job_title, job_description):
        """
        Analyzes a job description against the user's resume/skills.
        Returns a dict: {"match_score": int, "match_reason": str}
        """
        # 1. Fallback to keyword matching if LLM is not available
        if not self.model:
            is_match = is_backend(job_title)
            return {
                "match_score": 50 if is_match else 10,
                "match_reason": "Basic Keyword Match (LLM Unavailable - Set GEMINI_API_KEY)"
            }
        
        # 2. Construct the prompt
        # We truncate description to avoid token limits and reduce cost/latency
        truncated_desc = job_description[:8000] if job_description else "No description provided."
        
        prompt = f"""
        Act as an expert technical recruiter. Evaluate if the following job is a good match for the candidate.
        
        CANDIDATE PROFILE:
        - Target Role: Junior/Associate Java Backend Engineer
        - Target Experience: 0 to 3 years (ENTRY LEVEL / FRESHER)
        - Key Skills: {', '.join(SKILLS)}
        - Core Tech: Java, Spring Boot, Microservices, SQL, Git
        
        JOB DETAILS:
        - Title: {job_title}
        - Description: {truncated_desc}
        
        CRITICAL EVALUATION STEPS:
        1. EXPERIENCE CHECK: If the job requires 4+ years of experience OR is a 'Senior/Lead/Staff' role, give a score of 0.
        2. TECH STACK: Is it primarily a Java/Backend role? If it is Frontend (React/Angular), iOS, Android, or purely Infrastructure (DevOps/SRE), give a score < 30.
        3. JUNIOR/ENTRY: If the job mentions 'New Grad', 'Junior', 'Associate', 'Intern', or 'Entry level', boost the score.
        
        INSTRUCTIONS:
        - Assign a 'match_score' (0 to 100).
        - 90-100: Java/Spring + 0-2 years exp (Perfect).
        - 70-89: Backend (any stack) + Junior level.
        - 0-39: Senior roles, non-backend, or unrelated fields (Compliance, Business, etc.).
        - Provide a 'match_reason' (max 15 words).
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "match_score": <int>,
            "match_reason": "<string>"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            result = json.loads(response.text)
            return result
        except Exception as e:
            self.logger.error(f"LLM matching failed for '{job_title}': {e}")
            # Fallback on error
            is_match = is_backend(job_title)
            return {
                "match_score": 45 if is_match else 0,
                "match_reason": "LLM Error (Fallback to Keywords)"
            }
