import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Jobs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            url TEXT,
            location TEXT,
            description TEXT,
            date_posted TEXT,
            source TEXT,
            is_remote BOOLEAN,
            salary TEXT,
            status TEXT DEFAULT 'new',
            match_score INTEGER DEFAULT 0,
            match_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Companies Table (for discovery)
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            name TEXT PRIMARY KEY,
            board_url TEXT,
            ats_provider TEXT,
            last_scraped TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_job(job_data):
    """
    Saves a job to the database. 
    job_data should be a dictionary with keys matching the table columns.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT OR IGNORE INTO jobs (
                id, title, company, url, location, description, 
                date_posted, source, is_remote, salary, 
                status, match_score, match_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_data.get('id'),
            job_data.get('title'),
            job_data.get('company'),
            job_data.get('url'),
            job_data.get('location'),
            job_data.get('description', ''),
            job_data.get('date_posted'),
            job_data.get('source'),
            job_data.get('is_remote', False),
            job_data.get('salary', ''),
            job_data.get('status', 'new'),
            job_data.get('match_score', 0),
            job_data.get('match_reason', '')
        ))
        conn.commit()
        return c.rowcount > 0 # Returns True if a new row was inserted
    except Exception as e:
        print(f"Error saving job {job_data.get('id')}: {e}")
        return False
    finally:
        conn.close()

def job_exists(job_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM jobs WHERE id = ?', (job_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def get_all_jobs(status_filter=None):
    conn = get_db_connection()
    c = conn.cursor()
    if status_filter:
        c.execute('SELECT * FROM jobs WHERE status = ? ORDER BY created_at DESC', (status_filter,))
    else:
        c.execute('SELECT * FROM jobs ORDER BY created_at DESC')
    jobs = [dict(row) for row in c.fetchall()]
    conn.close()
    return jobs

def update_job_status(job_id, new_status):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE jobs SET status = ? WHERE id = ?', (new_status, job_id))
    conn.commit()
    conn.close()

# Initialize DB on import if not exists
if not os.path.exists(DB_PATH):
    init_db()
