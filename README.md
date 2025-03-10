# 🚲 Bike Sharing Analysis Dashboard

<div align="center">
  <img src="/api/placeholder/800/300" alt="Bike Sharing Dashboard Banner"/>
  <br><br>
  <p>Sebuah dashboard interaktif untuk menganalisis pola dan tren penggunaan sepeda menggunakan Streamlit.</p>
  <br>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" alt="Python 3.10"/>
    <img src="https://img.shields.io/badge/Streamlit-1.43.1-FF4B4B?logo=streamlit" alt="Streamlit"/>
    <img src="https://img.shields.io/badge/Pandas-Latest-150458?logo=pandas" alt="Pandas"/>
    <img src="https://img.shields.io/badge/Scikit--learn-Latest-F7931E?logo=scikit-learn" alt="Scikit-learn"/>
    <img src="https://img.shields.io/badge/Matplotlib-Latest-11557c?logo=python" alt="Matplotlib"/>
    <img src="https://img.shields.io/badge/Seaborn-Latest-7db0bc?logo=python" alt="Seaborn"/>
  </p>
</div>

## 📋 Project Description

Dashboard ini menganalisis data bike sharing untuk mengidentifikasi pola dan tren penggunaan. Dashboard ini mencakup beberapa fitur analisis:

- **Overview**: Tampilan metrik utama dan tren bulanan
- **Time Analysis**: Analisis pola penggunaan berdasarkan jam, hari, dan musim
- **Weather Analysis**: Dampak cuaca terhadap jumlah penyewaan sepeda
- **Clustering**: Analisis pengelompokan pola penyewaan per jam

<div align="center">
  <img src="/api/placeholder/600/250" alt="Dashboard Preview"/>
</div>

## 🛠️ Project Structure

```
bike-sharing-dashboard/
│
├── dashboard/
│   └── dashboard.py       # File utama aplikasi Streamlit
│
├── data/
│   ├── day.csv            # Dataset per hari
│   └── hour.csv           # Dataset per jam
│
├── README.md              # Dokumentasi proyek
├── requirements.txt       # Daftar package yang dibutuhkan
├── notebook.ipynb         # Notebook analisis data
├── rangkuman_insight.txt  # Rangkuman insight analisis data
└── url.txt                # URL dashboard streamlit cloud
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

## 🚀 Running the Application

1. Pastikan struktur direktori sudah benar dengan folder `data` yang berisi file CSV berada di tempat yang tepat
2. Arahkan terminal ke direktori dashboard
3. Jalankan aplikasi dengan perintah:
```bash
streamlit run dashboard.py
```
4. Aplikasi akan terbuka secara otomatis di browser dengan alamat default:
   - Local URL: http://localhost:8501
   - Network URL: http://192.168.xxx.xxx:8501

<div align="center">
  <img src="/api/placeholder/600/180" alt="Application Running"/>
</div>

## 📊 Dashboard Features

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

<div align="center">
  <table>
    <tr>
      <td><img src="/api/placeholder/250/150" alt="Time Analysis"/></td>
      <td><img src="/api/placeholder/250/150" alt="Weather Analysis"/></td>
    </tr>
    <tr>
      <td align="center">Time Analysis</td>
      <td align="center">Weather Analysis</td>
    </tr>
  </table>
</div>

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

## 📝 Additional Notes

- Dashboard ini menggunakan Streamlit version 1.43.1
- Beberapa library yang digunakan:
  - <img src="/api/placeholder/15/15" alt="Pandas"/> Pandas - Manipulasi data
  - <img src="/api/placeholder/15/15" alt="NumPy"/> NumPy - Operasi numerik
  - <img src="/api/placeholder/15/15" alt="Matplotlib"/> Matplotlib - Visualisasi data
  - <img src="/api/placeholder/15/15" alt="Seaborn"/> Seaborn - Visualisasi data statistik
  - <img src="/api/placeholder/15/15" alt="Scikit-learn"/> Scikit-learn - Machine learning
- Data yang digunakan adalah dataset bike sharing yang berisi informasi penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, hari, dll.

## 📚 Author

Muhammad Hasan Fadhlillah

<div align="center">
  <br>
  <p>
    <a href="#"><img src="/api/placeholder/20/20" alt="GitHub"/> GitHub</a> •
    <a href="#"><img src="/api/placeholder/20/20" alt="LinkedIn"/> LinkedIn</a> •
    <a href="#"><img src="/api/placeholder/20/20" alt="Email"/> Kontak</a>
  </p>
</div>
