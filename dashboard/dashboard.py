# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Exploratory Data Analysis (EDA), Data Visualization, & Explanatory Analysis
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/data/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/aljauzr/pad-submission-dicoding/refs/heads/main/data/hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

# Data Cleaning (Hanya menggunakan hour_df)

# Menghapus kolom 'instant' dan 'holiday' lalu mengubah tipe data kolom 'dteday' dari object menjadi datetime pada data hour.csv
hour_df.drop(columns=['instant', 'holiday'], inplace=True)
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
# Penghapusan kolom instant dikarenakan kolom ini hanya mengandung nomor urut dari data yang ada pada dataset
# Sedangkan kolom holiday tidak diperlukan karena kita sudah memiliki kolom weekday yang menunjukkan hari apa data tersebut diambil
# Kolom dteday juga diubah menjadi tipe data datetime agar lebih mudah dalam melakukan analisis dan visualisasi data.
# Mengubah nilai kolom 'season', 'yr', 'mnth', 'weekday', dan 'workingday' sesuai nilai yang didefinisikan di file Readme.txt

# Mengubah nilai kolom 'season' menjadi nilai kategori
season_mapping = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
hour_df['season'] = hour_df['season'].map(season_mapping)
# Mengubah nilai kolom 'yr' menjadi nilai tahun aslinya
yr_mapping = {
    0: 2011,
    1: 2012
}
hour_df['yr'] = hour_df['yr'].map(yr_mapping)
# Mengubah nilai kolom 'mnth' menjadi nilai kategori
mnth_mapping = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}
hour_df['mnth'] = hour_df['mnth'].map(mnth_mapping)
# Mengubah nilai kolom 'weekday' menjadi nilai kategori
weekday_mapping = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}
hour_df['weekday'] = hour_df['weekday'].map(weekday_mapping)
# Mengubah nilai kolom 'workingday' menjadi nilai kategori
workingday_mapping = {
    0: 'Holiday',
    1: 'Not Holiday'
}
hour_df['workingday'] = hour_df['workingday'].map(workingday_mapping)
# Mengubah nilai kondisi cuaca yang telah dinormalisasi ke nilai sebenarnya
hour_df['temp_actual'] = hour_df['temp'] * 41
hour_df['atemp_actual'] = hour_df['atemp'] * 50
hour_df['hum_actual'] = hour_df['hum'] * 100
hour_df['windspeed_actual'] = hour_df['windspeed'] * 67

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
    # Pilihan tahun
    tahun_pilihan = st.selectbox(
        'Pilih Tahun Data yang Ditampilkan:',
        options=['Gabungan', 2011, 2012],
        index=0,  # default: Gabungan
        key='tahun_tab2'
    )

    # Filter dataframe berdasarkan pilihan
    if tahun_pilihan == 'Gabungan':
        hour_df_filtered = hour_df.copy()  # tidak difilter
    else:
        hour_df_filtered = hour_df[hour_df['yr'] == tahun_pilihan]
    
    # Buat kanvas visualisasi
    fig, axs = plt.subplots(3, 2, figsize=(16, 14))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Visualisasi 1
    mean_cnt_per_season = hour_df_filtered.groupby('season')['cnt'].mean().reset_index()
    max_value = mean_cnt_per_season['cnt'].max()
    colors = ['#72BCD4' if val == max_value else '#D3D3D3' for val in mean_cnt_per_season['cnt']]
    sns.barplot(data=mean_cnt_per_season, x='season', y='cnt', palette=colors, hue='season', legend=False, ax=axs[0, 0])
    for index, row in mean_cnt_per_season.iterrows():
        axs[0, 0].text(index, row['cnt'], round(row['cnt']), color='black', ha="center", va="bottom")
    axs[0, 0].set_title('Rata-Rata Jumlah Perentalan Sepeda Berdasarkan Musim')
    axs[0, 0].set_xlabel('Musim')
    axs[0, 0].set_ylabel('Rata-Rata Jumlah')

    # Visualisasi 2
    mean_cnt_per_month = hour_df_filtered.groupby('mnth', observed=True)['cnt'].mean().reset_index()
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    mean_cnt_per_month['mnth'] = pd.Categorical(mean_cnt_per_month['mnth'], categories=month_order, ordered=True)
    mean_cnt_per_month = mean_cnt_per_month.sort_values('mnth')
    # Tentukan warna berdasarkan tahun yang dipilih
    if tahun_pilihan == 'Gabungan':
        colors = ["#D3D3D3"]*5 + ["#72BCD4"] + ["#D3D3D3"]*2 + ["#72BCD4"] + ["#D3D3D3"]*3
    elif tahun_pilihan == 2011:
        colors = ["#D3D3D3"]*5 + ["#72BCD4"] + ["#D3D3D3"]*6
    elif tahun_pilihan == 2012:
        colors = ["#D3D3D3"]*8 + ["#72BCD4"] + ["#D3D3D3"]*2
    sns.barplot(data=mean_cnt_per_month, y='mnth', x='cnt', palette=colors, hue='mnth', ax=axs[0, 1])
    for i, row in mean_cnt_per_month.iterrows():
        axs[0, 1].text(row['cnt'] + 1, row['mnth'], round(row['cnt']), va='center', color='black')
    axs[0, 1].set_title('Rata-Rata Jumlah Perentalan Sepeda Berdasarkan Bulan')
    axs[0, 1].set_xlabel('Rata-Rata Jumlah')
    axs[0, 1].set_ylabel('Bulan')

    # Visualisasi 3
    mean_cnt_per_hour = hour_df_filtered.groupby('hr')['cnt'].mean().reset_index()
    sns.lineplot(data=mean_cnt_per_hour, x='hr', y='cnt', marker='o', color='#72BCD4', ax=axs[1, 0])
    axs[1, 0].set_title('Rata-Rata Jumlah Perentalan Sepeda per Jam')
    axs[1, 0].set_xlabel('Jam')
    axs[1, 0].set_ylabel('Rata-Rata Jumlah')
    axs[1, 0].set_xticks(range(0, 24))
    axs[1, 0].grid(True)

    # Visualisasi 4
    mean_cnt_per_weekday = hour_df_filtered.groupby('weekday', observed=True)['cnt'].mean().reset_index()
    weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    mean_cnt_per_weekday['weekday'] = pd.Categorical(mean_cnt_per_weekday['weekday'], categories=weekday_order, ordered=True)
    mean_cnt_per_weekday = mean_cnt_per_weekday.sort_values('weekday')
    # Tentukan warna berdasarkan tahun yang dipilih
    if tahun_pilihan == 'Gabungan':
        colors = ["#D3D3D3"]*4 + ["#72BCD4"]*2 + ["#D3D3D3"]
    elif tahun_pilihan == 2011:
        colors = ["#D3D3D3"]*2 + ["#72BCD4"] + ["#D3D3D3"]*4
    elif tahun_pilihan == 2012:
        colors = ["#D3D3D3"]*4 + ["#72BCD4"] + ["#D3D3D3"]*2
    sns.barplot(data=mean_cnt_per_weekday, y='weekday', x='cnt', palette=colors, hue='weekday', ax=axs[1, 1])
    for i, row in mean_cnt_per_weekday.iterrows():
        axs[1, 1].text(row['cnt'] + 1, row['weekday'], round(row['cnt']), va='center', color='black')
    axs[1, 1].set_title('Rata-Rata Jumlah Perentalan Sepeda Berdasarkan Hari')
    axs[1, 1].set_xlabel('Rata-Rata Jumlah')
    axs[1, 1].set_ylabel('Hari')

    # Visualisasi 5
    sum_cnt_per_workingday = hour_df_filtered.groupby('workingday')['cnt'].mean().reset_index()
    colors = ["#D3D3D3", "#72BCD4"]
    sns.barplot(data=sum_cnt_per_workingday, x='workingday', y='cnt', palette=colors, hue='workingday', legend=False, ax=axs[2, 0])
    for index, row in sum_cnt_per_workingday.iterrows():
        axs[2, 0].text(index, row['cnt'], round(row['cnt']), color='black', ha="center", va="bottom")
    axs[2, 0].set_title('Jumlah Perentalan Sepeda Berdasarkan Kondisi Hari')
    axs[2, 0].set_xlabel('Libur/Tidak')
    axs[2, 0].set_ylabel('Jumlah')

    # Kosongkan subplot terakhir
    axs[2, 1].axis('off')
    # Tampilkan di Streamlit
    st.pyplot(fig)

    st.text('Berdasarkan hasil analisis data, waktu di mana jumlah perentalan sepeda tertinggi terjadi pada waktu berikut:')
    st.text('Musim: Fall (Musim Gugur) -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Bulan: Juni (2011), September (2012), dan Juni & September (Tahun Gabungan)')
    st.text('Jam: 17:00 (5 sore) -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Hari: Selasa (2011), Kamis (2012), dan Kamis & Jumat (Tahun Gabungan)')
    st.text('Kondisi Hari: Tidak Libur (Hari Kerja) -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Sedangkan untuk waktu di mana jumlah perentalan sepeda terendah terjadi pada waktu berikut:')
    st.text('Musim: Spring (Musim Semi) -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Bulan: Januari -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Jam: 04:00 (4 pagi) -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Hari: Rabu (2011) dan Minggu (2012 & Tahun Gabungan)')
    st.text('Kondisi Hari: Libur -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')

