import streamlit as st
import pandas as pd

def app():
    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'signout' not in st.session_state:
        st.session_state.signout = False
    
    def load_data():
        return pd.read_csv('sepatu.csv')


    if st.session_state.signout:
        df = load_data()
        
        st.markdown('<h3 style="font-size: 20px;">Halaman Update Stok 🔄</h3>', unsafe_allow_html=True)
        choice = st.selectbox('Opsi', ['Stok yang sudah ada', 'Stok baru','Upload File (CSV)'])
        if choice == "Stok yang sudah ada":
            selected_item = st.selectbox("Pilih Barang", df["nama"].tolist())

            available_sizes = df[df["nama"] == selected_item]["ukuran"].unique().tolist()
            selected_size = st.selectbox("Pilih Ukuran", available_sizes)

            # Input jumlah yang ingin dibeli
            jumlah = st.number_input("Masukkan jumlah stok yang akan di tambahkan", min_value=1, step=1)
            if st.button("Tambahkan", use_container_width=True):
                # Menambahkan stok pada item yang dipilih
                df.loc[(df["nama"] == selected_item) & (df["ukuran"] == selected_size), "stok"] += jumlah
                
                # Mengelompokkan dan menjumlahkan stok berdasarkan nama dan ukuran
                df_grouped = df.groupby(["nama", "ukuran"], as_index=False).agg({
                    "stok": "sum",
                    "harga": "first"  # Ambil harga pertama
                })

                # Simpan data yang sudah diperbarui
                df_grouped.to_csv('sepatu.csv', index=False)

                st.success("Stok berhasil diperbarui!")

        elif choice == "Upload File (CSV)":
            st.info("Pastikan file yang diunggah memiliki format yang sesuai, yaitu dengan nama kolom yang mencakup nama, ukuran, stok, dan harga, di mana nama produk ditulis dengan huruf kapital seluruhnya.")
            
            # Upload file CSV
            data_baru = st.file_uploader("Upload a CSV", type=["csv"])
            if data_baru is not None:
                new_data = pd.read_csv(data_baru)
            
            if st.button("Tambahkan", use_container_width=True):
                # Ubah nama produk menjadi kapital seluruhnya
                new_data["nama"] = new_data["nama"].str.upper()
                
                # Gabungkan dengan data lama dan hindari duplikasi
                df_lama = pd.read_csv('sepatu.csv')
                df_lama["nama"] = df_lama["nama"].str.upper()  # Pastikan konsistensi kapitalisasi
                
                df = pd.concat([df_lama, new_data], ignore_index=True)
                
                # Mengelompokkan dan mengatur stok serta harga
                df_grouped = df.groupby(["nama", "ukuran"], as_index=False).agg({
                    "stok": "sum",
                    "harga": "last"  # Gunakan harga terbaru
                })

                # Simpan data yang sudah diperbarui
                df_grouped.to_csv('sepatu.csv', index=False)
                st.success("Stok data berhasil diperbarui ✨🌟")

        elif choice == "Stok baru":
            selected_item = st.text_input("Nama Barang")
            selected_size = st.number_input("Pilih Ukuran", step=1, max_value=49, min_value=16)

            jumlah = st.number_input("Masukkan jumlah stok yang akan ditambahkan", min_value=1, step=1)
            harga_input = st.text_input("Masukkan harga (hanya angka):", placeholder="Contoh: 1200000")

            if st.button("Tambahkan", use_container_width=True):
                try:
                    harga = int(harga_input)

                    new_item = pd.DataFrame({
                    "nama": [selected_item.upper()],  # Pastikan nama produk huruf kapital
                    "ukuran": [selected_size],
                    "stok": [jumlah],
                    "harga": [harga_input]  # Harga bisa diatur sesuai kebutuhan
                })

                    # Membaca DataFrame yang ada
                    df = pd.read_csv('sepatu.csv')

                    # Menggabungkan data lama dengan data baru
                    df = pd.concat([df, new_item], ignore_index=True)

                    # Mengelompokkan dan menjumlahkan stok berdasarkan nama dan ukuran
                    df_grouped = df.groupby(["nama", "ukuran"], as_index=False).agg({
                        "stok": "sum",
                        "harga": "first"  # Ambil harga pertama
                    })

                    # Simpan data yang sudah diperbarui
                    df_grouped.to_csv('sepatu.csv', index=False)

                    st.success("Stok baru berhasil ditambahkan!")

                except ValueError:
                    # Tampilkan error jika bukan integer
                    st.error("Input harga tidak memenuhi kriteria.")

                # Menambahkan stok untuk barang baru
                


    else:
        st.image("background_harmoncorps.png")
        st.text("Please log in to access this page.")
