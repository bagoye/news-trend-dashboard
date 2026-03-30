import sqlite3
import pandas as pd
import os

DB_PATH = "db/news_trend.db"

def get_connection():
    os.makedirs("db", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE,
            published_at TEXT,
            source TEXT,
            collected_at TEXT DEFAULT (date('now'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keyword_trend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            count INTEGER NOT NULL,
            date TEXT NOT NULL,
            UNIQUE(keyword, date)
        )
    """)
    conn.commit()
    conn.close()
    print("DB 초기화 완료!")

def save_news(df):
    conn = get_connection()
    saved = 0
    for _, row in df.iterrows():
        try:
            conn.execute("""
                INSERT OR IGNORE INTO news (title, link, published_at, source)
                VALUES (?, ?, ?, ?)
            """, (row["title"], row["link"], row["published_at"], row["source"]))
            saved += 1
        except Exception as e:
            print(f"저장 오류: {e}")
    conn.commit()
    conn.close()
    print(f"{saved}개 기사 저장 완료!")

def save_keyword_trend(keyword_counts, date):
    conn = get_connection()
    for keyword, count in keyword_counts.items():
        try:
            conn.execute("""
                INSERT OR REPLACE INTO keyword_trend (keyword, count, date)
                VALUES (?, ?, ?)
            """, (keyword, count, date))
        except Exception as e:
            print(f"키워드 저장 오류: {e}")
    conn.commit()
    conn.close()

def load_news():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM news ORDER BY collected_at DESC", conn)
    conn.close()
    return df

def load_keyword_trend():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM keyword_trend ORDER BY date", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()