import pandas as pd

# 데이터 로드
df = pd.read_excel('data/data.xlsx')

# '주소' 열에 결측치(null)가 있는 행 필터링
null_address_rows = df[df['주소'].isnull()]

# '주소' 열에 결측치(null)가 있는 행 삭제
df_cleaned = df.dropna(subset=['주소'])

# 결과 확인
print("결측치(null)인 '주소' 행:")
print(null_address_rows)

print("\n'주소' 열에서 결측치(null)를 삭제한 데이터프레임:")
print(df_cleaned)

# 결측치(null)가 제거된 데이터 저장
df_cleaned.to_excel('data/cleaned_data.xlsx', index=False)