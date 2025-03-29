import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", page_icon="🚲", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Memuat file CSV
    day_data_path = os.path.join(script_dir, 'day.csv')
    hour_data_path = os.path.join(script_dir, 'hour.csv')
    
    # Membaca file CSV ke DataFrame
    day_data = pd.read_csv(day_data_path)
    hour_data = pd.read_csv(hour_data_path)
    
    # Konversi kolom tanggal ke datetime
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    
    # Konversi kolom kategorikal
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        day_data[col] = day_data[col].astype('category')
        hour_data[col] = hour_data[col].astype('category')
    
    # Menambahkan nama musim, bulan, dan hari
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    month_mapping = {i: calendar.month_name[i] for i in range(1, 13)}
    weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    
    day_data['season_name'] = day_data['season'].map(season_mapping)
    day_data['month_name'] = day_data['mnth'].map(month_mapping)
    day_data['weekday_name'] = day_data['weekday'].map(weekday_mapping)
    day_data['weather_name'] = day_data['weathersit'].map(weather_mapping)
    
    hour_data['season_name'] = hour_data['season'].map(season_mapping)
    hour_data['month_name'] = hour_data['mnth'].map(month_mapping)
    hour_data['weekday_name'] = hour_data['weekday'].map(weekday_mapping)
    hour_data['weather_name'] = hour_data['weathersit'].map(weather_mapping)
    
    return day_data, hour_data

# Memuat data
day_data, hour_data = load_data()

# Sidebar navigasi dan filter
st.sidebar.title("Filter")
page = st.sidebar.radio("Navigasi", ["Overview", "Analisis Waktu", "Analisis Cuaca", "Analisis Lanjutan"])

# Filter rentang tanggal
min_date = day_data['dteday'].min()
max_date = day_data['dteday'].max()
start_date = st.sidebar.date_input("Tanggal Mulai", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

# Konversi ke datetime
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter data berdasarkan rentang tanggal
day_data_filtered = day_data[(day_data['dteday'] >= start_date) & (day_data['dteday'] <= end_date)]
hour_data_filtered = hour_data[(hour_data['dteday'] >= start_date) & (hour_data['dteday'] <= end_date)]

if page == "Overview":
    st.title("🚲 Bike Sharing Analysis Dashboard")
    st.markdown("Analisis pola penyewaan sepeda berdasarkan waktu dan kondisi cuaca.")
    
    # Metrik utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", f"{day_data_filtered['cnt'].sum():,}")
    with col2:
        st.metric("Rata-rata Penyewaan Harian", f"{int(day_data_filtered['cnt'].mean()):,}")
    with col3:
        st.metric("Jumlah Hari Dianalisis", f"{len(day_data_filtered):,}")
    
    # Tren bulanan dengan filter interaktif
    st.subheader("Tren Penyewaan Bulanan")
    
    # Filter musim
    selected_seasons = st.multiselect(
        "Pilih Musim",
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        default=['Spring', 'Summer', 'Fall', 'Winter']
    )
    
    monthly_data = day_data_filtered[day_data_filtered['season_name'].isin(selected_seasons)]
    monthly_rentals = monthly_data.groupby('month_name')['cnt'].mean().reindex(list(calendar.month_name)[1:])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values, ax=ax, palette="Blues_d")
    plt.title("Rata-rata Penyewaan per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Rata-rata Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Analisis Waktu":
    st.title("⏰ Analisis Berdasarkan Waktu")
    
    # Tab interaktif untuk dimensi waktu berbeda
    tab1, tab2, tab3 = st.tabs(["Per Jam", "Per Hari", "Per Musim"])
    
    with tab1:
        st.subheader("Pola Penyewaan per Jam")
        
        # Filter jenis hari
        day_type = st.selectbox(
            "Pilih Jenis Hari",
            options=["Semua Hari", "Hari Kerja", "Akhir Pekan"],
            index=0
        )
        
        if day_type == "Hari Kerja":
            hour_data_filtered = hour_data_filtered[hour_data_filtered['weekday'].isin([1,2,3,4,5])]
        elif day_type == "Akhir Pekan":
            hour_data_filtered = hour_data_filtered[hour_data_filtered['weekday'].isin([0,6])]
        
        hourly_rentals = hour_data_filtered.groupby('hr')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker='o', ax=ax, color='darkblue', linewidth=2)
        plt.title(f"Rata-rata Penyewaan per Jam ({day_type})")
        plt.xlabel("Jam")
        plt.ylabel("Rata-rata Penyewaan")
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Pola Penyewaan per Hari")
        
        daily_rentals = day_data_filtered.groupby('weekday_name')['cnt'].mean().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=daily_rentals.index, y=daily_rentals.values, ax=ax, palette="Blues_d")
        plt.title("Rata-rata Penyewaan per Hari")
        plt.xlabel("Hari")
        plt.ylabel("Rata-rata Penyewaan")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Pola Penyewaan per Musim")
        
        seasonal_rentals = day_data_filtered.groupby('season_name')['cnt'].mean().reindex(
            ['Spring', 'Summer', 'Fall', 'Winter']
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, ax=ax, palette="Blues_d")
        plt.title("Rata-rata Penyewaan per Musim")
        plt.xlabel("Musim")
        plt.ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

