import streamlit as st
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import base64
import io
from datetime import datetime

import uuid 


def app():
    # Cek apakah pengguna sudah login dan session_state untuk cart
    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # Jika pengguna sudah logout, tampilkan pesan untuk login
    if st.session_state.signout:
        
        def load_data():
            return pd.read_csv('sepatu.csv')

        df = load_data()

        if 'cart' not in st.session_state:
            st.session_state.cart = []

        st.markdown('<h3 style="font-size: 20px;">Halaman Pembayaran 💳</h3>', unsafe_allow_html=True)
        # Nama item
        selected_item = st.selectbox("Pilih Barang", df["nama"].tolist())

        # Ukuran yang tersedia
        available_sizes = df[df["nama"] == selected_item]["ukuran"].unique().tolist()
        selected_size = st.selectbox("Pilih Ukuran", available_sizes)

        # Stok yang tersedia
        available_stok = df[(df["nama"] == selected_item) & (df["ukuran"] == selected_size)]["stok"].iloc[0]
        st.info(f"Stok yang tersedia: {available_stok} pasang")

        # Input jumlah yang ingin dibeli
        jumlah = st.number_input("Masukkan jumlah yang ingin dibeli", min_value=1, step=1)

        # Harga
        harga_satuan = df[(df["nama"] == selected_item) & (df["ukuran"] == selected_size)]["harga"].iloc[0]
        total_harga = harga_satuan * jumlah

        # Menambahkan ke keranjang
        if st.button("Tambahkan ke Keranjang",use_container_width = True):

            if jumlah <= available_stok:
                item_exists = False
                for item in st.session_state.cart:
                    if selected_item == item['item'] and selected_size == item['ukuran']:
                        item_exists = True
                        break
                if item_exists:
                    st.error('Item yang anda tambahkan sudah ada di keranjang')
                else:
                    st.session_state.cart.append({
                        "item": selected_item,
                        "ukuran": selected_size,
                        "jumlah": jumlah,
                        "total_harga": total_harga
                    })
                    st.success(f'{selected_item} (Ukuran: {selected_size}) berhasil ditambahkan ke keranjang!')
            elif available_stok == 0:
                st.error('Stok tidak tersedia!')
            else:
                st.error('Jumlah melebihi stok yang tersedia!')

        if st.session_state.cart:
            st.subheader("Keranjang Belanja")
            item_to_delete = None  # Variabel untuk melacak item yang akan dihapus
            for i, item in enumerate(st.session_state.cart):
                try:
                    cols = st.columns([3, 1])
                    cols[0].write(f"- {item['item']} (Ukuran: {item['ukuran']}): {item['jumlah']} pcs, Total Harga: Rp{item['total_harga']}")
                    if cols[1].button("Hapus", key=f"hapus_{i}"):
                        item_to_delete = i  # Tandai item yang akan dihapus

                except KeyError as e:
                    st.error(f"KeyError: {e} tidak ditemukan dalam item.")

            # Proses penghapusan di luar loop
            if item_to_delete is not None:
                deleted_item = st.session_state.cart.pop(item_to_delete)
                st.success(f"{deleted_item['item']} (Ukuran: {deleted_item['ukuran']}) berhasil dihapus dari keranjang!")
                st.rerun()
        else:
            st.write("Keranjang belanja Anda kosong.")
            
        # Inisialisasi session state untuk melacak status konfirmasi
        if 'is_confirming' not in st.session_state:
            st.session_state.is_confirming = False
        
        # Function to calculate the total
        def calculate_total(cart):
            return sum(item["total_harga"] for item in cart)

        # Function to generate invoice

        def generate_invoice(cart, total,username,id_invoice,id_pelanggan):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)

            # Set font style for title
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(300, 760, "INVOICE")  # Title centered

            # Add company name below the title
            c.setFont("Helvetica", 12)
            c.drawCentredString(300, 740, "Harmon CORP")

            # Add company name below the title
            c.setFont("Helvetica", 8)
            c.drawCentredString(300, 730, "Jalan Sumbawa I/20, Kelurahan Merdeka, Kecamatan Sumurbandung, Surabaya 61257")
            
            # Add Jargon below company name
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(300, 710, "harmon corp, harmoni di setiap langkah")  # Replace with your company slogan

            # Draw a line below company name
            c.setStrokeColor(colors.grey)
            c.setLineWidth(0.5)
            c.line(50, 725, 550, 725)

            # Add current date and time
            current_datetime = datetime.now().strftime("%d %B %Y %H:%M")
            c.setFont("Helvetica", 10)
            c.drawRightString(550, 690, f"Date: {current_datetime}")  # Date and Time on the top-right corner

            c.setFont("Helvetica", 9)
            c.drawRightString(550, 680,f"Invoice ID: {id_invoice}") 
            c.drawRightString(550, 670,f"Customer ID: {id_pelanggan}") 
            c.drawRightString(550, 660,"Metode Pembayaran: Cash") 

            # Add cashier name beside the date, on the left side
            c.setFont("Helvetica", 10)
            c.drawString(50, 690, f"Kasir yang melayani: {username}") 
            

            # Invoice details header
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 630, "Deskripsi Item")
            c.drawString(300, 630, "Jumlah Item")
            c.drawString(400, 630, "Harga Satuan")
            c.drawString(500, 630, "Total Harga")
            
            y_position = 600
            for item in cart:
                c.setFont("Helvetica", 10)
                c.drawString(100, y_position, f"{item['item']} (Size: {item['ukuran']})")
                c.drawString(300, y_position, f"{item['jumlah']} pcs")
                c.drawString(400, y_position, f"Rp{item['total_harga'] / item['jumlah']:,.0f}")  # Unit Price
                c.drawString(500, y_position, f"Rp{item['total_harga']:,.0f}")  # Total Price
                y_position -= 20
            
            # Add the total amount at the bottom
            c.setFont("Helvetica-Bold", 12)
            c.drawString(375, y_position - 10, f"Total Keseluruhan:")
            c.drawString(500, y_position - 10, f"Rp{total:,.0f}")  # Total price

            # Footer with contact information
            c.setFont("Helvetica", 8)
            c.drawCentredString(300, 50, "Terima kasih telah berbelanja! Hubungi kami di: harmoncorporation@gmail.com")

            # Draw a line at the bottom
            c.setStrokeColor(colors.grey)
            c.setLineWidth(0.5)
            c.line(50, 50 - 10, 550, 50 - 10)

            c.save()
            buffer.seek(0)
            return buffer

        # Fungsi untuk menyimpan data ke Firestore
        def save_to_firestore(cart, username):
            db = st.session_state.db
            try:
                # Buat ID penjualan dan ID pelanggan dengan hanya mengambil 4-5 karakter pertama dari UUID
                id_penjualan = "PES" + str(uuid.uuid4().hex[:5]).upper()  # Mengambil 5 karakter pertama dari UUID
                id_pelanggan = "PEL" + str(uuid.uuid4().hex[:5]).upper()  # Mengambil 5 karakter pertama dari UUID

                # Ambil tanggal dan waktu saat ini
                now = datetime.now()
                tanggal = now.strftime("%Y-%m-%d")  # Format hanya tanggal
                waktu = now.strftime("%H:%M:%S")    # Format hanya waktu

                # Gabungkan item dan ukuran dalam satu tuple (item, ukuran)
                items_with_sizes = [{"item": item['item'], "ukuran": item['ukuran']} for item in cart]

                # Format data untuk Firestore
                data = {
                    "item_ukuran": items_with_sizes,  # Menyimpan tuple (item, ukuran)
                    "harga": [float(item['total_harga'] / item['jumlah']) for item in cart],  # Harga satuan
                    "jumlah": [int(item['jumlah']) for item in cart],
                    "id_penjualan": [id_penjualan],
                    "total_harga": [int(sum(item['total_harga'] for item in cart))],
                    "username": username,
                    "id_pelanggan": id_pelanggan,
                    "tanggal": tanggal,
                    "waktu": waktu
                }

                # Simpan data ke Firestore
                db.collection("Penjualan").document(id_penjualan).set(data)
                return id_penjualan, id_pelanggan
            except Exception as e:
                st.error(f"Gagal menyimpan data ke Firestore: {e}")
                return None, None

     


        # Fungsi untuk menampilkan tombol konfirmasi atau batal
        def show_confirmation_buttons():
            if st.session_state.is_confirming:
                # Menampilkan tombol Konfirmasi dan Batal setelah tombol konfirmasi ditekan
                col1, col2 = st.columns([5, 5])
                
                with col1:
                    if st.button("Konfirmasi", use_container_width=True):                        

                        #Menambahkan data penjualan ke firestore
                        cart = st.session_state.cart
                        username = st.session_state.username
                        id_invoice,id_pelanggan = save_to_firestore(cart, username)

                        # Generate invoice
                        total = calculate_total(cart)
                        pdf_buffer = generate_invoice(cart, total, username,id_invoice,id_pelanggan)
                        
                        # Simpan PDF ke session_state dalam format base64
                        pdf_file = io.BytesIO(pdf_buffer.getvalue())
                        pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode()
                        st.session_state.pdf_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="invoice.pdf">Click untuk mengunduh faktur pembelajaan</a>'

                        # Kosongkan keranjang belanja
                        st.session_state.cart = []
                        st.success("Pembelian berhasil diproses! Stok telah diperbarui.")
                        st.session_state.is_confirming = False  # Kembali ke satu tombol
                        st.rerun()

                with col2:
                    if st.button("Batal", use_container_width=True):
                        st.session_state.is_confirming = False
                        st.info("Pembelian dibatalkan.")
                        st.rerun()

            else:
                # Tombol tunggal untuk menampilkan tombol konfirmasi dan batal
                if st.button("Proses Pembelian", use_container_width=True):
                    st.session_state.is_confirming = True
                    st.warning("Apakah Anda yakin ingin melanjutkan pembelian?")
                    st.rerun()

            # Tampilkan link download invoice jika sudah ada
            if 'pdf_link' in st.session_state:
                st.markdown(st.session_state.pdf_link, unsafe_allow_html=True)


        # Panggil fungsi untuk menampilkan tombol
        show_confirmation_buttons()

    else:
        st.image("images/background_harmoncorps.png")
        st.text("Please log in to access this page.")


    
