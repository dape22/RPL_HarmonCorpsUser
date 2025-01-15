import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Pemetaan bulan Indonesia ke bulan Inggris
bulan_inggris = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

def app():
    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'signout' not in st.session_state:
        st.session_state.signout = False
    
    def get_data():       
        docs = db.collection("Penjualan").stream()
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            item_ukuran = []
            for item in doc_data.get("item_ukuran", []):
                item_ukuran.append(f"{item['item']} (Ukuran: {item['ukuran']})")
            
            tanggal_str = doc_data.get("tanggal")
            try:
                # Mengonversi tanggal dengan format '%Y-%m-%d'
                tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d")
                bulan = tanggal.month - 1
                bulan_format = bulan_indonesia[bulan]
                tanggal_format = tanggal.strftime(f"%d {bulan_format} %Y")
            except ValueError:
                tanggal_format = tanggal_str
            
            record = {
                "id_pelanggan": doc_data.get("id_pelanggan"),
                "id_invoice": ', '.join(doc_data.get("id_penjualan", [])),
                "tanggal": tanggal_format,
                "total_harga": ', '.join(map(str, doc_data.get("total_harga", []))),
                "nama_kasir": doc_data.get("username"),
                "waktu": doc_data.get("waktu"),
                "item_ukuran": item_ukuran,
            }

            data.append(record)
        
        df = pd.DataFrame(data)
        return df

    if st.session_state.signout:
        db = st.session_state.db
        input_hari_salah = False
        st.markdown('<h3 style="font-size: 20px;">Dashboard penjualan 📊</h3>', unsafe_allow_html=True)
        df = get_data()

        if df.empty:
            st.error("Tidak ada data yang tersedia di Firestore!")
        else:
            choice = st.selectbox("Opsi", ["Opsi 1", "Opsi 2"], label_visibility="collapsed", index=0)

            if choice == "Opsi 1":
                bulan = st.selectbox("Pilih Bulan", ["All"] + bulan_indonesia)
                tahun = st.selectbox("Pilih Tahun", ["All"] + [str(i) for i in range(2020, 2026)])
                hari = st.text_input("Masukkan Hari (Tanggal)", "")

                if bulan != "All":
                    df = df[df["tanggal"].str.contains(bulan)]
                if tahun != "All":
                    df = df[df["tanggal"].str.endswith(tahun)]
                if hari:
                    try:
                        hari = int(hari)
                        hari_to_string = str(hari).zfill(2)
                        df = df[df["tanggal"].str.startswith(hari_to_string)]
                    except ValueError:
                        input_hari_salah = True

                if input_hari_salah:
                    input_hari_salah = False
                    st.error("Input hari tidak valid, pastikan input berupa angka!")
                elif df.empty:
                    st.error("Tidak ada data yang cocok dengan filter yang Anda pilih!")
                else:
                    # Konversi kolom tanggal ke datetime
                    df["tanggal"] = pd.to_datetime(df["tanggal"], format='%d %B %Y')

                    # Konversi kolom total_harga ke numerik
                    df["total_harga"] = pd.to_numeric(df["total_harga"].str.replace(",", ""), errors="coerce")

                    # Hitung total harga
                    total_harga = df.groupby('tanggal')['total_harga'].sum()

                    # Hitung jumlah barang terjual dari kolom 'item_ukuran'
                    df['total_barang'] = df['item_ukuran'].apply(lambda x: len(x))

                    # Hitung total barang terjual per tanggal
                    total_barang = df.groupby('tanggal')['total_barang'].sum()

                    # Hitung jumlah pesanan berdasarkan kasir
                    kasir_count = df['nama_kasir'].value_counts()

                    # Menggabungkan semua item yang terjual tanpa ukuran
                    item_list = [item.split(" (")[0] for sublist in df['item_ukuran'] for item in sublist]
                    item_count = pd.Series(item_list).value_counts()

                    # Gunakan dua kolom untuk menampilkan grafik batang berdampingan
                    col1, col2 = st.columns(2)

                    with col1:
                        # Urutkan total harga secara descending
                        st.markdown(f"**Total Pemasukan :** Rp {total_harga.sum():,.0f}")
                        total_harga_sorted = total_harga.sort_values(ascending=False)
                        st.bar_chart(total_harga_sorted)

                        # Membuat Pie Chart menggunakan matplotlib
                        fig, ax = plt.subplots()
                        ax.pie(kasir_count, labels=kasir_count.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                        ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

                        # Tampilkan Pie Chart di bawah grafik batang
                        st.markdown(f"**Pelayanan Pegawai**")
                        st.pyplot(fig)

                    with col2:
                        # Urutkan total barang terjual secara descending
                        st.markdown(f"**Total Barang Terjual :** {total_barang.sum()}")
                        total_barang_sorted = total_barang.sort_values(ascending=False)
                        st.bar_chart(total_barang_sorted)

                        # Bar Chart untuk item yang terjual, diurutkan
                        st.markdown(f"**Distribusi Item Terjual**")
                        item_count_sorted = item_count.sort_values(ascending=False)
                        st.bar_chart(item_count_sorted)

                    # Tampilkan DataFrame dan dua diagram batang dalam kolom
                    with st.expander('See DataFrame (Selected time frame)'):
                        st.dataframe(df)

            else:
                # Konversi tanggal
                tanggal = pd.to_datetime(df['tanggal'], format='%d %B %Y')
                tanggal_awal = tanggal.min()
                tanggal_akhir = tanggal.max()

                # Input date
                min_date = tanggal_awal.strftime('%Y-%m-%d')
                max_date = tanggal_akhir.strftime('%Y-%m-%d')
                start_date = st.date_input("Start date", min_value=min_date, max_value=max_date)
                end_date = st.date_input("End date", min_value=min_date, max_value=max_date)

                # Info widget
                tanggal_awal1 = tanggal_awal.strftime('%d %B %Y')
                tanggal_akhir1 = tanggal_akhir.strftime('%d %B %Y')
                st.info(f"Menampilkan kurun waktu: {tanggal_awal1} hingga: {tanggal_akhir1}")

                if start_date and end_date:
                    # Konversi start_date dan end_date ke tipe datetime
                    start_date = pd.to_datetime(start_date)
                    end_date = pd.to_datetime(end_date)

                    # Filter data berdasarkan rentang tanggal
                    mask = (tanggal >= start_date) & (tanggal <= end_date)
                    df = df[mask]

                    if df.empty:
                        st.error("Tidak ada data dalam rentang tanggal yang dipilih.")
                    else:
                        # Konversi kolom total_harga ke numerik
                        df["total_harga"] = pd.to_numeric(df["total_harga"].str.replace(",", ""), errors="coerce")

                        # Hitung total harga per hari
                        total_harga = df.groupby('tanggal')['total_harga'].sum()

                        # Hitung jumlah barang terjual dari kolom 'item_ukuran'
                        df['total_barang'] = df['item_ukuran'].apply(lambda x: len(x))

                        # Hitung total barang terjual per tanggal
                        total_barang = df.groupby('tanggal')['total_barang'].sum()

                        # Hitung jumlah pesanan berdasarkan kasir
                        kasir_count = df['nama_kasir'].value_counts()

                        # Menggabungkan semua item yang terjual tanpa ukuran
                        item_list = [item.split(" (")[0] for sublist in df['item_ukuran'] for item in sublist]
                        item_count = pd.Series(item_list).value_counts()

                        # Gunakan dua kolom untuk menampilkan grafik batang berdampingan
                        col1, col2 = st.columns(2)

                        with col1:
                            # Urutkan total harga secara descending
                            st.markdown(f"**Total Pemasukan :** Rp {total_harga.sum():,.0f}")
                            total_harga_sorted = total_harga.sort_values(ascending=False)
                            st.bar_chart(total_harga_sorted)

                            # Membuat Pie Chart menggunakan matplotlib
                            fig, ax = plt.subplots()
                            ax.pie(kasir_count, labels=kasir_count.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                            ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

                            # Tampilkan Pie Chart di bawah grafik batang
                            st.markdown(f"**Pelayanan Pegawai**")
                            st.pyplot(fig)

                        with col2:
                            # Urutkan total barang terjual secara descending
                            st.markdown(f"**Total Barang Terjual :** {total_barang.sum()}")
                            total_barang_sorted = total_barang.sort_values(ascending=False)
                            st.bar_chart(total_barang_sorted)

                            # Bar Chart untuk item yang terjual, diurutkan
                            st.markdown(f"**Distribusi Item Terjual**")
                            item_count_sorted = item_count.sort_values(ascending=False)
                            st.bar_chart(item_count_sorted)

                        # Tampilkan informasi tanggal yang dipilih
                        start_date_str = start_date.strftime('%d %B %Y')
                        end_date_str = end_date.strftime('%d %B %Y')
                        st.info(f"Menampilkan kurun waktu: {start_date_str} hingga: {end_date_str}")

                        # Tampilkan DataFrame dan dua diagram batang dalam kolom
                        with st.expander('See DataFrame (Selected time frame)'):
                            st.dataframe(df)
