import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
df_hour = pd.read_csv('hour.csv')

def map_season(x):
    return{
        1:'Springer',
        2:'Summer',
        3:'Fall',
        4:'Winter'
    }.get(x, 'unknown')
df_hour['season'] = df_hour['season'].apply(map_season)

df_hour['holiday'] = df_hour['holiday'].apply(lambda x: {1: 'Holiday', 0: 'Not Holiday'}.get(x, 'unknown'))


# Convert 'dteday' to datetime
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Filter data
min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df_hour[(df_hour["dteday"] >= start_date) & (df_hour["dteday"] <= end_date)]

# Hitung total penyewa
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()
total_all = total_casual + total_registered

# Streamlit app
st.title("Bike Sharing Data Explorer")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Casual", value=total_casual)

with col2:
    st.metric("Total Registered", value=total_registered)

with col3:
    st.metric("Total All", value=total_all)

# Visualisasi jumlah penyewa harian
st.subheader("Jumlah Penyewa Sepeda Harian")
fig, ax = plt.subplots(figsize=(10, 6))  # Variabel fig didefinisikan di sini
sns.lineplot(x='dteday', y='cnt', data=filtered_df, ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewa")
plt.title("Jumlah Penyewa Sepeda Harian")
st.pyplot(fig)

# Visualisasi berdasarkan musim
st.subheader("Performa Penyewa Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(7, 5))
sns.despine(fig)
sns.countplot(x='season', data=filtered_df, hue='season', palette='magma', legend=False)
plt.title("Jumlah Penyewa Sepeda per Musim", loc="center", fontsize=16)
st.pyplot(fig)

# Visualisasi berdasarkan holiday
st.subheader("Performa Penyewa Sepeda Berdasarkan Hari Libur")
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='holiday', data=filtered_df, hue='holiday', palette='coolwarm', legend=False)
plt.title("Jumlah Penyewa Sepeda pada Hari Libur", loc="center", fontsize=16)
st.pyplot(fig)

# Analisis jam penyewaan terbanyak
hourly_counts = filtered_df.groupby('hr')['cnt'].sum()
max_hour = hourly_counts.idxmax()
max_count = hourly_counts.max()

st.subheader("Jam Penyewaan Terbanyak")
st.write(f"Jam penyewaan terbanyak adalah pukul {max_hour} dengan jumlah {max_count} penyewaan.")

# Visualisasi jumlah penyewaan per jam
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(hourly_counts.index, hourly_counts)
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.title('Jumlah Penyewaan Sepeda per Jam')
plt.xticks(range(24))
plt.grid(True)
st.pyplot(fig)

# Visualisasi jumlah pengguna casual dan registered
st.subheader("Jumlah Pengguna Casual dan Registered")
casual_counts = filtered_df['casual'].sum()
registered_counts = filtered_df['registered'].sum()

plot_data = pd.DataFrame({'penyewa': ['casual', 'registered'], 'cnt': [casual_counts, registered_counts]})
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(x='penyewa', y='cnt', data=plot_data, palette='pastel')
plt.title("Jumlah Pengguna Sepeda Berdasarkan Tipe")
plt.ylabel("Jumlah Penyewa")
st.pyplot(fig)

# Analisis korelasi
data = filtered_df[['cnt', 'temp', 'atemp', 'hum', 'windspeed']]
correlation_matrix = data.corr()

st.subheader("Korelasi Antar Atribut")
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Heatmap Korelasi')
st.pyplot(plt)