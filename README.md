# Welcome to Harmon Corp System Interface repo - Sistem informasi penjualan toko fisik (halaman karyawan)
<p align="justify">Proyek ini bertujuan untuk merancang dan mengimplementasikan sistem informasi berbasis web untuk mendukung proses penjualan di toko fisik milik Harmon Corp, sebuah perusahaan penyedia alas kaki. Sistem ini dirancang untuk mempermudah pengelolaan transaksi, data produk, dan interaksi antara admin, karyawan, serta pelanggan.</p>

## Fitur Utama

1. **Pendaftara akun terverifikasi**  
   - tidak semua user dapat mendaftar pada interface ini, sehingga dapat meminimalisir kesalahan data yang ada pada database dengan oknum yang tidak diketahui. 
     
2. **Manajemen Produk**  
   - Tambah, ubah, dan hapus data produk oleh admin.
   - Menampilkan daftar produk yang tersedia untuk karyawan dan pelanggan.

3. **Transaksi Penjualan**  
   - Input data penjualan secara langsung oleh karyawan.
   - Cetak struk transaksi.

4. **Laporan Penjualan**  
   - User dapat melihat grafik penjualan secara realtime untuk kebutuhan laporan penjualan yang diberikan kepada manager secara lebih lanjut.

## Teknologi yang Digunakan
- **Python**: Bahasa pemrograman utama untuk logika backend.
- **Streamlit**: Framework untuk membangun aplikasi web dengan cepat.
- **Firebase, .csv file**: Database untuk menyimpan data produk, pengguna, dan transaksi.
- **HTML/CSS**: Untuk meningkatkan antarmuka pengguna.

## Arsitektur Sistem
Sistem ini dirancang berbasis web dengan dua faktor utama:
1. **Karyawan (User)**
   - Memasukkan data transaksi penjualan.
   - Memberikan layanan pembayaran kepada pelanggan di toko fisik.
   - Memantau grafik penjualan untuk dilakukanya pembuatan laporan lebih lanjut

2. **Pelanggan**
   - Melihat informasi produk yang tersedia di toko fisik.
   - Melakukan pembelian yang dilayani oleh karyawan.

## SDLC Model: Prototyping
Proyek ini dikembangkan menggunakan metode SDLC berbasis *prototyping*, dengan tahapan sebagai berikut:
1. **Analisis Kebutuhan**
   - Identifikasi kebutuhan pengguna dari sudut pandang admin, karyawan, dan pelanggan.

2. **Pembuatan Prototipe**
   - Pembuatan antarmuka dan fitur awal.

3. **Evaluasi Prototipe**
   - Mendapatkan masukan dari pengguna.
   - Revisi prototipe hingga sesuai dengan kebutuhan.

4. **Implementasi dan Pengujian**
   - Pengujian sistem oleh tim pengembang dan pengguna.

5. **Pemeliharaan**
   - Pemeliharaan sistem secara berkala untuk memastikan kinerja optimal.

## Cara Menjalankan Proyek
- Akses pada link tersebut "https://harmoncorpuser2024.streamlit.app/"
- Akses fitur karyawan dan login sebagai karyawan
- User/Pw: `kiculpengenkerja2@gmail.com`, `kiculpengenkerja123`
- jika ada yang ditanyakan kontak saya melalui email "dhaniaditya762@gmail.com"
