import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from db.database import init_db, load_news, load_keyword_trend

st.set_page_config(page_title="뉴스 키워드 트렌드", layout="wide")

init_db()

@st.cache_data(ttl=300)
def get_data():
    news = load_news()
    trend = load_keyword_trend()
    return news, trend

news_df, trend_df = get_data()

st.title("📈 IT 뉴스 키워드 트렌드")
st.caption("GeekNews · 요즘IT 기사를 기반으로 기술 키워드 트렌드를 분석합니다")

tab1, tab2 = st.tabs(["📊 트렌드 분석", "📰 뉴스 목록"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("수집 기사 수", len(news_df))
    col2.metric("분석 키워드 수", len(trend_df["keyword"].unique()) if not trend_df.empty else 0)
    col3.metric("수집 기간", f"{trend_df['date'].nunique()}일" if not trend_df.empty else "0일")

    st.divider()

    if not trend_df.empty:
        total_kw = trend_df.groupby("keyword")["count"].sum().reset_index()
        total_kw = total_kw.sort_values("count", ascending=False)

        # 워드 클라우드 + 키워드 순위 나란히
        col_wc, col_bar = st.columns(2)

        with col_wc:
            st.subheader("☁️ 워드 클라우드")
            kw_dict = total_kw.set_index("keyword")["count"].to_dict()
            wc = WordCloud(
                font_path="C:/Windows/Fonts/malgun.ttf",
                width=400,
                height=250,
                background_color="black",
                colormap="Blues",
                max_words=20,
                max_font_size=60,
                min_font_size=12,
                prefer_horizontal=0.9,
                margin=8
            ).generate_from_frequencies(kw_dict)

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            fig.patch.set_facecolor("black")
            plt.tight_layout(pad=0)
            st.pyplot(fig)

        with col_bar:
            st.subheader("🏆 키워드 순위 Top 15")
            fig_bar = px.bar(
                total_kw.head(15),
                x="keyword", y="count",
                color="count",
                color_continuous_scale="Blues",
                labels={"keyword": "키워드", "count": "빈도"}
            )
            fig_bar.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                margin=dict(t=10, b=10)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # 시계열 트렌드
        st.subheader("📈 키워드 시계열 트렌드")
        top_keywords = total_kw["keyword"].head(8).tolist()
        selected = st.multiselect(
            "키워드 선택",
            options=trend_df["keyword"].unique().tolist(),
            default=top_keywords[:5]
        )

        if selected:
            filtered_trend = trend_df[trend_df["keyword"].isin(selected)].copy()
            filtered_trend["date"] = pd.to_datetime(filtered_trend["date"]).dt.strftime("%Y-%m-%d")
            fig_line = px.line(
                filtered_trend,
                x="date", y="count",
                color="keyword",
                markers=True,
                labels={"date": "날짜", "count": "빈도", "keyword": "키워드"}
            )
            fig_line.update_xaxes(type="category")
            st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.info("아직 트렌드 데이터가 없어요. 며칠 수집하면 시계열 차트가 나타납니다!")

with tab2:
    st.subheader(f"📰 수집된 기사 ({len(news_df)}개)")

    search = st.text_input("🔍 기사 검색", placeholder="키워드 입력")

    if search:
        filtered_news = news_df[
            news_df["title"].str.contains(search, case=False, na=False)
        ]
    else:
        filtered_news = news_df

    st.caption(f"{len(filtered_news)}개 표시 중")
    st.divider()

    for _, row in filtered_news.head(50).iterrows():
        c1, c2, c3 = st.columns([5, 1, 1])
        c1.write(row["title"])
        c2.caption(row["collected_at"])
        c3.link_button("보기 →", row["link"])