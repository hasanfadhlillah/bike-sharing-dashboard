# 🚲 Bike Sharing Analysis Dashboard

Sebuah dashboard interaktif untuk menganalisis pola dan tren penggunaan sepeda menggunakan Streamlit.

## 📋 Deskripsi Proyek

Dashboard ini menganalisis data bike sharing untuk mengidentifikasi pola dan tren penggunaan. Dashboard ini mencakup beberapa fitur analisis:

- **Overview**: Tampilan metrik utama dan tren bulanan
- **Time Analysis**: Analisis pola penggunaan berdasarkan jam, hari, dan musim
- **Weather Analysis**: Dampak cuaca terhadap jumlah penyewaan sepeda
- **Clustering**: Analisis pengelompokan pola penyewaan per jam

## 🛠️ Struktur Proyek

```
bike-sharing-dashboard/
│
├── dashboard/
│   └── dashboard.py      # File utama aplikasi Streamlit
│
├── data/
│   ├── day.csv           # Dataset per hari
│   └── hour.csv          # Dataset per jam
│
├── README.md             # Dokumentasi proyek
├── requirements.txt      # Daftar package yang dibutuhkan
├── notebook.ipynb
├── rangkuman_insight.txt
└── url.txt
```

## ⚙️ Setup Environment

### Menggunakan Anaconda

```bash
# Membuat environment baru
conda create --name bike-env python=3.10

# Mengaktifkan environment
conda activate bike-env

# Menginstall package yang dibutuhkan
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### Menggunakan Python venv

```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan environment (Windows)
venv\Scripts\activate

# Mengaktifkan environment (Linux/Mac)
source venv/bin/activate

# Menginstall package yang dibutuhkan
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### Menggunakan requirements.txt

Anda juga dapat menginstall semua package yang dibutuhkan secara langsung menggunakan file requirements.txt:

```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Aplikasi

1. Pastikan struktur direktori sudah benar dengan folder `data` yang berisi file CSV berada di tempat yang tepat
2. Arahkan terminal ke direktori dashboard
3. Jalankan aplikasi dengan perintah:

```bash
streamlit run dashboard.py
```

4. Aplikasi akan terbuka secara otomatis di browser dengan alamat default:
   - Local URL: http://localhost:8501
   - Network URL: http://192.168.xxx.xxx:8501

## 📊 Fitur Dashboard

### 1. Overview

- Metrik total penyewaan, rata-rata penyewaan harian, dan total hari
- Visualisasi tren bulanan rata-rata penyewaan sepeda

### 2. Time Analysis

- Pola penyewaan berdasarkan jam
- Pola penyewaan berdasarkan hari dalam seminggu
- Pola penyewaan berdasarkan musim

### 3. Weather Analysis

- Dampak kondisi cuaca terhadap jumlah penyewaan
- Hubungan suhu dengan jumlah penyewaan

### 4. Clustering

- Analisis klaster untuk mengidentifikasi pola penyewaan berdasarkan jam dan hari

## ⚠️ Troubleshooting

Jika Anda mendapatkan error seperti berikut:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/day.csv'
```

Pastikan bahwa:

1. Folder `data` berada di lokasi yang benar (sebaiknya di folder yang sama dengan file `dashboard.py`)
2. File `day.csv` dan `hour.csv` berada di dalam folder `data`
3. Pastikan path pada kode benar. Jika perlu, ubah path di file `dashboard.py`:
   ```python
   day_data = pd.read_csv('data/day.csv')
   hour_data = pd.read_csv('data/hour.csv')
   ```
   menjadi:
   ```python
   day_data = pd.read_csv('../data/day.csv')
   hour_data = pd.read_csv('../data/hour.csv')
   ```
   atau path absolut jika diperlukan.

## 📝 Catatan Tambahan

- Dashboard ini menggunakan Streamlit version 1.43.1
- Beberapa library yang digunakan: pandas, numpy, matplotlib, seaborn, scikit-learn
- Data yang digunakan adalah dataset bike sharing yang berisi informasi penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, hari, dll.

## 📚 Author

Muhammad Hasan Fadhlillah
