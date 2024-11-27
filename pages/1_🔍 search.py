import streamlit as st
import pandas as pd

df = pd.DataFrame(pd.read_excel('data/cleaned_data.xlsx'))

st.set_page_config(
    page_title="기업 검색",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('🔍 기업 검색')

search_term = st.text_input('기업명을 검색하세요', value='')

selected_sido = st.multiselect('시도를 선택하세요', options=df['시도'].unique(), default=[])

available_sigungu = []
if selected_sido:
    for sido in selected_sido:

        sigungu_for_sido = df[df['시도'] == sido]['시군구'].unique()
        available_sigungu.extend(sigungu_for_sido)

   
    available_sigungu = list(set(available_sigungu))

selected_sigungu = st.multiselect('시군구를 선택하세요', options=available_sigungu, default=[])

selected_upjong = st.multiselect('업종을 선택하세요', options=df['업종명'].unique(), default=[])

if selected_sido or selected_sigungu or selected_upjong or search_term:
    filtered_df = df[
        (df['시도'].isin(selected_sido) if selected_sido else True) &
        (df['시군구'].isin(selected_sigungu) if selected_sigungu else True) &
        (df['업종명'].isin(selected_upjong) if selected_upjong else True) &
        (df['사업장명'].str.contains(search_term, case=False, na=False) if search_term else True)
    ]
else:
    
    filtered_df = df


columns_to_display = ['사업장명', '주소', '업종명', '직원수', '신입수', '퇴사수', '평균인당고지금액']
filtered_df = filtered_df[columns_to_display]


filtered_df.reset_index(drop=True, inplace=True)

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.write("선택한 조건에 맞는 기업이 없습니다.")
