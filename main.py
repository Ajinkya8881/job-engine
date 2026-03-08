import time
import schedule
import json
import os
import sys
from config import SEEN_JOBS_FILE, JOBS_DB_FILE, MIN_SCORE_TO_ALERT

# Sources
from sources.greenhouse_sources import greenhouse_jobs
from sources.lever_sources import lever_jobs
from sources.api_sources import get_remotive_jobs, get_arbeitnow_jobs, get_jobicy_jobs, get_remoteok_jobs, get_wwr_jobs
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
    if not os.path.exists(SEEN_JOBS_FILE): return set()
    try:
        with open(SEEN_JOBS_FILE, "r") as f: return set(f.read().splitlines())
    except: return set()

def save_seen(seen):
    try:
        with open(SEEN_JOBS_FILE, "w") as f:
            for job in seen: f.write(job + "\n")
    except: pass

def save_jobs_db(jobs):
    try:
        current_db = []
        if os.path.exists(JOBS_DB_FILE):
            with open(JOBS_DB_FILE, 'r') as f: current_db = json.load(f)
        db_dict = {f"{j['company']}_{j['title']}": j for j in current_db}
        for job in jobs:
            job_id = f"{job['company']}_{job['title']}"
            if job_id not in db_dict: db_dict[job_id] = job
            else:
                old_status = db_dict[job_id].get('status')
                db_dict[job_id] = job
                if old_status: db_dict[job_id]['status'] = old_status
        with open(JOBS_DB_FILE, "w") as f: json.dump(list(db_dict.values()), f, indent=4)
    except: pass

seen = load_seen()

def run_engine():
    print("--- 🚀 FULL ENGINE SCAN STARTING ---")
    all_jobs = []
    
    # 1. API Sources
    print("[1/7] Fetching Remotive...")
    all_jobs.extend(get_remotive_jobs())
    print("[2/7] Fetching Arbeitnow...")
    all_jobs.extend(get_arbeitnow_jobs())
    print("[3/7] Fetching RemoteOK, Jobicy, WWR...")
    all_jobs.extend(get_remoteok_jobs())
    all_jobs.extend(get_jobicy_jobs())
    all_jobs.extend(get_wwr_jobs())
    
    # 2. Tech Sources
    print("[4/7] Fetching GitHub Job Trackers...")
    all_jobs.extend(get_github_jobs())
    print("[5/7] Fetching HackerNews 'Who is Hiring'...")
    all_jobs.extend(get_hackernews_jobs())
    
    # 3. Venture/Board Sources
    print("[6/7] Fetching YC Startup Jobs...")
    all_jobs.extend(get_yc_jobs())
    print("[7/7] Fetching 100+ Greenhouse/Lever Boards...")
    all_jobs.extend(greenhouse_jobs())
    all_jobs.extend(lever_jobs())

    print(f"--- TOTAL FOUND: {len(all_jobs)} ---")
    
    processed_jobs = []
    new_jobs_count = 0

    for job in all_jobs:
        if not job: continue
        if job.get('description') is None: job['description'] = ""
        if job.get('url') is None: job['url'] = ""
        if job.get('title') is None: job['title'] = "Unknown"
        if job.get('company') is None: job['company'] = "Unknown"
        
        if is_backend(job.get("title", "")):
            from filters.resume_matcher import get_matched_skills
            job['matched_skills'] = get_matched_skills(job.get('description') or '')
            score = calculate_application_score(job)
            job['score'] = score
            if 'status' not in job: job['status'] = 'new'
            processed_jobs.append(job)

            job_id = f"{job.get('company')}_{job.get('title')}"
            if job_id not in seen:
                if score >= MIN_SCORE_TO_ALERT:
                    print(f"🔥 NEW HIGH MATCH: {job.get('title')} @ {job.get('company')} ({score})")
                    send_job(job, score)
                    new_jobs_count += 1
                seen.add(job_id)

    print(f"Matched: {len(processed_jobs)} | New Alerts: {new_jobs_count}")
    save_seen(seen)
    save_jobs_db(processed_jobs)

schedule.every(10).minutes.do(run_engine)

if __name__ == "__main__":
    print("Job Discovery Engine Running...")
    
    # Discovery Expansion
    try: run_discovery()
    except: pass

    run_engine() # Start first scan

    if "--run-once" in sys.argv:
        print("Done. Exiting CI mode.")
        sys.exit(0)

    while True:
        schedule.run_pending()
        time.sleep(60)
