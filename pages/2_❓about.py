import streamlit as st


st.set_page_config(page_title="서비스 정보", layout="wide")

# ------

st.markdown("### 📊 국내 SW 기업정보 분석")
st.write("교내 학생들이 국내 SW 기업정보를 쉽고 빠르게 확인하고자 제작된 서비스입니다.")
st.markdown("""<a href="https://github.com/minnnisu/sw-job-hackathon">깃허브</a>""", unsafe_allow_html=True)
st.markdown("---")

# ------

st.markdown("### 💻 서비스 정보")
st.write("프로그래밍 언어: Python")
st.write("서비스 형태: Web")
st.write("사용한 라이브러리: streamlit, pandas, altair, folium, streamlit-folium, openpyxl")
st.markdown("---")

# ------

st.markdown("### 📋 서비스 기능")
st.markdown("#### 1. 대시보드 기능")
st.write("교내 학생들이 국내 SW 기업정보를 쉽고 빠르게 파악할 수 있도록 대시보드를 제작하였습니다. 상단에는 평균인당고지금액을 기준으로 상위 10개에 해당하는 기업들이 노출됩니다.")
st.write("그 아래로는 업종별 인력 및 고용 현황, 업종별 지역 분포, 시도별 인력 및 고용 현황, 시도별 사업장 현황 및 업종 분포를 확인할 수 있습니다.")
st.markdown("#### 2. 기업 검색 기능")
st.write("원하는 지역 또는 업종을 선택하여 해당 조건에 맞는 기업들을 볼 수 있도록 제작하였습니다.")
st.write("유저가 확인하고 싶은 기업이 있을 경우 검색창을 활용할 수 있습니다. 또한 검색된 결과들은 상단의 컬럼명을 클릭하여 정렬을 할 수 있습니다.")
st.markdown("---")

# ------

st.markdown("### 🧑🏻‍💻 200_OK 팀원 소개")
team_members = [
    {"name": "정성훈", "role": "팀장", "bio": "대시보드 제작"},
    {"name": "윤용현", "role": "팀원", "bio": "데이터 전처리, 검색페이지 제작"},
    {"name": "최민수", "role": "팀원", "bio": "배포, about 페이지 제작"},
]

for member in team_members:
    st.write(f"**{member['name']}**")
    st.write(f"역할: {member['role']}")
    st.write(f"담당: {member['bio']}")
st.markdown("---")

