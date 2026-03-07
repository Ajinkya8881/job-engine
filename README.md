# Ajinkya's Job Engine 🚀

A fully automated Java Backend & SDE job discovery platform tailored for freshers in India (Hyderabad/Pune) and global remote roles.

## Features

- **24/7 Scanning:** Runs every 6 hours via GitHub Actions.
- **Multi-Source:** Fetches from Greenhouse, Lever, YC, HackerNews, GitHub, and multiple APIs.
- **Intelligent Scoring:** Scores roles (0-100) based on **Skills (Java, Spring Boot, etc.)** and **Fresher status**.
- **Smart Experience Filter:** Specifically targets roles for 0-3 years of experience.
- **Dual-View Dashboard:** Separate columns for **India Headquarters** (Hyderabad, Pune, Bangalore) and **Global Opportunities**.
- **One-Click Auto-Apply:** Integrated Selenium bot to autofill applications for top matches.
- **AI Career Tools:** Built-in Cover Letter generator and Interview Prep questions.

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Ajinkya8881/job-engine.git
   cd job-engine
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `config.py`:**
   Add your Telegram `BOT_TOKEN` and `CHAT_ID`.

4. **Run the Engine:**
   ```bash
   python main.py
   ```

5. **Open Dashboard:**
   ```bash
   python dashboard/app.py
   ```
   Visit `http://localhost:5000` in Edge.

## Architecture

- `sources/`: Scrapers for various platforms.
- `filters/`: Logic for backend role detection.
- `ranking/`: Scoring algorithm with "Missing Skills" intelligence.
- `automation/`: Selenium scripts for form filling.
- `dashboard/`: Flask-based Command Center.

## GitHub Actions

The engine is cloud-ready. To activate:
1. Go to your Repo Settings -> Secrets and variables -> Actions.
2. Add `BOT_TOKEN` and `CHAT_ID`.
3. The bot will automatically scan and push new jobs to your repo while you sleep!
