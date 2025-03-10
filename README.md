# 🚲 Bike Sharing Analysis Dashboard

<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/bike-sharing-logo.png" alt="Bike Sharing Logo" width="200"/>
</p>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bike-sharing-analysis.streamlit.app/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive dashboard for analyzing bike sharing patterns and trends using Streamlit.

## 📋 Project Description

This dashboard analyzes bike sharing data to identify usage patterns and trends. The dashboard includes several analytical features:

<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/dashboard-preview.png" alt="Dashboard Preview" width="650"/>
</p>

- **Overview**: Display of key metrics and monthly trends
- **Time Analysis**: Analysis of usage patterns by hour, day, and season
- **Weather Analysis**: Weather impact on bike rentals
- **Clustering**: Hourly rental pattern cluster analysis

## 🔍 Data Source

The analysis is based on the [Bike Sharing Dataset](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset) from the UCI Machine Learning Repository, which contains:
- Historical usage patterns 
- Weather conditions
- Temporal information

## 🛠️ Project Structure

```
bike-sharing-dashboard/
│
├── dashboard/
│   └── dashboard.py       # Main Streamlit application file
│
├── data/
│   ├── day.csv            # Daily dataset
│   └── hour.csv           # Hourly dataset
│
├── assets/                # Images and other static assets
│
├── README.md              # Project documentation
├── requirements.txt       # Required packages list
├── notebook.ipynb         # Data analysis notebook
├── rangkuman_insight.txt  # Analysis insights summary
└── url.txt                # Streamlit cloud dashboard URL
```

## ⚙️ Setup Environment

<p align="center">
  <img src="https://raw.githubusercontent.com/python/cpython/main/Lib/test/python.png" height="40"/>
  <img src="https://raw.githubusercontent.com/pandas-dev/pandas/main/web/pandas/static/img/pandas_mark.svg" height="40"/>
  <img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" height="40"/>
  <img src="https://seaborn.pydata.org/_static/logo-wide-lightbg.svg" height="40"/>
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg" height="40"/>
  <img src="https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png" height="40"/>
</p>

### Using Anaconda

```bash
# Create a new environment
conda create --name bike-env python=3.10
# Activate the environment
conda activate bike-env
# Install required packages
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### Using Python venv

```bash
# Create virtual environment
python -m venv venv
# Activate environment (Windows)
venv\Scripts\activate
# Activate environment (Linux/Mac)
source venv/bin/activate
# Install required packages
pip install streamlit pandas numpy matplotlib seaborn scikit-learn
```

### Using requirements.txt

You can also install all required packages directly using the requirements.txt file:

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

1. Ensure the directory structure is correct with the `data` folder containing CSV files in the right location
2. Navigate to the dashboard directory with your terminal
3. Run the application with the command:

```bash
streamlit run dashboard.py
```

4. The application will automatically open in your browser at the default address:
   - Local URL: http://localhost:8501
   - Network URL: http://192.168.xxx.xxx:8501

## 📊 Dashboard Features

### 1. Overview
<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/overview.png" alt="Overview" width="500"/>
</p>

- Total rentals, average daily rentals, and total days metrics
- Monthly average bike rental trend visualization

### 2. Time Analysis
<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/time-analysis.png" alt="Time Analysis" width="500"/>
</p>

- Rental patterns by hour
- Rental patterns by day of week
- Rental patterns by season

### 3. Weather Analysis
<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/weather-analysis.png" alt="Weather Analysis" width="500"/>
</p>

- Impact of weather conditions on rental numbers
- Relationship between temperature and rentals

### 4. Clustering
<p align="center">
  <img src="https://raw.githubusercontent.com/username/bike-sharing-dashboard/main/assets/clustering.png" alt="Clustering" width="500"/>
</p>

- Cluster analysis to identify rental patterns based on hour and day

## 📈 Key Insights

- Bike rentals peak during morning (8-9 AM) and evening (5-6 PM) rush hours on weekdays
- Weekend patterns show more distributed usage throughout the day
- Weather significantly impacts rental volume, with clear conditions showing 40% higher rentals than rainy days
- Temperature has a strong positive correlation with rental numbers up to 30°C
- Seasonal variation shows highest usage in summer and lowest in winter

## ⚠️ Troubleshooting

If you get an error like:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/day.csv'
```

Ensure that:
1. The `data` folder is in the correct location (preferably in the same folder as the `dashboard.py` file)
2. The `day.csv` and `hour.csv` files are inside the `data` folder
3. The path in the code is correct. If needed, modify the path in the `dashboard.py` file:
   ```python
   day_data = pd.read_csv('data/day.csv')
   hour_data = pd.read_csv('data/hour.csv')
   ```
   to:
   ```python
   day_data = pd.read_csv('../data/day.csv')
   hour_data = pd.read_csv('../data/hour.csv')
   ```
   or use an absolute path if necessary.

## 💻 Technologies Used

- **Streamlit** (v1.43.1): Interactive dashboard framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical calculations
- **Matplotlib & Seaborn**: Data visualization
- **Scikit-learn**: Machine learning for clustering analysis

## 📝 Additional Notes

- This dashboard uses Streamlit version 1.43.1
- The data used is a bike sharing dataset containing rental information based on various factors such as weather, season, day, etc.
- The clustering analysis uses K-means to identify similar usage patterns

## 📚 Author

Muhammad Hasan Fadhlillah
