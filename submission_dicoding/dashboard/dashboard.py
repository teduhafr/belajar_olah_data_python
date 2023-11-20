import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
## from babel.numbers import format_currency kelihatannya ini tidak akan dipakai
sns.set(style='dark')

all_df = pd.read_csv("data.csv")

#untuk dashboard

tahun=list(all_df['year'].unique())
tahun_awal = min(tahun)
tahun_option_akhir = filter(lambda num: num >= tahun_awal, tahun)
tahun_akhir = max(tahun)

data_awal = 'PM2.5'



##untuk fungsi-fungsi
def filter_tahun(df, awal, akhir):
    df_tahun = df.drop(df[(df.year < awal) | (df.year > akhir)].index)
    return df_tahun


def data_station_pertahun(df, awal, akhir):
    df_data = filter_tahun(df, awal, akhir)
    if(data_awal =='PM2.5'):
        data_df = df_data.pivot_table('PM2.5', 'year', 'station', aggfunc='mean').reset_index()
        return data_df
    elif (data_awal =='PM10'):
        data_df = df_data.pivot_table('PM10', 'year', 'station', aggfunc='mean').reset_index()
        return data_df

def data_station_pertahun_perbulan(df, awal, akhir):
    df_data = filter_tahun(df, awal, akhir)
    if(data_awal =='PM2.5'):
        data_df = df_data.pivot_table('PM2.5', ['year', 'month', 'yearmonth'], 'station', aggfunc='mean').reset_index()
        return data_df
    elif (data_awal =='PM10'):
        data_df = df_data.pivot_table('PM10', ['year', 'month', 'yearmonth'], 'station', aggfunc='mean').reset_index()
        return data_df
def data_perjam(df, awal, akhir):
    df_data1 = filter_tahun(df, awal, akhir)
    data_pivot_perjam = df_data1.pivot_table(['PM2.5', 'PM10'], 'hour', aggfunc='mean').reset_index()
    return data_pivot_perjam

with st.sidebar:
    #judul
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.subheader("Air Quality")
    # Menambahkan logo perusahaan
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("./asset/gambar_depan.png", width=150)
    
    # Mengambil start_date & end_date dari date_input
    option = st.selectbox(
    'Data yang ditampilkan',
    ('PM2.5', 'PM10'))
    data_awal = option

    st.divider()
    st.subheader("Tahun")
    col1, col2 = st.columns(2)
    
    with col1:
        option_awal = st.selectbox(
        'Awal',
        (tahun))
        tahun_awal = option_awal
    with col2:
        option_akhir = st.selectbox(
        'Akhir',
        (tahun_option_akhir))
        tahun_akhir = option_akhir
    st.text("Data Terakhir 2017 Februari")
#buat judul
st.title('Data PM2.5 dan PM 10' 
          + '\n untuk Station Aotizhongxin, Changping, Dingling, Dongsi dan Guanyuan')

##
st.subheader('Pemamantauan Kualitas PM2.5 dan PM 10 di Tiap Station', divider='rainbow')
st.subheader('Kualitas Udara '+ str(data_awal)+ ' Tahun ' + str(tahun_awal) + ' - ' + str(tahun_akhir))
df = data_station_pertahun(all_df, tahun_awal, tahun_akhir)
plt.figure(figsize=(13, 5))
plt.plot(df['year'], df['Aotizhongxin'], label = 'Aotizhongxin', color='red')
plt.plot(df['year'], df['Changping'], label = 'Changping', color='blue')
plt.plot(df['year'], df['Dingling'], label = 'Dingling', color='yellow')
plt.plot(df['year'], df['Dongsi'], label = 'Dongsi', color='black')
plt.plot(df['year'], df['Guanyuan'], label = 'Guanyuan', color='pink')
plt.xlabel('tahun',size= 20)
plt.ylabel('Kadar ' + str(data_awal), size = 20)
plt.legend()
st.pyplot(plt)
with st.expander("Detail Per Tahun"):


    st.subheader('Kualitas Udara detail per tahun untuk '+ str(data_awal))
    tahun_digunakan = 2013
    option_tahun = st.selectbox(
        'Tahun data',
        (tahun))
    tahun_digunakan = option_tahun

    df_peryear = data_station_pertahun_perbulan(all_df, tahun_digunakan, tahun_digunakan)
    plt.figure(figsize=(12, 5))
    plt.plot(df_peryear['month'], df_peryear['Aotizhongxin'], label = 'Aotizhongxin', color='red')
    plt.plot(df_peryear['month'], df_peryear['Changping'], label = 'Changping', color='blue')
    plt.plot(df_peryear['month'], df_peryear['Dingling'], label = 'Dingling', color='yellow')
    plt.plot(df_peryear['month'], df_peryear['Dongsi'], label = 'Dongsi', color='black')
    plt.plot(df_peryear['month'], df_peryear['Guanyuan'], label = 'Guanyuan', color='pink')
    plt.xlabel('Bulan',size= 20)
    plt.ylabel('Kadar ' +str(data_awal), size = 20)
    judul  = 'Data Kulatias' +str(data_awal) + 'per Station Tahun ' + str(tahun_digunakan) +  '\n makin kecil makin bagus'
    plt.title(judul , fontsize=15)
    plt.legend()

    st.pyplot(plt)


st.divider()
st.subheader('Pemantauan Kualitas ' + str(data_awal)+' tiap jam', divider='rainbow')
df_perjam = data_perjam(all_df, tahun_awal, tahun_akhir)
plt.figure(figsize=(8, 3))
sns.barplot(y=df_perjam["PM2.5"], x=df_perjam["hour"])
plt.xlabel('Jam',size= 15)
plt.ylabel('Kadar ' +str(data_awal), size = 15)
plt.xticks(rotation='vertical')
st.pyplot(plt)
