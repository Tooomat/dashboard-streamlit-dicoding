import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
import streamlit as st
import os
sb.set(style='dark')

def count_bycycle_byweater(csv):
    byweathersit_df = csv.groupby(by="weathersit").cnt.nunique().reset_index()
    byweathersit_df.rename(columns={
        "cnt": "jumlah_sepeda_yang_disewa"
    }, inplace=True)
    return byweathersit_df

def create_count_year(csv, fist, last):
    monthly_order_df = csv.resample(rule='M', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    hour_df_year = monthly_order_df[(monthly_order_df.index >= fist) & (monthly_order_df.index < last)]
    hour_df_year.index = hour_df_year.index.strftime('%B')

    hour_df_year = hour_df_year.reset_index()
    hour_df_year.rename(columns={
        "instant": "order",
        "cnt": "count"
    }, inplace=True)
    return hour_df_year

try:
    hour_csv_path = os.path.abspath("dashboard/day-1.csv")
    day_csv_path = os.path.abspath("dashboard/hour-1.csv")
    hour_df = pd.read_csv(hour_csv_path)
    day_df = pd.read_csv(day_csv_path)
except FileNotFoundError:
    st.error("File not found. Please check the file path.")

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
count_day_2011_df = create_count_year(day_df, '2011-01-01', '2012-01-01')
count_hour_2011_df = create_count_year(hour_df, '2011-01-01', '2012-01-01')

count_day_2012_df = create_count_year(day_df, '2012-01-01', '2013-01-01')
count_hour_2012_df = create_count_year(hour_df, '2012-01-01', '2013-01-01')

bycycle_byweater_hour = count_bycycle_byweater(hour_df)
bycycle_byweater_day = count_bycycle_byweater(day_df)

st.header("Bike Sharing Dataset :bike:")
st.subheader("Total Orders")
col1, col2 = st.columns(2)
# --> tahun 2011
with col1:
    total_order_2011 = count_day_2011_df["count"].sum()
    st.metric("tahun 2011", value=str(total_order_2011) + "/h")

with col2:
    total_order_2011_hour = count_hour_2011_df["count"].sum()
    st.metric("", value=str(total_order_2011_hour) + "/d")

# --> grafik
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    count_day_2011_df["dteday"],
    count_day_2011_df["count"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Number of orders Month (2011)")
ax.set_xlabel(None)
ax.set_ylabel("Number of bikes rented")
st.pyplot(fig)
with st.expander("# Conclusion-1"):
    st.write("Berdasarkan data yang diamati, terdapat tren peningkatan penggunaan sepeda dari bulan Januari hingga Juni, diikuti oleh penurunan yang signifikan dari bulan Juni hingga Desember pada tahun 2011. Penurunan ini dapat disebabkan oleh faktor-faktor musiman, seperti perubahan cuaca, liburan, atau peristiwa khusus yang terjadi pada periode tersebut. Hal ini menunjukkan perlunya strategi pemasaran dan penyesuaian layanan untuk mengimbangi fluktuasi permintaan yang terjadi sepanjang tahun.")


#  --> tahun 2012
col1a, col2b = st.columns(2)
with col1a:
    total_order_2012 = count_day_2012_df["count"].sum()
    st.metric(label="tahun 2012", value=str(total_order_2012) + "/h")
with col2b:
    total_order_2012 = count_hour_2012_df["count"].sum()
    st.metric(label="", value=str(total_order_2012) + "/d")

# --> grafik
fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(
    count_hour_2012_df["dteday"],
    count_hour_2012_df["count"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
plt.title("Number of orders per Month (2011)")
plt.xlabel(None)
plt.ylabel("Jumlah sepeda yang tersewa")
st.pyplot(fig)
with st.expander("# Conclusion-2"):
    st.write("Berdasarkan data yang diamati, terdapat tren peningkatan penggunaan sepeda dari bulan Januari hingga September, diikuti oleh penurunan yang signifikan dari bulan september hingga Desember pada tahun 2012. Hal ini menunjukkan perlunya strategi pemasaran dan penyesuaian layanan untuk mengimbangi fluktuasi permintaan yang terjadi sepanjang tahun.")

# --> colom grafik (2011-2012)
st.subheader("Weathersit Demographics (2011-2012)")
colg1, colg2 = st.columns(2)
with colg1:
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(10,5))
    sb.barplot(
        y="jumlah_sepeda_yang_disewa",
        x="weathersit",
        data=bycycle_byweater_hour.sort_values(by="jumlah_sepeda_yang_disewa", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of weathersit on hours by jumlah sepeda", loc="center", fontsize=15)
    ax.set_xlabel("cuaca")
    ax.set_ylabel("banyak sepeda yang disewa")
    st.pyplot(fig)
with colg2:
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    fig, ax = plt.subplots(figsize=(10,5))
    sb.barplot(
        y="jumlah_sepeda_yang_disewa",
        x="weathersit",
        data=bycycle_byweater_day.sort_values(by="jumlah_sepeda_yang_disewa", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of weathersit on day by jumlah sepeda", loc="center", fontsize=15)
    ax.set_xlabel("cuaca")
    ax.set_ylabel("banyak sepeda yang disewa")
    st.pyplot(fig)

with st.expander("## Conclusion-weathersit"):
    st.write("jadi, cuaca sangat mempengaruhi customer untuk menyewa sepeda, dibuktikan pada tabel diatas cuaca yang bernilai 1 atau cuaca  bagus memiliki nilai yang paling tinggi")
