import schedule
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from crawler.news_crawler import fetch_all_news, extract_keyword_counts
from db.database import init_db, save_news, save_keyword_trend

def run_all():
    print(f"\n[{date.today()}] 자동 수집 시작...")

    try:
        print("  뉴스 수집 중...")
        df = fetch_all_news()

        print("  DB 저장 중...")
        save_news(df)

        print("  키워드 트렌드 분석 중...")
        keyword_counts = extract_keyword_counts(df.to_dict("records"))
        save_keyword_trend(keyword_counts, str(date.today()))

        print(f"  완료! 상위 키워드: {sorted(keyword_counts.items(), key=lambda x: -x[1])[:3]}")

    except Exception as e:
        print(f"  오류 발생: {e}")

# 매일 09:00 실행
schedule.every().day.at("09:00").do(run_all)

# 테스트용 - 1시간마다 실행하고 싶으면 아래 주석 해제
# schedule.every(1).hours.do(run_all)

print("스케줄러 시작! 매일 09:00에 자동 수집합니다.")
print("종료하려면 Ctrl+C\n")

# 시작하자마자 한 번 즉시 실행
run_all()

while True:
    schedule.run_pending()
    time.sleep(60)