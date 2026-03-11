# X-extractor

Automated pipeline to collect, evaluate, and route high-signal AI/Dev insights from X (Twitter).

## 🚀 Overview

X-extractor monitors X for valuable technical content using scraping, filters it for quality using Gemini 2.0 Flash, and automatically routes the results to your knowledge bases (Obsidian, Gemini CLI, Claude Code, and Telegram).

## 🛠 Features

- **Playwright-based Scraping**: Bypasses expensive X API v2 costs.
- **AI Intelligence**: Uses `gemini-flash-latest` to score utility (1-10) and classify content.
- **Multi-Agent Support**: Automatically updates `GEMINI.md` and `CLAUDE.md` with new principles.
- **Knowledge Sync**: Generates Obsidian notes and sends Telegram notifications for manual reviews.

---

## 📋 Step-by-Step Setup

### 1. Prerequisites
- **Python 3.12+** installed.
- **Node.js** (required for Playwright).
- **Gemini API Key**: Get one at [aistudio.google.com](https://aistudio.google.com).
- **Telegram Bot**: Create one via [@BotFather](https://t.me/botfather).

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/heeshin174/X-extractor.git
cd X-extractor/04_ACTIVE/X-extractor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
Edit `.env`:
- `GEMINI_API_KEY`: Your Google AI SDK key.
- `TELEGRAM_BOT_TOKEN`: From BotFather.
- `TELEGRAM_CHAT_ID`: Your chat ID.
- `OBSIDIAN_VAULT_PATH`: Full path to your local Obsidian vault.

### 4. X (Twitter) Login
To avoid bot detection, the collector uses a stored session.
1. Run the collector script once in headful mode (manually modify `collector.py` to `headless=False`).
2. Log in to your X account manually.
3. The script will save `session.json`.

---

## 🏃 Usage

The pipeline is split into four modular stages:

### Stage 1: Collect
Scrapes X for raw data and saves to `knowledge/raw/`.
```bash
python collector.py
```

### Stage 2: Evaluate
Scores utility using Gemini. High-signal tweets (Score 7+) move to `knowledge/evaluated/`.
```bash
python evaluator.py
```

### Stage 3: Classify
Categorizes insights (PRINCIPLE, SKILL, MCP, etc.) and saves to `knowledge/processed/`.
```bash
python classifier.py
```

### Stage 4: Route
Distributes insights to Obsidian, Telegram, and `.md` files.
```bash
python router.py
```

---

## 📂 Folder Structure
- `knowledge/raw/`: Scraped JSON files.
- `knowledge/evaluated/`: Filtered by utility score.
- `knowledge/processed/`: Categorized and summarized.
- `00_CORE/`: Location of `GEMINI.md` and `CLAUDE.md` for principle updates.

## ⚖️ License
MIT
