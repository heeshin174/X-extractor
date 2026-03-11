import os
import json
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv

# Explicitly load .env from the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def classify_tweet(tweet_text):
    prompt = f"""
    다음 트윗의 내용을 분석하여 아래 유형 중 하나를 골라주세요.
    - PRINCIPLE: 개발/업무 원칙, 철학, 습관에 관한 내용
    - SKILL: 구체적인 기술, 명령어, 코드 스니펫, 워크플로우 절차
    - MCP: 새로운 MCP 서버, 도구, API 발견
    - PROJECT: 특정 프로젝트에만 적용 가능한 팁 (프레임워크/라이브러리 특화)
    - REFERENCE: 단순 참고용 정보, 뉴스, 일반 지식

    트윗: {tweet_text}
    
    유형만 출력하세요 (예: SKILL).
    """
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            return response.text.strip().upper()
        except errors.ClientError as e:
            if "429" in str(e):
                print("Quota exceeded, waiting 30s...")
                time.sleep(30)
                continue
            raise e
    return "UNKNOWN"

def process_evaluated_tweets():
    base_dir = os.path.dirname(__file__)
    eval_dir = os.path.join(base_dir, "knowledge/evaluated")
    proc_dir = os.path.join(base_dir, "knowledge/processed")
    
    if not os.path.exists(eval_dir):
        print(f"Evaluated directory not found: {eval_dir}")
        return

    for filename in os.listdir(eval_dir):
        if filename.endswith(".json"):
            with open(os.path.join(eval_dir, filename), 'r') as f:
                tweet = json.load(f)
            
            print(f"Classifying {filename}...")
            category = classify_tweet(tweet['text'])
            tweet['category'] = category
            
            if not os.path.exists(proc_dir):
                os.makedirs(proc_dir)
            with open(os.path.join(proc_dir, filename), 'w') as f:
                json.dump(tweet, f, indent=4)
            print(f"Classified: {filename} as {category}")

if __name__ == "__main__":
    process_evaluated_tweets()
