import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_hour = pd.read_csv('hour.csv')

# Data Preprocessing
df_hour['season'] = df_hour['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_hour['holiday'] = df_hour['holiday'].map({0: 'Not Holiday', 1: 'Holiday'})
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Sidebar for Date Filtering
with st.sidebar:
    st.header("Filter Data")
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=df_hour['dteday'].min(),
        max_value=df_hour['dteday'].max(),
        value=[df_hour['dteday'].min(), df_hour['dteday'].max()]
    )

# Filter data based on date range (corrected)
filtered_df = df_hour[(df_hour['dteday'] >= pd.to_datetime(start_date)) & 
                    (df_hour['dteday'] <= pd.to_datetime(end_date))]

# Calculate total rentals
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()
total_all = total_casual + total_registered

# Display Metrics
st.title("Bike Sharing Data Explorer")
col1, col2, col3 = st.columns(3)
col1.metric("Total Casual", value=total_casual)
col2.metric("Total Registered", value=total_registered)
col3.metric("Total All", value=total_all)

# Visualizations
st.subheader("Jumlah Penyewa Sepeda Harian")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='dteday', y='cnt', data=filtered_df, ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewa")
plt.title("Jumlah Penyewa Sepeda Harian")
st.pyplot(fig)

st.subheader("Performa Penyewa Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='season', data=filtered_df, hue='season', palette='magma', ax=ax)
plt.title("Jumlah Penyewa Sepeda per Musim")
st.pyplot(fig)

st.subheader("Performa Penyewa Sepeda Berdasarkan Hari Libur")
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='holiday', data=filtered_df, hue='holiday', palette='coolwarm', ax=ax)
plt.title("Jumlah Penyewa Sepeda pada Hari Libur")
st.pyplot(fig)

st.subheader("Jam Penyewaan Terbanyak")
hourly_counts = filtered_df.groupby('hr')['cnt'].sum()
max_hour = hourly_counts.idxmax()
max_count = hourly_counts.max()
st.write(f"Jam penyewaan terbanyak adalah pukul {max_hour} dengan jumlah {max_count} penyewaan.")

fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(hourly_counts.index, hourly_counts)
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.title('Jumlah Penyewaan Sepeda per Jam')
plt.xticks(range(24))
plt.grid(True)
st.pyplot(fig)

st.subheader("Jumlah Pengguna Casual dan Registered")
plot_data = pd.DataFrame({'penyewa': ['casual', 'registered'], 'cnt': [total_casual, total_registered]})
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(x='penyewa', y='cnt', data=plot_data, palette='pastel', ax=ax)
plt.title("Jumlah Pengguna Sepeda Berdasarkan Tipe")
plt.ylabel("Jumlah Penyewa")
st.pyplot(fig)

st.subheader("Korelasi Antar Atribut")
data = filtered_df[['cnt', 'temp', 'atemp', 'hum', 'windspeed']]
correlation_matrix = data.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
plt.title('Heatmap Korelasi')
st.pyplot(fig)