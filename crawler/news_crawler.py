import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
from datetime import datetime
from collections import Counter

TECH_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js",
    "Spring", "FastAPI", "Django", "Kotlin", "Swift", "iOS", "Android",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "DevOps", "MLOps",
    "AI", "ML", "딥러닝", "머신러닝", "LLM", "GPT", "데이터", "SQL",
    "백엔드", "프론트엔드", "풀스택", "보안", "클라우드", "오픈소스",
    "ChatGPT", "RAG", "벡터DB", "파이프라인", "Airflow"
]

def fetch_geek_news():
    url = "https://news.hada.io/rss/news"
    response = requests.get(url)
    response.encoding = "utf-8"
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    articles = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        published = entry.findtext("atom:published", namespaces=ns)
        articles.append({
            "title": title,
            "link": link,
            "published_at": published[:10] if published else "",
            "source": "GeekNews"
        })

    print(f"  GeekNews: {len(articles)}개 수집")
    return articles

def fetch_naver_it_news():
    url = "https://rss.blog.naver.com/it"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        root = ET.fromstring(response.content)
        channel = root.find("channel")

        articles = []
        for item in channel.findall("item"):
            title = item.findtext("title")
            link = item.findtext("link")
            pub_date = item.findtext("pubDate", "")
            articles.append({
                "title": title,
                "link": link,
                "published_at": pub_date[:10] if pub_date else "",
                "source": "네이버IT"
            })

        print(f"  네이버IT: {len(articles)}개 수집")
        return articles

    except Exception as e:
        print(f"  네이버IT 수집 실패: {e}")
        return []

def extract_keyword_counts(articles):
    counter = Counter()
    for article in articles:
        title = article.get("title", "") or ""
        for kw in TECH_KEYWORDS:
            if kw.lower() in title.lower():
                counter[kw] += 1
    return dict(counter)

def fetch_all_news():
    print("뉴스 수집 시작...")
    articles = []
    articles.extend(fetch_geek_news())
    articles.extend(fetch_naver_it_news())
    articles.extend(fetch_yozm_it())

    df = pd.DataFrame(articles).drop_duplicates(subset=["link"])
    print(f"총 {len(df)}개 기사 수집 완료!")
    return df

def fetch_yozm_it():
    url = "https://yozm.wishket.com/magazine/feed/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        root = ET.fromstring(response.content)
        channel = root.find("channel")

        articles = []
        for item in channel.findall("item"):
            title = item.findtext("title")
            link = item.findtext("link")
            pub_date = item.findtext("pubDate", "")
            articles.append({
                "title": title,
                "link": link,
                "published_at": pub_date[:10] if pub_date else "",
                "source": "요즘IT"
            })

        print(f"  요즘IT: {len(articles)}개 수집")
        return articles

    except Exception as e:
        print(f"  요즘IT 수집 실패: {e}")
        return []

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from datetime import date
    from db.database import init_db, save_news, save_keyword_trend

    init_db()

    df = fetch_all_news()
    save_news(df)

    keyword_counts = extract_keyword_counts(df.to_dict("records"))
    today = str(date.today())
    save_keyword_trend(keyword_counts, today)

    print(f"\n키워드 트렌드 저장 완료! ({today})")
    print("상위 키워드:", sorted(keyword_counts.items(), key=lambda x: -x[1])[:5])