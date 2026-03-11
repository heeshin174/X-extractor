# X-extractor Design Specification (2026-03-11)

## 1. Project Overview
X-extractor is an automated pipeline designed to collect high-signal tweets (AI, development tips, etc.) from X (Twitter) using scraping (Playwright), evaluate their utility using the Gemini API, and route them to appropriate knowledge bases (Gemini CLI, Claude Code, Obsidian, Telegram).

## 2. Goals & Success Criteria (MVP)
- **Automation-first**: End-to-end pipeline from collection to routing.
- **Cost-efficiency**: Use Playwright scraping to avoid X API v2 costs.
- **Multi-agent Support**: Update both `GEMINI.md` and `CLAUDE.md` with relevant principles/skills.
- **Knowledge Integration**: Seamlessly sync extracted insights into Obsidian and Telegram.

## 3. Architecture: Modular Event-Driven
The system is composed of independent Python scripts communicating via a structured directory hierarchy.

### 3.1 Data Flow
1. **Collector (`collector.py`)**: Uses Playwright to scrape X. Stores results in `knowledge/raw/`.
2. **Evaluator (`evaluator.py`)**: Uses Gemini 1.5 Flash to score utility (1-10). Stores 7+ scores in `knowledge/evaluated/`.
3. **Classifier (`classifier.py`)**: Uses Gemini 1.5 Flash to categorize into `PRINCIPLE`, `SKILL`, `MCP`, `PROJECT`, `REFERENCE`. Stores in `knowledge/processed/`.
4. **Router (`router.py`)**: Distributes processed insights to destinations based on classification.

## 4. Component Details

### 4.1 Collector (Scraping)
- **Tech**: Python, Playwright.
- **Strategy**: Search-and-scroll based on configurable queries.
- **Login**: Manual one-time login to save `session.json` cookies.
- **Throttling**: Random delays and human-like interactions to minimize detection.

### 4.2 Intelligence (Gemini API)
- **Evaluator**: "Is this tweet useful for a developer/AI enthusiast?"
- **Classifier**: Categorize into 5 types.
- **Summarizer**: Generate a concise, actionable summary of the core insight.

### 4.3 Router (Destinations)
- **GEMINI.md / CLAUDE.md**: Append principles after 8-point validation (uniqueness, relevance, etc.).
- **Skills**: Create `.sh`, `.py`, or `.md` files in `~/.gemini/skills/` and `~/.claude/skills/`.
- **Obsidian**: Create markdown notes with metadata in the specified vault.
- **Telegram**: Send rich notifications for `MCP` (new tools) or `PROJECT` specific findings.

## 5. Directory Structure
```
X-extractor/
├── collector.py
├── evaluator.py
├── classifier.py
├── router.py
├── .env (API Keys, Paths)
├── session.json (Playwright cookies)
└── knowledge/
    ├── raw/
    ├── evaluated/
    └── processed/
```

## 6. Implementation Phases
1. **Phase 1**: Setup Playwright and `collector.py` with manual login.
2. **Phase 2**: Implement Gemini-based `evaluator.py` and `classifier.py`.
3. **Phase 3**: Implement `router.py` for Obsidian and Telegram.
4. **Phase 4**: Implement `router.py` for `GEMINI.md` and `CLAUDE.md` updates.