elif page == "Analisis Cuaca":
    st.title("🌤️ Analisis Dampak Cuaca")
    
    # Tab interaktif untuk visualisasi cuaca berbeda
    tab1, tab2 = st.tabs(["Kondisi Cuaca", "Pengaruh Suhu"])
    
    with tab1:
        st.subheader("Dampak Kondisi Cuaca")
        
        # Filter jenis cuaca
        weather_types = st.multiselect(
            "Pilih Jenis Cuaca",
            options=['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'],
            default=['Clear', 'Mist', 'Light Snow/Rain']
        )
        
        weather_data = day_data_filtered[day_data_filtered['weather_name'].isin(weather_types)]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(
            data=weather_data,
            x='weather_name',
            y='cnt',
            order=weather_types,
            ax=ax,
            palette="Blues"
        )
        plt.title("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
        plt.xlabel("Kondisi Cuaca")
        plt.ylabel("Jumlah Penyewaan")
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Hubungan Suhu dengan Penyewaan")
        
        # Filter musim
        selected_seasons = st.multiselect(
            "Pilih Musim untuk Analisis Suhu",
            options=['Spring', 'Summer', 'Fall', 'Winter'],
            default=['Summer', 'Fall']
        )
        
        temp_data = day_data_filtered[day_data_filtered['season_name'].isin(selected_seasons)]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(
            data=temp_data,
            x='temp',
            y='cnt',
            hue='season_name',
            ax=ax,
            palette="Set1"
        )
        plt.title("Hubungan Suhu dengan Jumlah Penyewaan")
        plt.xlabel("Suhu (°C)")
        plt.ylabel("Jumlah Penyewaan")
        plt.legend(title="Musim")
        st.pyplot(fig)

elif page == "Analisis Lanjutan":
    st.title("📊 Analisis Lanjutan")
    
    st.subheader("Pola Penyewaan per Jam Berdasarkan Hari")
    
    # Membuat pivot table untuk pola per jam
    hourly_pattern = hour_data_filtered.pivot_table(
        index='weekday_name', 
        columns='hr', 
        values='cnt', 
        aggfunc='mean'
    )
    
    # Mengelompokkan secara manual
    weekday_pattern = hourly_pattern.loc[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].mean()
    saturday_pattern = hourly_pattern.loc['Saturday']
    sunday_pattern = hourly_pattern.loc['Sunday']
    
    # Visualisasi hasil grouping manual
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.plot(weekday_pattern.index, weekday_pattern.values, marker='o', linewidth=2, label='Hari Kerja (Senin-Jumat)')
    plt.plot(saturday_pattern.index, saturday_pattern.values, marker='o', linewidth=2, label='Sabtu')
    plt.plot(sunday_pattern.index, sunday_pattern.values, marker='o', linewidth=2, label='Minggu')
    
    plt.title("Pola Penyewaan Sepeda Per Jam Berdasarkan Hari")
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata Jumlah Penyewaan")
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    st.pyplot(fig)
    
    # Interpretasi pola
    st.subheader("Interpretasi Pola")
    st.markdown("""
    - **Hari Kerja (Senin-Jumat):**  
      - Terlihat **dua puncak jelas** di jam **8 pagi** dan **17-18 sore**, menunjukkan pola khas **commuting** (pergi/pulang kerja).  
      - Penyewaan rendah di jam **10 malam hingga 4 pagi**.  
    - **Sabtu:**  
      - Pola lebih landai dengan puncak di **siang hari (12-16)**.  
      - Menunjukkan penggunaan untuk **aktivitas rekreasi** di akhir pekan.  
    - **Minggu:**  
      - Puncak lebih rendah dibanding Sabtu, terjadi di **11 pagi-14 siang**.  
      - Pola lebih santai, mungkin untuk aktivitas keluarga atau olahraga ringan.  
    """)
    
    st.subheader("Rekomendasi:")
    st.markdown("""
    - **Optimalkan ketersediaan sepeda** di jam sibuk weekdays (7-9 pagi dan 16-18 sore).  
    - **Tawarkan paket weekend** di Sabtu-Minggu (contoh: sewa 4 jam dengan diskon).  
    - **Kurangi operasional** di dini hari (00.00-05.00) karena permintaan sangat rendah.  
    """)
    
    # RFM Analysis sederhana
    st.subheader("Segmentasi Pengguna Terdaftar (RFM Analysis)")
    
    rfm_data = day_data_filtered.copy()
    rfm_data['recency'] = (rfm_data['dteday'].max() - rfm_data['dteday']).dt.days
    rfm_data['frequency'] = rfm_data.groupby('weekday')['registered'].transform('count')
    rfm_data['monetary'] = rfm_data['registered']
    
    # Segmentasi manual
    rfm_data['segment'] = 'Low'
    rfm_data.loc[(rfm_data['recency'] <= 30) & 
                 (rfm_data['frequency'] >= 20) & 
                 (rfm_data['monetary'] >= 3000), 'segment'] = 'High'
    rfm_data.loc[(rfm_data['recency'] <= 60) & 
                 (rfm_data['frequency'] >= 15) & 
                 (rfm_data['monetary'] >= 2000), 'segment'] = 'Medium'
    
    # Visualisasi
    segment_counts = rfm_data['segment'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=segment_counts.index, y=segment_counts.values, palette='Blues_d')
    plt.title('Segmentasi Pengguna Terdaftar Berdasarkan RFM')
    plt.xlabel('Segment')
    plt.ylabel('Jumlah Hari')
    st.pyplot(fig)
    
    st.subheader("Interpretasi Segmentasi RFM")
    st.markdown("""
    - **High Value:**  
      - Hari dengan aktivitas pengguna terdaftar **tinggi** (recency ≤30 hari, frekuensi ≥20, penyewaan ≥3000).  
      - Contoh: Hari kerja di musim panas dengan cuaca cerah.  
    - **Medium Value:**  
      - Aktivitas **sedang** (recency ≤60 hari, frekuensi ≥15, penyewaan ≥2000).  
    - **Low Value:**  
      - Hari dengan **aktivitas minimal**, seperti musim dingin atau cuaca buruk.  
    """)
    
    st.subheader("Rekomendasi Segmentasi RFM:")
    st.markdown("""
    - **Pertahankan High Value Days**:  
      - Berikan layanan premium (contoh: prioritas peminjaman sepeda).  
    - **Tingkatkan Low Value Days**:  
      - Promosi diskon 20-30% atau paket bulanan untuk menarik pengguna.  
    - **Analisis penyebab**:  
      - Cek apakah Low Value Days terkait cuaca/musim, lalu siapkan strategi mitigasi.  
    """)