with tab3:
    st.subheader("Pertanyaan 2: Bagaimana pengaruh cuaca terhadap jumlah pengguna sepeda (baik kasual maupun terdaftar)?")
    st.text('Untuk menjawab pertanyaan ini, kita akan membuat visualisasi jumlah penyewa sepeda berdasarkan kondisi cuaca, suhu sebenarnya, suhu yang dirasakan, kelembapan, dan kecepatan angin.')
    
    st.text('Visualisasi ini akan membantu kita memahami bagaimana pengaruh cuaca terhadap jumlah perentalan sepeda.')
    # Pilihan tahun
    tahun_pilihan2 = st.selectbox(
        'Pilih Tahun Data yang Ditampilkan:',
        options=['Gabungan', 2011, 2012],
        index=0,  # default: Gabungan
        key='tahun_tab3'
    )

    # Filter dataframe berdasarkan pilihan
    if tahun_pilihan2 == 'Gabungan':
        hour_df_filtered2 = hour_df.copy()  # tidak difilter
    else:
        hour_df_filtered2 = hour_df[hour_df['yr'] == tahun_pilihan2]
    
    # Buat kanvas visualisasi
    fig, axs = plt.subplots(3, 2, figsize=(16, 14))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Visualisasi 1
    mean_cnt_per_weathersit = hour_df_filtered2.groupby('weathersit')['cnt'].mean().reset_index()
    max_value = mean_cnt_per_weathersit['cnt'].max()
    colors = ['#72BCD4' if val == max_value else '#D3D3D3' for val in mean_cnt_per_weathersit['cnt']]
    sns.barplot(data=mean_cnt_per_weathersit, x='weathersit', y='cnt', palette=colors, hue='weathersit', legend=False, ax=axs[0, 0])
    for index, row in mean_cnt_per_weathersit.iterrows():
        axs[0, 0].text(index, row['cnt'], round(row['cnt']), color='black', ha="center", va="bottom")
    axs[0, 0].set_title('Rata-Rata Jumlah Perentalan Sepeda Berdasarkan Kondisi Cuaca')
    axs[0, 0].set_xlabel('Kondisi Cuaca')
    axs[0, 0].set_ylabel('Rata-Rata Jumlah')

    # Visualisasi 2
    hour_df_filtered2['temp_bin'] = pd.cut(hour_df_filtered2['temp_actual'], bins=np.arange(0, 43, 6))
    temp = hour_df_filtered2.groupby('temp_bin', observed=True)['cnt'].sum().reset_index()
    max_val = temp['cnt'].max()
    colors = ['#72BCD4' if val == max_val else '#D3D3D3' for val in temp['cnt']]
    sns.barplot(data=temp, x='temp_bin', y='cnt', hue='temp_bin', palette=colors, legend=False, ax=axs[0,1])
    axs[0, 1].set_title('Jumlah Perentalan Sepeda Berdasarkan Suhu Sebenarnya')
    axs[0, 1].set_xlabel('Suhu Sebenarnya (°C)')
    axs[0, 1].set_ylabel('Jumlah')

    # Visualisasi 3
    hour_df_filtered2['atemp_bin'] = pd.cut(hour_df_filtered2['atemp_actual'], bins=np.arange(0, 51, 5))
    atemp = hour_df_filtered2.groupby('atemp_bin', observed=True)['cnt'].sum().reset_index()
    max_val = atemp['cnt'].max()
    colors = ['#72BCD4' if val == max_val else '#D3D3D3' for val in atemp['cnt']]
    sns.barplot(data=atemp, x='atemp_bin', y='cnt', hue='atemp_bin', palette=colors, legend=False, ax=axs[1, 0])
    axs[1, 0].set_title('Jumlah Perentalan Sepeda Berdasarkan Suhu yang Dirasakan')
    axs[1, 0].set_xlabel('Suhu yang Dirasakan (°C)')
    axs[1, 0].set_ylabel('Jumlah')

    # Visualisasi 4
    hour_df_filtered2['hum_bin'] = pd.cut(hour_df_filtered2['hum_actual'], bins=np.arange(0, 101, 10))
    hum = hour_df_filtered2.groupby('hum_bin', observed=True)['cnt'].sum().reset_index()
    max_val = hum['cnt'].max()
    colors = ['#72BCD4' if val == max_val else '#D3D3D3' for val in hum['cnt']]
    sns.barplot(data=hum, x='hum_bin', y='cnt', hue='hum_bin', palette=colors, legend=False, ax=axs[1, 1])
    axs[1, 1].set_title('Jumlah Perentalan Sepeda Berdasarkan Kelembapan')
    axs[1, 1].set_xlabel('Kelembapan')
    axs[1, 1].set_ylabel('Jumlah')

    # Visualisasi 5
    hour_df_filtered2['windspeed_bin'] = pd.cut(hour_df_filtered2['windspeed_actual'], bins=np.arange(0, 67, 7))
    wind = hour_df_filtered2.groupby('windspeed_bin', observed=True)['cnt'].sum().reset_index()
    max_val = wind['cnt'].max()
    colors = ['#72BCD4' if val == max_val else '#D3D3D3' for val in wind['cnt']]
    sns.barplot(data=wind, x='windspeed_bin', y='cnt', hue='windspeed_bin', palette=colors, legend=False, ax=axs[2, 0])
    axs[2, 0].set_title('Jumlah Perentalan Sepeda Berdasarkan Kecepatan Angin')
    axs[2, 0].set_xlabel('Kecepatan Angin')
    axs[2, 0].set_ylabel('Jumlah')

    # Kosongkan subplot terakhir
    axs[2, 1].axis('off')
    # Tampilkan di Streamlit
    st.pyplot(fig)

    st.text('Berdasarkan hasil analisis data, kondisi cuaca di mana jumlah perentalan sepeda tertinggi terjadi pada kondisi cuaca berikut:')
    st.text('Kondisi: Cerah dan sedikit berawan -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Suhu Sebenarnya: 24°C-30°C -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Suhu yang Dirasakan: 30°C-35°C -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Kelembapan: 50-60 (2011), 30-40 (2012), dan 40-50 (Tahun Gabungan)')
    st.text('Kecepatan Angin: 7-14 -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Sedangkan untuk kondisi cuaca di mana jumlah perentalan sepeda terendah terjadi pada kondisi cuaca berikut:')
    st.text('Kondisi: Hujan lebat, bersalju, badai, mendung, dan berkabut -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Suhu Sebenarnya: 0°C-6°C -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Suhu yang Dirasakan: 0°C-5°C -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Kelembapan: 0-10 -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Kecepatan Angin: 56-63 -> Pada Kedua Tahun (2011 & 2012) dan Tahun Gabungan')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')
    st.text('1. Kondisi cuaca yang cerah membuat orang-orang lebih ingin merental sepeda, sedangkan jika turun hujan hingga badai, jumlah perentalan sepeda semakin sedikit.')
    st.text('2. Untuk kondisi suhu, suhu normal (yaitu pada rentang 24-30°C) adalah suhu terbaik untuk merental sepeda. Suhu yang lebih dingin (berkisar antara 18-24°C) juga lebih menarik minat orang untuk merental sepeda dibanding suhu yang lebih panas (berkisar antara 30-36°C)')
    st.text('3. Kelembapan yang paling menarik minat orang-orang untuk merental sepeda ada pada angka 40-50.')
    st.text('4. Kecepatan angin yang paling menarik minat orang-orang untuk meerntal sepeda ada pada angka 7-14. Hal ini agak kontra pada proses EDA yang menyatakan maksimal jumlah perentalan sepeda terbanyak ada pada kecepatan angin 0, kemungkinan penyebabnya adalah kesalahan input data.')
    st.text('Maka dari itu, penyedia jasa perentalan sepeda dapat meningkatkan suplai sepeda yang akan direntalkan berdasarkan kondisi di tertinggi yang telah disebutkan di atas dan sebaliknya, penyedia dapat mengurangi suplai sepeda yang akan direntalkan berdasarkan kondisi terendah untuk tujuan efisiensi dan menghindari kejadian yang tidak diinginkan.')