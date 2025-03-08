import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
files = [
    "PRSA_Data_Aotizhongxin_20130301-20170228.csv",
    "PRSA_Data_Changping_20130301-20170228.csv",
    "PRSA_Data_Dingling_20130301-20170228.csv",
    "PRSA_Data_Dongsi_20130301-20170228.csv",
    "PRSA_Data_Guanyuan_20130301-20170228.csv"
]

locations = ["Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan"]



# Load and preprocess datasets

dfs = {}

for loc, file in zip(locations, files):

    try:

        df = pd.read_csv(file)

        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

        df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

        df.set_index('date', inplace=True)

        

        # Ensure numeric data types

        for col in ['PM2.5', 'TEMP', 'HUMI', 'WSPM']:

            if col in df.columns:

                df[col] = pd.to_numeric(df[col], errors='coerce')

        

        # Drop missing values in existing key columns

        existing_cols = [col for col in ['PM2.5', 'TEMP', 'HUMI', 'WSPM'] if col in df.columns]

        df.dropna(subset=existing_cols, inplace=True)

        

        dfs[loc] = df

    except Exception as e:

        st.error(f"Error loading {loc}: {e}")


# Set title for the dashboard

st.title("Dashboard Analisis Kualitas Udara")

st.subheader("Analisis Data Kualitas Udara Berdasarkan Faktor Cuaca dan Waktu")


# Sidebar

with st.sidebar:

    st.header("📊 Menu Sidebar")

    

    # Pilih lokasi

    st.subheader("📍 Pilih Lokasi")

    selected_location = st.selectbox("Lokasi", locations)

    

    # Tampilkan informasi dataset

    st.subheader("📂 Informasi Dataset")

    st.write(f"Dataset yang dipilih: **{selected_location}**")

    st.write(f"Jumlah baris data: **{len(dfs[selected_location])}**")

    

    # Filter berdasarkan tanggal

    st.subheader("📅 Filter Tanggal")

    min_date = dfs[selected_location].index.min()

    max_date = dfs[selected_location].index.max()

    start_date = st.date_input("Tanggal Mulai", min_date)

    end_date = st.date_input("Tanggal Selesai", max_date)

    

    # Filter data berdasarkan tanggal yang dipilih

    filtered_df = dfs[selected_location].loc[start_date:end_date]

    

    # Informasi Kontak

    st.subheader("📞 Informasi Kontak")

    st.write("Nama: **Yuda Reyvandra Herman**")

    st.write("Email: **reyvandrayuda@gmail.com**")

    st.write("ID Dicoding: **MC189D5Y0450**")


# Create tabs for different sections

tab1, tab2, tab3 = st.tabs(["📈 Analisis Polusi Udara", "📊 Pola Polusi Udara", "📝 Kesimpulan"])


# Tab 1: Analisis Polusi Udara

with tab1:

    st.header("📈 Analisis Polusi Udara")

    

    st.subheader(f"Data untuk {selected_location}")

    st.write(filtered_df.head())

    

    available_columns = filtered_df.columns.tolist()

    

    # Scatter plots

    scatter_plots = [

        ('TEMP', 'PM2.5', 'Hubungan Suhu terhadap PM2.5'),

        ('HUMI', 'PM2.5', 'Hubungan Kelembaban terhadap PM2.5'),

        ('WSPM', 'PM2.5', 'Hubungan Kecepatan Angin terhadap PM2.5')

    ]

    

    for x_col, y_col, title in scatter_plots:

        if {x_col, y_col}.issubset(available_columns):

            fig, ax = plt.subplots()

            sns.scatterplot(data=filtered_df, x=x_col, y=y_col, ax=ax)

            ax.set_title(f'{title} - {selected_location}')

            st.pyplot(fig)

    

    # Heatmap korelasi

    required_columns = {'TEMP', 'HUMI', 'WSPM', 'PM2.5'}

    if required_columns.issubset(set(available_columns)):

        fig, ax = plt.subplots()

        sns.heatmap(filtered_df[list(required_columns)].corr(), annot=True, cmap='coolwarm', ax=ax)

        ax.set_title(f'Korelasi Faktor Cuaca terhadap PM2.5 - {selected_location}')

        st.pyplot(fig)


# Tab 2: Pola Polusi Udara

with tab2:

    st.header("📊 Pola Polusi Udara")

    

    # Line plot tren PM2.5

    st.subheader("Tren Polusi PM2.5")
 
    plt.figure(figsize=(12, 6))

    if 'PM2.5' in filtered_df.columns:

        filtered_df['PM2.5'].resample('M').mean().plot(label=selected_location)

    

    plt.title('Tren Bulanan PM2.5')

    plt.xlabel('Tanggal')

    plt.ylabel('Rata-rata PM2.5')

    plt.legend()

    st.pyplot(plt)


# Tab 3: Kesimpulan

with tab3:

    st.header("📝 Kesimpulan")

    st.write("Analisis ini menunjukkan hubungan antara faktor cuaca dan kualitas udara berdasarkan data PM2.5. "

             "Dari visualisasi yang ditampilkan, kita dapat melihat tren dan pola yang ada dalam data. "

             "Kualitas udara dapat dipengaruhi oleh suhu, kelembaban, dan kecepatan angin. "

             "Penting untuk terus memantau data ini untuk memahami dampak lingkungan dan kesehatan masyarakat.")