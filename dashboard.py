import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Dashboard Histogram Polutan")

# Memuat data dari file CSV
@st.cache_data
def load_data():
    # Gantilah dengan path ke file main-data.csv Anda
    data = pd.read_csv("main-data.csv")
    return data

data = load_data()

# Memastikan kolom yang relevan ada
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']  # Gantilah dengan nama kolom yang sesuai di data Anda

# Memilih polutan untuk analisis
selected_pollutant = st.selectbox("Pilih Polutan untuk Histogram", pollutants)

# Membuat histogram
st.subheader(f'Histogram {selected_pollutant}')
fig, ax = plt.subplots()
ax.hist(data[selected_pollutant].dropna(), bins=30, color='blue', alpha=0.7)
ax.set_title(f'Distribusi {selected_pollutant}')
ax.set_xlabel(f'{selected_pollutant} (µg/m³)')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Judul Dashboard
st.title("Dashboard Kualitas Udara Berdasarkan Daerah")

# Memastikan kolom yang relevan ada
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']  # Gantilah dengan nama kolom yang sesuai di data Anda
area_column = 'station'  # Gantilah dengan nama kolom yang sesuai di data Anda

# Memilih daerah untuk analisis
if area_column in data.columns:
    areas = data[area_column].unique()
    selected_area = st.selectbox("Pilih Daerah", areas)

    # Memilih polutan untuk analisis
    selected_pollutant = st.selectbox("Pilih Polutan untuk Kategori", pollutants)

    # Menampilkan kategori kualitas udara
    st.subheader("Kategori Kualitas Udara untuk Daerah: " + selected_area)

    # Filter data berdasarkan daerah yang dipilih
    filtered_data = data[data[area_column] == selected_area]

    def categorize_pollutant(value, pollutant):
        if pollutant == 'PM2.5':
            if value < 35:
                return 'Baik'
            elif value < 75:
                return 'Sedang'
            elif value < 150:
                return 'Buruk'
            else:
                return 'Sangat Buruk'
        elif pollutant == 'CO':
            if value < 4:
                return 'Baik'
            elif value < 9:
                return 'Sedang'
            elif value < 12:
                return 'Buruk'
            else:
                return 'Sangat Buruk'
        return 'Tidak Diketahui'

    # Mengkategorikan polutan yang dipilih
    filtered_data[f'{selected_pollutant} Category'] = filtered_data[selected_pollutant].apply(lambda x: categorize_pollutant(x, selected_pollutant))
    
    # Menampilkan tabel dengan nama daerah dan kategori
    st.write(filtered_data[[area_column, selected_pollutant, f'{selected_pollutant} Category']])
else:
    st.error(f"Data tidak memiliki kolom '{area_column}'.")