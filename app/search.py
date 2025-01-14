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

        st.markdown('<h3 style="font-size: 20px;">Daftar Barang 👟</h3>', unsafe_allow_html=True)

        # Load data barang dari file CSV
        data = load_data()
        
        # Tampilkan daftar barang
        # st.subheader("Daftar Barang")
        st.dataframe(data)

        # Input untuk cek ketersediaan
        st.subheader("Cari Sepatu Anda 🔎")
        selected_name = st.selectbox("Pilih Nama Sepatu:", data['nama'].unique())
        selected_size = st.number_input("Masukkan Ukuran Sepatu:", min_value=36, max_value=45, step=1)

        # Tombol cek ketersediaan
        if st.button("Cek Ketersediaan",use_container_width=True):
            # Filter data sesuai input
            sepatu = data[(data['nama'] == selected_name) & (data['ukuran'] == selected_size)]
            
            if not sepatu.empty:
                stok = sepatu.iloc[0]['stok']
                harga = sepatu.iloc[0]['harga']

                if stok > 0:
                    st.success(f"Sepatu tersedia! Stok: {stok} pasang. Harga: Rp {harga:,}")
                else:
                    st.error("Sepatu tidak tersedia (stok habis).")
            else:
                st.error("Sepatu dengan ukuran tersebut tidak ditemukan.")
    else:
        
        st.image("images/background_harmoncorps.png")
        st.text("Please log in to access this page.")
