import streamlit as st
import pandas as pd

# 예시 데이터프레임 (df) 로드
df = pd.DataFrame(pd.read_excel('data/data.xlsx'))

# Streamlit UI 구성
st.title('사업장 필터링')

# 검색창 추가 (사업장명 검색)
search_term = st.text_input('사업장명을 검색하세요', value='')

# 시도 선택 (디폴트 값: 아무것도 선택되지 않음)
selected_sido = st.multiselect('시도를 선택하세요', options=df['시도'].unique(), default=[])

# 시도를 선택했을 때 해당 시도에 포함된 시군구 목록을 필터링
available_sigungu = []
if selected_sido:
    for sido in selected_sido:
        # 해당 시도에 포함된 시군구 목록
        sigungu_for_sido = df[df['시도'] == sido]['시군구'].unique()
        available_sigungu.extend(sigungu_for_sido)

    # 중복된 시군구 제거
    available_sigungu = list(set(available_sigungu))

# 시군구 선택
selected_sigungu = st.multiselect('시군구를 선택하세요', options=available_sigungu, default=[])

# 다중 체크박스를 통한 업종 선택 (디폴트 값: 아무것도 선택되지 않음)
selected_upjong = st.multiselect('업종을 선택하세요', options=df['업종명'].unique(), default=[])

# 선택된 값에 따라 필터링
if selected_sido or selected_sigungu or selected_upjong or search_term:
    filtered_df = df[
        (df['시도'].isin(selected_sido) if selected_sido else True) &
        (df['시군구'].isin(selected_sigungu) if selected_sigungu else True) &
        (df['업종명'].isin(selected_upjong) if selected_upjong else True) &
        (df['사업장명'].str.contains(search_term, case=False, na=False) if search_term else True)
    ]
else:
    # 아무것도 선택되지 않았을 경우 모든 결과를 출력
    filtered_df = df

# 필요한 칼럼만 선택하여 출력
columns_to_display = ['사업장명', '주소', '업종명', '직원수', '신입수', '퇴사수', '평균인당고지금액']
filtered_df = filtered_df[columns_to_display]

# 인덱스를 제거하고 결과 출력
filtered_df.reset_index(drop=True, inplace=True)

# 필터링된 사업장 출력
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.write("선택한 조건에 맞는 사업장이 없습니다.")
