import time
import schedule
import sys
import logging
import os
from dotenv import load_dotenv
from config import MIN_SCORE_TO_ALERT

# Load environment variables from .env
load_dotenv()

# Storage
import storage.database as db

# Sources
from sources.greenhouse_sources import greenhouse_jobs
from sources.lever_sources import lever_jobs
from sources.api_sources import get_remotive_jobs, get_arbeitnow_jobs, get_jobicy_jobs, get_remoteok_jobs, get_wwr_jobs
from sources.github_sources import get_github_jobs
from sources.yc_sources import get_yc_jobs
from sources.hackernews_sources import get_hackernews_jobs
from sources.company_discovery import run_discovery

# Filters
from filters.backend_filter import is_backend
from filters.llm_matcher import LLMMatcher

# Notifier
from notifier.telegram_bot import send_job

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Matcher
matcher = LLMMatcher()

def run_engine():
    logger.info("--- 🚀 FULL ENGINE SCAN STARTING ---")
    all_jobs = []
    
    try:
        # 1. API Sources
        logger.info("[1/7] Fetching Remotive...")
        all_jobs.extend(get_remotive_jobs() or [])
        
        logger.info("[2/7] Fetching Arbeitnow...")
        all_jobs.extend(get_arbeitnow_jobs() or [])
        
        logger.info("[3/7] Fetching RemoteOK, Jobicy, WWR...")
        all_jobs.extend(get_remoteok_jobs() or [])
        all_jobs.extend(get_jobicy_jobs() or [])
        all_jobs.extend(get_wwr_jobs() or [])
        
        # 2. Tech Sources
        logger.info("[4/7] Fetching GitHub Job Trackers...")
        all_jobs.extend(get_github_jobs() or [])
        
        logger.info("[5/7] Fetching HackerNews 'Who is Hiring'...")
        all_jobs.extend(get_hackernews_jobs() or [])
        
        # 3. Venture/Board Sources
        logger.info("[6/7] Fetching YC Startup Jobs...")
        all_jobs.extend(get_yc_jobs() or [])
        
        logger.info("[7/7] Fetching Greenhouse/Lever Boards...")
        all_jobs.extend(greenhouse_jobs() or [])
        all_jobs.extend(lever_jobs() or [])

    except Exception as e:
        logger.error(f"Error during fetching sources: {e}")

    logger.info(f"--- TOTAL FOUND: {len(all_jobs)} ---")
    
    new_jobs_count = 0
    
    for job in all_jobs:
        if not job: continue
        
        # Normalize Data
        title = job.get('title', 'Unknown')
        company = job.get('company', 'Unknown')
        description = job.get('description', '')
        url = job.get('url', '')
        
        # 1. Quick Keyword Filter (Save LLM tokens & time)
        # Only process Backend/Software Engineer roles
        if not is_backend(title):
            continue
            
        # 2. Check Deduplication
        # Create a consistent ID (slug-like)
        safe_company = "".join(x for x in company if x.isalnum())
        safe_title = "".join(x for x in title if x.isalnum())
        job_id = f"{safe_company}_{safe_title}".lower()[:255] # truncate if too long
        
        if db.job_exists(job_id):
            continue

        # 3. LLM Match (With small delay for Gemini Free Tier)
        time.sleep(4)
        match_result = matcher.match_job(title, description)
        score = match_result['match_score']
        reason = match_result['match_reason']
        
        # 4. Save to DB
        job_data = {
            'id': job_id,
            'title': title,
            'company': company,
            'url': url,
            'location': job.get('location', ''),
            'description': description,
            'date_posted': job.get('date_posted', ''),
            'source': job.get('source', 'Unknown'),
            'is_remote': job.get('is_remote', False),
            'salary': job.get('salary', ''),
            'status': 'new',
            'match_score': score,
            'match_reason': reason
        }
        
        saved = db.save_job(job_data)
        
        # 5. Alert
        if saved and score >= MIN_SCORE_TO_ALERT:
            logger.info(f"🔥 NEW MATCH: {title} @ {company} ({score}) - {reason}")
            try:
                # Add score/reason to job dict for the notifier
                job['score'] = score
                job['match_reason'] = reason
                send_job(job, score)
                new_jobs_count += 1
            except Exception as e:
                logger.error(f"Failed to send alert: {e}")

    logger.info(f"Scan complete. New High Matches: {new_jobs_count}")

# Schedule
schedule.every(10).minutes.do(run_engine)

if __name__ == "__main__":
    logger.info("Job Discovery Engine Running (SQLite + LLM Powered)...")
    
    # Discovery Expansion
    try: 
        logger.info("Running Company Discovery...")
        run_discovery()
    except Exception as e: 
        logger.error(f"Discovery failed: {e}")

    # Initial Run
    run_engine()

    if "--run-once" in sys.argv:
        logger.info("Done. Exiting (Run-Once Mode).")
        sys.exit(0)

    # Loop
    while True:
        schedule.run_pending()
        time.sleep(60)
