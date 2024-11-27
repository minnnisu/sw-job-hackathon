import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import folium_static
import json
import time 

st.set_page_config(
    page_title="국내 SW 기업정보 분석 대시보드", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")    

# 데이터 불러오기
df = pd.read_excel('data/cleaned_data.xlsx')
geo_str = json.load(open('data/korea.json', encoding='utf-8'))

st.title("국내 SW 기업정보 분석 대시보드")
st.write("다양한 국내 SW 기업정보에 대한 데이터 시각화와 분석 결과를 확인하세요.")

row0_col1 = st.container()
row1_col1, row1_col2 = st.columns(2)  
row2_col1, row2_col2 = st.columns(2)  


# 1. 업종별 평균 데이터 시각화
required_columns = ["업종명", "직원수", "신입수", "퇴사수", "평균인당고지금액"]
if all(col in df.columns for col in required_columns):
    with row1_col1: 
        st.subheader("📊 업종별 인력 및 고용 현황")
        option = st.selectbox(
            "업종별 데이터 표시 항목을 선택하세요",
            ["직원수", "신입수", "퇴사수", "평균인당고지금액"],
            key="업종별"
        )

        grouped_data = df.groupby("업종명").agg({
            "직원수": "sum",
            "신입수": "sum",
            "퇴사수": "sum",
            "평균인당고지금액": "mean" 
        }).reset_index()

        selected_data = grouped_data[["업종명", option]]

        chart = (
            alt.Chart(selected_data)
            .mark_bar(color="skyblue")
            .encode(
                x=alt.X(option, title=f"{option}"),
                y=alt.Y("업종명", sort="-x", title="업종명")
            )
            .properties(width=400, height=300)
        )
        st.altair_chart(chart, use_container_width=True)


# 2. 특정 업종의 시도별 개수
required_columns = ["시도", "업종명"]
if all(col in df.columns for col in required_columns):
    with row1_col2:  
        st.subheader("📊 업종별 지역 분포")
        selected_industry = st.selectbox(
            "확인할 업종을 선택하세요   ",
            df["업종명"].unique(),
            key="특정업종"
        )
        filtered_data = df[df["업종명"] == selected_industry]
        grouped_data = filtered_data["시도"].value_counts().reset_index()
        grouped_data.columns = ["시도", "개수"]
        chart = (
            alt.Chart(grouped_data)
            .mark_bar(color="skyblue")
            .encode(
                x=alt.X("개수", title="개수"),
                y=alt.Y("시도", sort="-x", title="시도"),
            )
            .properties(width=400, height=300)
        )
        st.altair_chart(chart, use_container_width=True)

# 3. 시도별 평균 데이터 시각화
required_columns = ["시도", "직원수", "신입수", "퇴사수"]
if all(col in df.columns for col in required_columns):
    with row2_col1:  
        st.subheader("📊 시도별 인력 및 고용 현황")
        option = st.selectbox(
            "시도별 데이터 표시 항목을 선택하세요",
            ["직원수", "신입수", "퇴사수"],
            key="시도별"
        )
        grouped_data = df.groupby("시도").sum(numeric_only=True).reset_index()
        selected_data = grouped_data[["시도", option]]

        chart = (
            alt.Chart(selected_data)
            .mark_bar(color="skyblue")
            .encode(
                x=alt.X(option, title=f"{option}"),
                y=alt.Y("시도", sort="-x", title="지역")
            )
            .properties(width=400, height=300)
        )
        st.altair_chart(chart, use_container_width=True)

# 4. Choropleth 지도 시각화 
with row2_col2:  
    st.subheader("🗺️ 시도별 기업 현황 및 업종 분포")
    map_option = st.selectbox(
        "지도에 표시할 데이터를 선택하세요:",
        ["시도별 기업 수", "업종별 기업 분포"],
        key="지도"
    )

    map_width = 500  
    map_height = 300  
    map_osm = folium.Map(location=[36.8, 127.5], zoom_start=6)

    if map_option == "시도별 기업 수":
        df_geo = df.groupby("시도").size().reset_index(name="사업장수")
        choropleth = folium.Choropleth(
            geo_data=geo_str,
            data=df_geo,
            columns=["시도", "사업장수"],
            key_on="feature.properties.CTP_KOR_NM",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="시도별 기업 수"
        )
        choropleth.add_to(map_osm)

    elif map_option == "업종별 기업 분포":
        selected_upjong = st.selectbox("업종을 선택하세요:", df["업종명"].unique(), key="업종_지도")
        filtered_data = df[df["업종명"] == selected_upjong]
        df_geo = filtered_data.groupby("시도").size().reset_index(name="사업장수")
        choropleth = folium.Choropleth(
            geo_data=geo_str,
            data=df_geo,
            columns=["시도", "사업장수"],
            key_on="feature.properties.CTP_KOR_NM",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f"{selected_upjong} 업종의 시도별 사업장 수"
        )
        choropleth.add_to(map_osm)

        st.markdown("""
                    <div>
                        <span style="padding-left: 5px; font-size: 15px; color: #666">
                            \t * 검은색 부분은 데이터가 없는 지역입니다.</span
                        >
                    </div>

                    """, unsafe_allow_html=True 
        )
        

    folium_static(map_osm, width=map_width, height=map_height)



# 평균인당고지금액이 높은 10개 사업장 배너
with row0_col1:
    st.markdown("""
                <div>
                    <span style="font-size: 25px">TOP 10 기업</span>
                    <span style="padding-left: 5px; font-size: 15px; color: #666">
                        \t (기준 : 평균인당고지금액)</span
                    >
                </div>

                """, unsafe_allow_html=True
                )

    banner_placeholder = st.empty() 

    # 평균인당고지금액이 높은 10개 데이터 추출
    if "평균인당고지금액" in df.columns and "사업장명" in df.columns:
        top_10_businesses = df.nlargest(10, "평균인당고지금액")[["사업장명", "평균인당고지금액"]]

        while True:
            for _, row in top_10_businesses.iterrows():
                with banner_placeholder:
                    st.markdown(
                        f"""
                        <div style="margin-bottom : 20px; padding: 10px; border: 2px solid rgb(53 56 67); border-radius: 5px; background-color: rgb(38 39 42); text-align: center;">
                            <h2 style="margin: 0;">{row['사업장명']}</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                time.sleep(2)  