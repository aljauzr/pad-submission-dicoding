# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/data/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/data/hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

st.title("Dashboard Proyek Analisis Data (Bike Sharing Dataset)")
st.text('Nama: Al Jauzi Abdurrohman')
st.text('Email: aljauzir@gmail.com')
st.text('Dicoding ID: aljauzr')
tab1, tab2, tab3 = st.tabs(["Home", "Pertanyaan 1", "Pertanyaan 2"])

with tab1:
    st.subheader("Pemahaman Data")
    st.text('Pada dataset ini terdapat dua file, yaitu hour.csv dan day.csv. Dataset ini berisi informasi tentang penyewaan sepeda di suatu kota.')
    st.text('Data hour.csv berisi informasi perentalan sepeda per jam, sedangkan day.csv berisi informasi per hari. Maka dari itu, hanya data hour.csv yang memiliki informasi lebih lengkap yang akan digunakan dalam proses analisis data kali ini.')
    st.text('Tampilan data hour.csv:')
    st.dataframe(hour_df.head(10))
    st.text('Tampilan data day.csv:')
    st.dataframe(day_df.head(10))
    st.text('Perbedaan antara data hour.csv dan day.csv adalah pada data hour.csv terdapat kolom "hr" (0-23) yang menunjukkan jam perentalan sepeda, sedangkan pada data day.csv tidak ada kolom tersebut.')
    st.text('Penjelasan kolom:')
    st.text('- instant: ID dari setiap jam')
    st.text('- dteday: Tanggal perentalan sepeda')
    st.text('- season: Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)')
    st.text('- yr: Tahun (0: 2011, 1: 2012)')
    st.text('- mnth: Bulan (1-12)')
    st.text('- hr: Jam (0-23)')
    st.text('- holiday: Apakah hari libur (0: tidak, 1: ya)')
    st.text('- weekday: Hari dalam seminggu (0: Minggu, 1: Senin, 2: Selasa, 3: Rabu, 4: Kamis, 5: Jumat, 6: Sabtu)')
    st.text('- workingday: Apakah hari kerja (0: tidak, 1: ya)')
    st.text('- weathersit: Kondisi cuaca (1: Cerah, 2: Berawan, 3: Hujan, 4: Salju)')
    st.text('- temp: Suhu dalam derajat Celcius')
    st.text('- atemp: Suhu yang dirasakan dalam derajat Celcius')
    st.text('- hum: Kelembapan')
    st.text('- windspeed: Kecepatan angin')
    st.text('- casual: Jumlah penyewa sepeda kasual')
    st.text('- registered: Jumlah penyewa sepeda terdaftar')
    st.text('- cnt: Jumlah total penyewa sepeda (casual + registered)')
    st.text('Data hour.csv memiliki 17379 baris dan 17 kolom. Data ini juga memiliki beberapa kolom yang tidak relevan untuk analisis, seperti "instant" dan "holiday" (sudah diwakilkan oleh kolom workingday)')

    st.subheader("Pertanyaan Analisis")
    st.text('Pertanyaan 1: Kapan waktu paling optimal untuk menyediakan lebih banyak sepeda untuk direntalkan?')
    st.text('Pertanyaan 2: Bagaimana pengaruh cuaca terhadap jumlah pengguna sepeda (baik kasual maupun terdaftar)?')

with tab2:
    st.subheader("Pertanyaan 1: Kapan waktu paling optimal untuk menyediakan lebih banyak sepeda untuk direntalkan?")
    st.text('Untuk menjawab pertanyaan ini, kita akan membuat visualisasi jumlah penyewa sepeda berdasarkan musim, bulan, jam, hari, dan kondisi hari.')
    st.text('Visualisasi ini akan membantu kita memahami kapan waktu paling ramai penyewaan sepeda.')
    st.image("img1.png", caption="Visualisasi: Tren Penyewaan Sepeda Berdasarkan Waktu Terbaik", use_container_width=True)
    st.text('Berdasarkan visualisasi data tersebut, waktu paling optimal untuk menyediakan lebih banyak sepeda untuk direntalkan adalah pada musim gugur (fall), pada bulan Juni atau September, jam 5 sore, hari Kamis atau Jumat, dan pada saat hari kerja (tidak libur).')

with tab3:
    st.subheader("Pertanyaan 2: Bagaimana pengaruh cuaca terhadap jumlah pengguna sepeda (baik kasual maupun terdaftar)?")
    st.text('Untuk menjawab pertanyaan ini, kita akan membuat visualisasi jumlah penyewa sepeda berdasarkan kondisi cuaca, suhu sebenarnya, suhu yang dirasakan, kelembapan, dan kecepatan angin.')
    st.text('Visualisasi ini akan membantu kita memahami bagaimana pengaruh cuaca terhadap jumlah perentalan sepeda.')
    st.image("img2.png", caption="Visualisasi: Tren Penyewaan Sepeda Berdasarkan Pengaruh Cuaca", use_container_width=True)
    st.text('Berdasarkan visualisasi data tersebut, pengaruh cuaca terhadap jumlah penyewa sepeda adalah sebagai berikut:')
    st.text('1. Kondisi cuaca yang cerah membuat orang-orang lebih ingin merental sepeda, sedangkan jika turun hujan hingga badai, jumlah perentalan sepeda semakin sedikit.') 
    st.text('2. Untuk kondisi suhu, suhu normal (yaitu pada rentang 24-30°C) adalah suhu terbaik untuk merental sepeda. Suhu yang lebih dingin (berkisar antara 18-24°C) juga lebih menarik minat orang untuk merental sepeda dibanding suhu yang lebih panas (berkisar antara 30-36°C)')
    st.text('3. Kelembapan yang paling menarik minat orang-orang untuk merental sepeda ada pada angka 40-50.')
    st.text('4. Kecepatan angin yang paling menarik minat orang-orang untuk meerntal sepeda ada pada angka 7-14. Hal ini agak kontra pada proses EDA yang menyatakan maksimal jumlah perentalan sepeda terbanyak ada pada kecepatan angin 0, kemungkinan penyebabnya adalah kesalahan input data.')