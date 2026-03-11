# X-extractor Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated pipeline to collect, evaluate, and route high-signal tweets to Gemini CLI, Claude Code, Obsidian, and Telegram.

**Architecture:** Modular Event-Driven Python scripts communicating via a local `knowledge/` folder hierarchy.

**Tech Stack:** Python, Playwright, Google Generative AI SDK, `python-dotenv`.

---

## Chunk 1: Environment & Collector Setup

### Task 1: Project Structure & Dependencies

**Files:**
- Create: `04_ACTIVE/X-extractor/requirements.txt`
- Create: `04_ACTIVE/X-extractor/.env.example`
- Create: `04_ACTIVE/X-extractor/.gitignore`

- [ ] **Step 1: Create requirements.txt**
```text
playwright
google-generativeai
python-dotenv
requests
pytest
```

- [ ] **Step 2: Create .env.example**
```text
GEMINI_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
OBSIDIAN_VAULT_PATH=/path/to/your/vault
GEMINI_SKILLS_PATH=~/.gemini/skills
CLAUDE_SKILLS_PATH=~/.claude/skills
```

- [ ] **Step 3: Create .gitignore**
```text
__pycache__/
.env
session.json
knowledge/raw/*
knowledge/evaluated/*
knowledge/processed/*
!knowledge/raw/.gitkeep
!knowledge/evaluated/.gitkeep
!knowledge/processed/.gitkeep
```

- [ ] **Step 4: Initialize knowledge directories**
Run: `mkdir -p 04_ACTIVE/X-extractor/knowledge/{raw,evaluated,processed} && touch 04_ACTIVE/X-extractor/knowledge/{raw,evaluated,processed}/.gitkeep`

- [ ] **Step 5: Install dependencies**
Run: `pip install -r 04_ACTIVE/X-extractor/requirements.txt && playwright install chromium`

- [ ] **Step 6: Commit**
```bash
git add 04_ACTIVE/X-extractor/requirements.txt 04_ACTIVE/X-extractor/.env.example 04_ACTIVE/X-extractor/.gitignore
git commit -m "chore: setup project structure and dependencies"
```

### Task 2: Playwright Collector (Initial Scraper)

**Files:**
- Create: `04_ACTIVE/X-extractor/collector.py`
- Test: `04_ACTIVE/X-extractor/tests/test_collector.py`

- [ ] **Step 1: Write a failing test for tweet extraction**
```python
import pytest
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import extract_tweet_id

def test_extract_tweet_id():
    url = "https://twitter.com/user/status/123456789"
    assert extract_tweet_id(url) == "123456789"
```

- [ ] **Step 2: Implement minimal `extract_tweet_id` in `collector.py`**
```python
import os
import json
import time
from playwright.sync_api import sync_playwright

def extract_tweet_id(url: str) -> str:
    return url.split('/')[-1]

if __name__ == "__main__":
    # Scraper logic will go here
    pass
```

- [ ] **Step 3: Run test**
Run: `pytest 04_ACTIVE/X-extractor/tests/test_collector.py`

- [ ] **Step 4: Implement `collector.py` skeleton**
Include Playwright setup, session loading, and a basic search-and-scroll loop.

- [ ] **Step 5: Commit**
```bash
git add 04_ACTIVE/X-extractor/collector.py 04_ACTIVE/X-extractor/tests/test_collector.py
git commit -m "feat: add collector skeleton and basic extraction logic"
```

---

## Chunk 2: Intelligence (Gemini API)

### Task 3: Evaluator & Classifier

**Files:**
- Create: `04_ACTIVE/X-extractor/evaluator.py`
- Create: `04_ACTIVE/X-extractor/classifier.py`
- Test: `04_ACTIVE/X-extractor/tests/test_intelligence.py`

- [ ] **Step 1: Implement `evaluator.py`**
Use Gemini 1.5 Flash to score tweets. Save to `knowledge/evaluated/`.

- [ ] **Step 2: Implement `classifier.py`**
Use Gemini 1.5 Flash to categorize tweets. Save to `knowledge/processed/`.

- [ ] **Step 3: Commit**
```bash
git add 04_ACTIVE/X-extractor/evaluator.py 04_ACTIVE/X-extractor/classifier.py
git commit -m "feat: implement Gemini evaluator and classifier"
```

---

## Chunk 3: Routing & Integration

### Task 4: Router (Obsidian & Telegram)

**Files:**
- Create: `04_ACTIVE/X-extractor/router.py`

- [ ] **Step 1: Implement Obsidian and Telegram routing**
Handle `REFERENCE`, `MCP`, and `PROJECT` categories.

- [ ] **Step 2: Implement GEMINI.md and CLAUDE.md routing**
Handle `PRINCIPLE` and `SKILL` categories with 8-point validation.

- [ ] **Step 3: Commit**
```bash
git add 04_ACTIVE/X-extractor/router.py
git commit -m "feat: implement routing to Obsidian, Telegram, and Markdown files"
```
