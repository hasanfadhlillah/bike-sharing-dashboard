import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import os
from sklearn.preprocessing import StandardScaler
from datetime import datetime

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

# Sidebar navigation and filters
st.sidebar.title("Filters")
page = st.sidebar.radio("Navigation", ["Overview", "Time Analysis", "Weather Analysis", "Clustering"])

# Date range filter (applies to all pages)
min_date = day_data['dteday'].min()
max_date = day_data['dteday'].max()
start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Convert to datetime
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter data based on date range
day_data_filtered = day_data[(day_data['dteday'] >= start_date) & (day_data['dteday'] <= end_date)]
hour_data_filtered = hour_data[(hour_data['dteday'] >= start_date) & (hour_data['dteday'] <= end_date)]

if page == "Overview":
    st.title("🚲 Bike Sharing Analysis Dashboard")
    st.markdown("Analyze bike sharing patterns based on time and weather conditions.")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rentals", f"{day_data_filtered['cnt'].sum():,}")
    with col2:
        st.metric("Average Daily Rentals", f"{int(day_data_filtered['cnt'].mean()):,}")
    with col3:
        st.metric("Days Analyzed", f"{len(day_data_filtered):,}")
    
    # Monthly trend with interactive filter
    st.subheader("Monthly Rental Trends")
    
    # Add season filter
    selected_seasons = st.multiselect(
        "Select Seasons",
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        default=['Spring', 'Summer', 'Fall', 'Winter']
    )
    
    monthly_data = day_data_filtered[day_data_filtered['season_name'].isin(selected_seasons)]
    monthly_rentals = monthly_data.groupby('month_name')['cnt'].mean().reindex(list(calendar.month_name)[1:])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=monthly_rentals.index, y=monthly_rentals.values, ax=ax, palette="Blues_d")
    plt.title("Average Daily Rentals by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Rentals")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Time Analysis":
    st.title("⏰ Time-based Analysis")
    
    # Interactive tabs for different time dimensions
    tab1, tab2, tab3 = st.tabs(["Hourly", "Daily", "Seasonal"])
    
    with tab1:
        st.subheader("Hourly Rental Pattern")
        
        # Add day type filter
        day_type = st.selectbox(
            "Select Day Type",
            options=["All Days", "Weekdays", "Weekends"],
            index=0
        )
        
        if day_type == "Weekdays":
            hour_data_filtered = hour_data_filtered[hour_data_filtered['weekday'].isin([1,2,3,4,5])]
        elif day_type == "Weekends":
            hour_data_filtered = hour_data_filtered[hour_data_filtered['weekday'].isin([0,6])]
        
        hourly_rentals = hour_data_filtered.groupby('hr')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker='o', ax=ax, color='darkblue', linewidth=2)
        plt.title(f"Average Rentals by Hour ({day_type})")
        plt.xlabel("Hour of Day")
        plt.ylabel("Average Rentals")
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Daily Rental Pattern")
        
        daily_rentals = day_data_filtered.groupby('weekday_name')['cnt'].mean().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=daily_rentals.index, y=daily_rentals.values, ax=ax, palette="Blues_d")
        plt.title("Average Rentals by Day of Week")
        plt.xlabel("Day of Week")
        plt.ylabel("Average Rentals")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Seasonal Rental Pattern")
        
        seasonal_rentals = day_data_filtered.groupby('season_name')['cnt'].mean().reindex(
            ['Spring', 'Summer', 'Fall', 'Winter']
        )
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=seasonal_rentals.index, y=seasonal_rentals.values, ax=ax, palette="Blues_d")
        plt.title("Average Rentals by Season")
        plt.xlabel("Season")
        plt.ylabel("Average Rentals")
        st.pyplot(fig)

elif page == "Weather Analysis":
    st.title("🌤️ Weather Impact Analysis")
    
    # Interactive tabs for different weather visualizations
    tab1, tab2 = st.tabs(["Weather Conditions", "Temperature Impact"])
    
    with tab1:
        st.subheader("Impact of Weather Conditions")
        
        # Add weather type filter
        weather_types = st.multiselect(
            "Select Weather Types",
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
        plt.title("Distribution of Rentals by Weather Condition")
        plt.xlabel("Weather Condition")
        plt.ylabel("Number of Rentals")
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Temperature vs Rentals")
        
        # Add season filter
        selected_seasons = st.multiselect(
            "Select Seasons for Temperature Analysis",
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
        plt.title("Temperature vs Total Rentals")
        plt.xlabel("Normalized Temperature")
        plt.ylabel("Total Rentals")
        plt.legend(title="Season")
        st.pyplot(fig)

elif page == "Clustering":
    st.title("📊 Clustering Analysis")
    
    st.subheader("Hourly Rental Patterns Clustering")
    
    # Create pivot table for hourly patterns
    hourly_pattern = hour_data_filtered.pivot_table(
        index='weekday', 
        columns='hr', 
        values='cnt', 
        aggfunc='mean'
    )
    
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
        plt.plot(
            hourly_counts.index,
            hourly_counts.values,
            marker='o',
            linewidth=2,
            label=f'Cluster {cluster+1}'
        )
    
    plt.title("Hourly Rental Patterns by Cluster")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Rentals")
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
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
        st.markdown(f"**{cluster}**: {', '.join(days)}")
        
        if cluster == "Cluster 1":
            st.markdown("- **Pattern**: Two peaks at 8 AM and 5-6 PM")
            st.markdown("- **Interpretation**: Typical commuting pattern")
        elif cluster == "Cluster 2":
            st.markdown("- **Pattern**: Gradual increase peaking at noon")
            st.markdown("- **Interpretation**: Weekend recreational use")
        else:
            st.markdown("- **Pattern**: Lower activity peaking midday")
            st.markdown("- **Interpretation**: Sunday leisure pattern")