import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='미세플라스틱 흡수량 분석', layout='wide')

@st.cache_data
def load_data(path='섭취량 웹앱 데이터(업로드).csv'):
    return pd.read_csv(path)

df = load_data()
st.title('미세플라스틱 흡수량 분석 (Streamlit)')
st.write('원본 파일: 섭취량 웹앱 데이터(업로드).csv')

st.sidebar.header('필터')
start = st.sidebar.number_input('시작 행', min_value=0, max_value=len(df)-1, value=0, step=1)
end = st.sidebar.number_input('끝 행', min_value=1, max_value=len(df), value=min(100, len(df)), step=1)
df_view = df.iloc[int(start):int(end)]

st.header('데이터 미리보기')
st.dataframe(df_view)

st.header('기초 통계')
st.write(df_view.describe(include='all'))

num_cols = df_view.select_dtypes(include=['number']).columns.tolist()
if num_cols:
    sel = st.selectbox('시각화할 수치형 열 선택', num_cols)
    st.line_chart(df_view[sel])
    fig, ax = plt.subplots()
    ax.hist(df_view[sel].dropna(), bins=30)
    ax.set_xlabel(sel)
    ax.set_ylabel('빈도')
    st.pyplot(fig)

st.download_button('필터된 CSV 다운로드', df_view.to_csv(index=False).encode('utf-8-sig'), file_name='filtered_data.csv', mime='text/csv')
