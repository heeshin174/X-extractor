import os
import json
import requests
from dotenv import load_dotenv

# Explicitly load .env from the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def save_to_obsidian(tweet):
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        return
    
    filename = f"X-Insight-{tweet['id']}.md"
    file_path = os.path.join(vault_path, filename)
    
    content = f"""---
id: {tweet['id']}
url: https://twitter.com/i/web/status/{tweet['id']}
category: {tweet['category']}
score: {tweet['utility_score']}
---

# X Insight: {tweet['id']}

{tweet['text']}

---
*Extracted via X-extractor*
"""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Saved to Obsidian: {filename}")
    except Exception as e:
        print(f"Obsidian error: {e}")

def update_markdown_principles(tweet, target_file):
    # Adjust target_file relative to repo root (assuming router.py is in 04_ACTIVE/X-extractor/)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    abs_target = os.path.join(repo_root, target_file)
    
    if not os.path.exists(abs_target):
        print(f"Target file not found: {abs_target}")
        return
    
    try:
        with open(abs_target, 'a') as f:
            f.write(f"\n- {tweet['text']} (Source: X)\n")
        print(f"Updated {target_file}")
    except Exception as e:
        print(f"Markdown update error: {e}")

def route_processed_tweets():
    base_dir = os.path.dirname(__file__)
    proc_dir = os.path.join(base_dir, "knowledge/processed")
    gemini_md = "00_CORE/GEMINI.md"
    claude_md = "00_CORE/CLAUDE.md"
    
    if not os.path.exists(proc_dir):
        print(f"Processed directory not found: {proc_dir}")
        return

    for filename in os.listdir(proc_dir):
        if filename.endswith(".json"):
            with open(os.path.join(proc_dir, filename), 'r') as f:
                tweet = json.load(f)
            
            category = tweet['category']
            
            # Universal Routing
            save_to_obsidian(tweet)
            
            # Specific Routing
            if category == "PRINCIPLE":
                update_markdown_principles(tweet, gemini_md)
                update_markdown_principles(tweet, claude_md)
            elif category in ["MCP", "PROJECT"]:
                send_telegram_message(f"New {category} Discovery!\n\n{tweet['text']}\n\nhttps://twitter.com/i/web/status/{tweet['id']}")
            
            print(f"Routed: {filename}")

if __name__ == "__main__":
    route_processed_tweets()
