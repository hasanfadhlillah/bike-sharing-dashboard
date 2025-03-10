import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Set page config
st.set_page_config(page_title="Bike Sharing Analysis", page_icon="🚲", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load CSV files using pandas
    day_data_path = os.path.join(script_dir, 'day.csv')
    hour_data_path = os.path.join(script_dir, 'hour.csv')
    
    # Read the CSV files into DataFrames
    day_data = pd.read_csv(day_data_path)
    hour_data = pd.read_csv(hour_data_path)
    
    # Convert date column to datetime
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    
    # Convert categorical columns to category type
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        day_data[col] = day_data[col].astype('category')
        hour_data[col] = hour_data[col].astype('category')
    
    # Add season, month, and weekday names
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

# Load data
day_data, hour_data = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Time Analysis", "Weather Analysis", "Clustering"])

if page == "Overview":
    st.title("🚲 Bike Sharing Analysis Dashboard")
    st.markdown("This dashboard analyzes bike sharing patterns and trends.")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rentals", f"{day_data['cnt'].sum():,}")
    with col2:
        st.metric("Average Daily Rentals", f"{int(day_data['cnt'].mean()):,}")
    with col3:
        st.metric("Total Days", f"{len(day_data):,}")
    
    # Monthly trend
    st.subheader("Monthly Rental Trends")
    monthly_rentals = day_data.groupby('month_name')['cnt'].mean().reindex(list(calendar.month_name)[1:])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values, ax=ax)
    plt.title("Average Daily Rentals by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Rentals")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Time Analysis":
    st.title("⏰ Time-based Analysis")
    
    # Hourly pattern
    st.subheader("Hourly Rental Pattern")
    hourly_rentals = hour_data.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker='o', ax=ax)
    plt.title("Average Rentals by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Rentals")
    st.pyplot(fig)
    
    # Day of week pattern
    st.subheader("Day of Week Pattern")
    weekly_rentals = day_data.groupby('weekday_name')['cnt'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=weekly_rentals.index, y=weekly_rentals.values, ax=ax)
    plt.title("Average Rentals by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Rentals")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Seasonal pattern
    st.subheader("Seasonal Rental Pattern")
    seasonal_rentals = day_data.groupby('season_name')['cnt'].mean().reindex(['Spring', 'Summer', 'Fall', 'Winter'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, ax=ax)
    plt.title("Average Rentals by Season")
    plt.xlabel("Season")
    plt.ylabel("Average Rentals")
    st.pyplot(fig)

elif page == "Weather Analysis":
    st.title("🌤️ Weather Impact Analysis")
    
    # Weather situation impact
    st.subheader("Impact of Weather Situations")
    weather_impact = day_data.groupby('weather_name')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=weather_impact.index, y=weather_impact.values, ax=ax)
    plt.title("Average Rentals by Weather Condition")
    plt.xlabel("Weather Situation")
    plt.ylabel("Average Rentals")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Temperature vs Rentals
    st.subheader("Temperature vs Rentals")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=day_data, x='temp', y='cnt', hue='season_name', ax=ax)
    plt.title("Temperature vs Total Rentals")
    plt.xlabel("Normalized Temperature")
    plt.ylabel("Total Rentals")
    st.pyplot(fig)

elif page == "Clustering":
    st.title("📊 Clustering Analysis")
    
    # Clustering based on hourly patterns
    st.subheader("Clustering of Hourly Rental Patterns")
    
    # Create pivot table for hourly patterns
    hourly_pattern = hour_data.pivot_table(index='weekday', columns='hr', values='cnt', aggfunc='mean')
    
    # Standardize data
    scaler = StandardScaler()
    hourly_pattern_scaled = scaler.fit_transform(hourly_pattern)
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(hourly_pattern_scaled)
    hourly_pattern['cluster'] = cluster_labels
    
    # Visualize clusters
    fig, ax = plt.subplots(figsize=(16, 8))
    for cluster in range(3):
        cluster_data = hourly_pattern[hourly_pattern['cluster'] == cluster].drop('cluster', axis=1)
        hourly_counts = cluster_data.mean()
        plt.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, label=f'Cluster {cluster+1}')
    
    plt.title("Hourly Rental Patterns by Cluster")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Rentals")
    plt.legend()
    st.pyplot(fig)
    
    # Interpret clusters
    st.subheader("Cluster Interpretation")
    cluster_days = {}
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for cluster in range(3):
        days_in_cluster = hourly_pattern[hourly_pattern['cluster'] == cluster].index
        cluster_days[f'Cluster {cluster+1}'] = [weekday_names[day] for day in days_in_cluster]
    
    for cluster, days in cluster_days.items():
        st.write(f"{cluster}: {', '.join(days)}")