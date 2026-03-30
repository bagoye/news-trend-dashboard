# 📈 IT 뉴스 키워드 트렌드 대시보드

> GeekNews · 요즘IT 기사를 자동 수집해 기술 키워드 트렌드를 분석하는 대시보드

**기간:** 2026.03 (1주)
**GitHub:** https://github.com/bagoye/news-trend-dashboard

---

## 📸 미리보기

<!-- 스크린샷 추가 예정 -->

---

## 📌 프로젝트 개요

매일 쏟아지는 IT 뉴스에서 어떤 기술이 주목받고 있는지 한눈에 파악하기 어렵다는 문제에서 시작했다.
GeekNews와 요즘IT의 기사를 자동 수집하고, 기술 키워드 빈도를 날짜별로 누적해 트렌드를 시각화했다.
첫 번째 프로젝트(IT 채용 대시보드)와 연계해 뉴스 트렌드와 채용 키워드를 비교할 수 있도록 설계했다.

---

## 🛠️ 사용 기술

| 분류         | 기술                               |
| ------------ | ---------------------------------- |
| 언어         | Python                             |
| 크롤링       | requests, BeautifulSoup4, XML 파싱 |
| 데이터 처리  | pandas                             |
| 데이터베이스 | SQLite                             |
| 시각화       | Streamlit, Plotly, WordCloud       |
| 자동화       | schedule                           |
| 버전 관리    | Git, GitHub                        |

---

## 📁 프로젝트 구조

```
news-trend-dashboard/
├── crawler/
│   └── news_crawler.py    # GeekNews · 요즘IT 크롤러
├── db/
│   └── database.py        # SQLite 연결 및 CRUD
├── app.py                 # Streamlit 대시보드
├── scheduler.py           # 자동 수집 스케줄러
└── requirements.txt
```

---

## ⚙️ 설치 및 실행

### 1. 가상환경 설정

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 2. 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터 수집

```bash
python crawler/news_crawler.py
```

### 4. 대시보드 실행

```bash
streamlit run app.py
```

### 5. 자동 수집 스케줄러 실행 (선택)

```bash
python scheduler.py
```

---

## 📊 주요 기능

**1. 멀티 소스 뉴스 수집**
GeekNews RSS와 요즘IT RSS를 파싱해 최신 IT 기사를 자동 수집. 중복 기사는 링크 기준으로 자동 제거.

**2. 키워드 트렌드 분석**
Python, AI, Docker 등 40개 기술 키워드 빈도를 날짜별로 누적 저장. 시계열 차트로 트렌드 변화를 확인할 수 있다.

**3. 워드 클라우드 시각화**
누적 키워드 빈도를 워드 클라우드로 시각화해 주목받는 기술을 직관적으로 파악할 수 있다.

**4. 자동 수집 스케줄러**
매일 오전 9시에 자동으로 데이터를 수집·저장하는 배치 스크립트를 구현했다.

---

## 💡 문제 해결 경험

**GeekNews RSS Atom 형식 파싱**
GeekNews RSS가 일반 RSS가 아닌 Atom 형식(RFC5023)으로 제공되어 파싱 오류 발생.
네임스페이스를 명시해서 해결했다.

```python
ns = {"atom": "http://www.w3.org/2005/Atom"}
entry.findtext("atom:title", namespaces=ns)
```

**SQLite 중복 저장 방지**
같은 기사가 반복 수집되는 문제를 `INSERT OR IGNORE` + `UNIQUE` 제약조건으로 해결했다.
