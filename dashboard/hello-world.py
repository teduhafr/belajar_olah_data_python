import streamlit as st 
import pandas as pd

st.title('Belajar Analisis Data')

st.header('Pengembangan Dashboard')

st.write(pd.DataFrame({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40],
}))

code = """def hello():
    print("Hello, Streamlit!")"""
st.code(code, language='python')