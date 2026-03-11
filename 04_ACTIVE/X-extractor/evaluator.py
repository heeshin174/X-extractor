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

def evaluate_tweet(tweet_text):
    prompt = f"""
    당신은 개발 및 AI 관련 콘텐츠의 유용성을 평가하는 전문가입니다.
    아래 트윗을 읽고 다음 기준에 따라 1~10점 사이의 점수를 매겨주세요.
    
    10점: 즉시 적용 가능한 구체적 팁, 도구, 코드 스니펫
    8–9점: 매우 유용한 인사이트, 워크플로우 개선안
    6–7점: 관련은 있지만 일반적인 수준
    4–5점: 간접적, 뉴스/발표 수준
    1–3점: 무관, 밈, 감상

    트윗: {tweet_text}
    
    점수만 숫자로 출력하세요.
    """
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            score = int(response.text.strip())
            return score
        except errors.ClientError as e:
            if "429" in str(e):
                print("Quota exceeded, waiting 30s...")
                time.sleep(30)
                continue
            raise e
        except Exception:
            return 0
    return 0

def process_raw_tweets():
    base_dir = os.path.dirname(__file__)
    raw_dir = os.path.join(base_dir, "knowledge/raw")
    eval_dir = os.path.join(base_dir, "knowledge/evaluated")
    
    if not os.path.exists(raw_dir):
        print(f"Raw directory not found: {raw_dir}")
        return

    for filename in os.listdir(raw_dir):
        if filename.endswith(".json"):
            with open(os.path.join(raw_dir, filename), 'r') as f:
                tweet = json.load(f)
            
            print(f"Evaluating {filename}...")
            score = evaluate_tweet(tweet['text'])
            tweet['utility_score'] = score
            
            if score >= 7:
                if not os.path.exists(eval_dir):
                    os.makedirs(eval_dir)
                with open(os.path.join(eval_dir, filename), 'w') as f:
                    json.dump(tweet, f, indent=4)
                print(f"Passed: {filename} (Score: {score})")
            else:
                print(f"Rejected: {filename} (Score: {score})")

if __name__ == "__main__":
    process_raw_tweets()
