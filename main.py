import time
import schedule
import json
import os
import sys
from config import SEEN_JOBS_FILE, JOBS_DB_FILE, MIN_SCORE_TO_ALERT

# Sources
from sources.greenhouse_sources import greenhouse_jobs
from sources.lever_sources import lever_jobs
from sources.api_sources import get_remotive_jobs, get_arbeitnow_jobs, get_jobicy_jobs
from sources.github_sources import get_github_jobs
from sources.yc_sources import get_yc_jobs
from sources.hackernews_sources import get_hackernews_jobs
from sources.company_discovery import run_discovery

# Filters & Ranking
from filters.backend_filter import is_backend
from ranking.job_ranker import calculate_application_score

# Notifier
from notifier.telegram_bot import send_job

def load_seen():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()
    try:
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_seen(seen):
    try:
        with open(SEEN_JOBS_FILE, "w") as f:
            for job in seen:
                f.write(job + "\n")
    except Exception as e:
        print(f"Error saving seen jobs: {e}")

def save_jobs_db(jobs):
    try:
        current_db = []
        if os.path.exists(JOBS_DB_FILE):
            with open(JOBS_DB_FILE, 'r') as f:
                current_db = json.load(f)
        
        db_dict = {f"{j['company']}_{j['title']}": j for j in current_db}
        
        for job in jobs:
            job_id = f"{job['company']}_{job['title']}"
            if job_id not in db_dict:
                db_dict[job_id] = job
            else:
                # Update existing job with new data if needed, or keep old status
                # We want to preserve 'status' if it exists in old job
                old_status = db_dict[job_id].get('status')
                db_dict[job_id] = job
                if old_status:
                    db_dict[job_id]['status'] = old_status
            
        with open(JOBS_DB_FILE, "w") as f:
            json.dump(list(db_dict.values()), f, indent=4)
            
    except Exception as e:
        print(f"Error saving jobs db: {e}")

seen = load_seen()

def run_engine():
    print("Scanning jobs...")
    
    all_jobs = []

    print("Fetching Remotive...")
    all_jobs.extend(get_remotive_jobs())
    print("Fetching Arbeitnow...")
    all_jobs.extend(get_arbeitnow_jobs())
    print("Fetching GitHub...")
    all_jobs.extend(get_github_jobs())
    print("Fetching HackerNews...")
    all_jobs.extend(get_hackernews_jobs())
    print("Fetching YC...")
    all_jobs.extend(get_yc_jobs())
    print("Fetching Greenhouse...")
    all_jobs.extend(greenhouse_jobs())
    print("Fetching Lever...")
    all_jobs.extend(lever_jobs())

    print("TOTAL JOBS FOUND:", len(all_jobs))
    
    processed_jobs = []
    new_jobs_count = 0

    for job in all_jobs:
        if 'description' not in job: job['description'] = ""
        if 'url' not in job: job['url'] = ""
        
        if is_backend(job.get("title", "")):
            from filters.resume_matcher import get_matched_skills
            job['matched_skills'] = get_matched_skills(job.get('description', ''))
            
            score = calculate_application_score(job)
            job['score'] = score
            
            # Default status
            if 'status' not in job:
                job['status'] = 'new'
            
            processed_jobs.append(job)

            job_id = f"{job.get('company')}_{job.get('title')}"
            
            if job_id not in seen:
                if score >= MIN_SCORE_TO_ALERT:
                    print(f"New job: {job.get('title')} at {job.get('company')} (Score: {score})")
                    send_job(job, score)
                    new_jobs_count += 1
                seen.add(job_id)

    print(f"Filtered Backend Jobs: {len(processed_jobs)}")
    print(f"New High Score Jobs: {new_jobs_count}")

    save_seen(seen)
    save_jobs_db(processed_jobs)

schedule.every(10).minutes.do(run_engine)

if __name__ == "__main__":
    print("Job engine running...")

    # Initial Discovery (only runs if file missing or forced, but logic is inside discovery module)
    print("Running initial company discovery...")
    try:
        run_discovery()
    except Exception as e:
        print(f"Initial discovery failed: {e}")

    run_engine() # Run once immediately

    if "--run-once" in sys.argv:
        print("Run-once mode active. Exiting.")
        sys.exit(0)

    while True:
        schedule.run_pending()
        time.sleep(60)
