# 🚀 Job Engine 2.0 Deployment Guide

This engine now supports 24/7 scanning, LLM-powered matching, and a Kanban dashboard.

## 📦 Docker Deployment (Recommended for 24/7)

1. **Install Docker Desktop**.
2. **Create a `.env` file** in this directory:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   ```
   *(Get a free Gemini API key from Google AI Studio)*

3. **Run the Engine:**
   ```bash
   docker-compose up -d --build
   ```

4. **Access Dashboard:**
   Open [http://localhost:5000](http://localhost:5000)

## 🧠 Features

### 1. LLM-Powered Matching
- **Old Way:** Simple keyword matching (often inaccurate).
- **New Way:** Uses Google Gemini 2.0 Flash to read the job description and compare it with your skills defined in `config.py`.
- **Result:** You get a 0-100 score and a "Why?" reason for every job.

### 2. Kanban Dashboard
- Drag and drop jobs between columns: `New`, `Applied`, `Interview`, `Offer`, `Rejected`.
- Generates **AI Cover Letters** automatically.

### 3. Database
- Migrated from JSON to **SQLite** (`storage/jobs.db`).
- Faster and more reliable for long-running processes.

## 🛠 Manual Run (Without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the engine (scheduler):
   ```bash
   python main.py
   ```
3. Run the dashboard (in a separate terminal):
   ```bash
   python dashboard/app.py
   ```

## 🤖 Auto-Apply Assistant

Run the assistant locally when you are ready to apply:
```bash
python automation/auto_apply.py
```
It will:
- Open a browser.
- Detect if you are on Greenhouse/Lever.
- Inject a "⚡ AUTO-FILL" button to fill your details in 1 click.
