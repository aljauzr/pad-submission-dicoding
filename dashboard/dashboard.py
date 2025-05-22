# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.text('- instant: ID dari setiap data')
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
    st.image("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/dashboard/img1.png", caption="Visualisasi: Tren Penyewaan Sepeda Berdasarkan Waktu Terbaik", use_container_width=True)
    st.text('Berdasarkan hasil analisis data, waktu di mana jumlah perentalan sepeda tertinggi terjadi pada waktu berikut:')
    st.text('Musim: Fall (Musim Gugur)')
    st.text('Bulan: Juni dan September')
    st.text('Jam: 17:00 (5 sore)')
    st.text('Hari: Kamis dan Jumat')
    st.text('Kondisi Hari: Tidak Libur (Hari Kerja)')
    st.text('Sedangkan untuk waktu di mana jumlah perentalan sepeda terendah terjadi pada waktu berikut:')
    st.text('Musim: Spring (Musim Semi)')
    st.text('Bulan: Januari')
    st.text('Jam: 04:00 (4 pagi)')
    st.text('Hari: Minggu')
    st.text('Kondisi Hari: Libur')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')
    st.markdown("### Visualisasi Interaktif: Filter Jumlah Penyewaan Sepeda Berdasarkan Kondisi Waktu")

    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    # Multiselect: Pilih tahun (tidak sebagai filter induk)
    selected_year = st.multiselect(
        "Pilih Tahun",
        options=hour_df['yr'].unique(),
        default=[0],  # Tahun 2011
        format_func=lambda x: "2011" if x == 0 else "2012"
    )

    selected_season = st.multiselect(
        "Pilih Musim",
        options=sorted(hour_df['season'].unique()),
        format_func=lambda x: {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}[x]
    )

    selected_hour = st.multiselect(
        "Pilih Jam",
        options=sorted(hour_df['hr'].unique())
    )

    selected_month = st.multiselect(
        "Pilih Bulan",
        options=sorted(hour_df['mnth'].unique()),
        format_func=lambda x: pd.to_datetime(f'2022-{x}-01').strftime('%B')
    )

    selected_weekday = st.multiselect(
        "Pilih Hari",
        options=sorted(hour_df['weekday'].unique()),
        format_func=lambda x: ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu'][x]
    )

    selected_workingday = st.multiselect(
        "Pilih Tipe Hari",
        options=sorted(hour_df['workingday'].unique()),
        format_func=lambda x: "Hari Kerja" if x == 1 else "Hari Libur"
    )

    # Mulai dari data asli
    df_filtered = hour_df.copy()

    # Terapkan semua filter
    if selected_year:
        df_filtered = df_filtered[df_filtered['yr'].isin(selected_year)]
    if selected_season:
        df_filtered = df_filtered[df_filtered['season'].isin(selected_season)]
    if selected_hour:
        df_filtered = df_filtered[df_filtered['hr'].isin(selected_hour)]
    if selected_month:
        df_filtered = df_filtered[df_filtered['mnth'].isin(selected_month)]
    if selected_weekday:
        df_filtered = df_filtered[df_filtered['weekday'].isin(selected_weekday)]
    if selected_workingday:
        df_filtered = df_filtered[df_filtered['workingday'].isin(selected_workingday)]

    # Tampilkan hasil visualisasi
    if not df_filtered.empty:
        total_count = df_filtered['cnt'].count()
        fig = px.bar(
            x=["Kondisi Filter"],
            y=[total_count],
            labels={'x': 'Kondisi Filter', 'y': 'Jumlah'},
            title='Jumlah Penyewaan Sepeda Berdasarkan Filter Kondis Waktu'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

with tab3:
    st.subheader("Pertanyaan 2: Bagaimana pengaruh cuaca terhadap jumlah pengguna sepeda (baik kasual maupun terdaftar)?")
    st.text('Untuk menjawab pertanyaan ini, kita akan membuat visualisasi jumlah penyewa sepeda berdasarkan kondisi cuaca, suhu sebenarnya, suhu yang dirasakan, kelembapan, dan kecepatan angin.')
    st.text('Visualisasi ini akan membantu kita memahami bagaimana pengaruh cuaca terhadap jumlah perentalan sepeda.')
    st.image("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/dashboard/img2.png", caption="Visualisasi: Tren Penyewaan Sepeda Berdasarkan Pengaruh Cuaca", use_container_width=True)
    st.text('Berdasarkan hasil analisis data, kondisi cuaca di mana jumlah perentalan sepeda tertinggi terjadi pada kondisi cuaca berikut:')
    st.text('Kondisi: Cerah dan sedikit berawan')
    st.text('Suhu Sebenarnya: 24°C-30°C')
    st.text('Suhu yang Dirasakan: 30°C-35°C')
    st.text('Kelembapan: 40-50')
    st.text('Kecepatan Angin: 7-14')
    st.text('Sedangkan untuk kondisi cuaca di mana jumlah perentalan sepeda terendah terjadi pada kondisi cuaca berikut:')
    st.text('Kondisi: Hujan lebat, bersalju, badai, mendung, dan berkabut')
    st.text('Suhu Sebenarnya: 36°C-42°C')
    st.text('Suhu yang Dirasakan: 0°C-5°C')
    st.text('Kelembapan: 0-10')
    st.text('Kecepatan Angin: 56-63')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')
    st.text('1. Kondisi cuaca yang cerah membuat orang-orang lebih ingin merental sepeda, sedangkan jika turun hujan hingga badai, jumlah perentalan sepeda semakin sedikit.')
    st.text('2. Untuk kondisi suhu, suhu normal (yaitu pada rentang 24-30°C) adalah suhu terbaik untuk merental sepeda. Suhu yang lebih dingin (berkisar antara 18-24°C) juga lebih menarik minat orang untuk merental sepeda dibanding suhu yang lebih panas (berkisar antara 30-36°C)')
    st.text('3. Kelembapan yang paling menarik minat orang-orang untuk merental sepeda ada pada angka 40-50.')
    st.text('4. Kecepatan angin yang paling menarik minat orang-orang untuk meerntal sepeda ada pada angka 7-14. Hal ini agak kontra pada proses EDA yang menyatakan maksimal jumlah perentalan sepeda terbanyak ada pada kecepatan angin 0, kemungkinan penyebabnya adalah kesalahan input data.')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')
    st.markdown("### Visualisasi Interaktif: Filter Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

    # Mengubah nilai kondisi cuaca yang telah dinormalisasi ke nilai sebenarnya
    hour_df['temp_actual'] = hour_df['temp'] * 41
    hour_df['atemp_actual'] = hour_df['atemp'] * 50
    hour_df['hum_actual'] = hour_df['hum'] * 100
    hour_df['windspeed_actual'] = hour_df['windspeed'] * 67

    # Multiselect: Pilih tahun (tidak sebagai filter induk)
    selected_weathersit = st.multiselect(
        "Kondisi Cuaca",
        options=hour_df['weathersit'].unique(),
        default=[1],
        format_func=lambda x: {1: 'Cerah dan sedikit berawan', 2: 'Mendung dan berawan', 3: 'Sedikit turun salju dan hujan', 4: 'Hujan lebat, salju, badai'}[x]
    )

    selected_temp = st.multiselect(
        "Suhu Sebenarnya",
        options=sorted(hour_df['temp_actual'].unique())
    )

    selected_atemp = st.multiselect(
        "Suhu yang Dirasakan",
        options=sorted(hour_df['atemp_actual'].unique())
    )

    selected_hum = st.multiselect(
        "Kelembapan",
        options=sorted(hour_df['hum_actual'].unique())
    )

    selected_windspeed = st.multiselect(
        "Kecepatan Angin",
        options=sorted(hour_df['windspeed_actual'].unique())
    )

    # Mulai dari data asli
    df_filtered = hour_df.copy()

    # Terapkan semua filter
    if selected_weathersit:
        df_filtered = df_filtered[df_filtered['weathersit'].isin(selected_weathersit)]
    if selected_temp:
        df_filtered = df_filtered[df_filtered['temp_actual'].isin(selected_temp)]
    if selected_atemp:
        df_filtered = df_filtered[df_filtered['atemp_actual'].isin(selected_atemp)]
    if selected_hum:
        df_filtered = df_filtered[df_filtered['hum_actual'].isin(selected_hum)]
    if selected_windspeed:
        df_filtered = df_filtered[df_filtered['windspeed_actual'].isin(selected_windspeed)]

    # Tampilkan hasil visualisasi
    if not df_filtered.empty:
        total_count = df_filtered['cnt'].count()
        fig = px.bar(
            x=["Kondisi Filter"],
            y=[total_count],
            labels={'x': 'Kondisi Filter', 'y': 'Jumlah'},
            title='Jumlah Penyewaan Sepeda Berdasarkan Filter Kondisi Cuaca'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")