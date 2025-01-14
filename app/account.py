import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Inisialisasi Firebase hanya sekali
if not firebase_admin._apps:
    cred = credentials.Certificate("rpl-edudoexam-58276d3f3b2b.json")
    firebase_admin.initialize_app(cred)

# Simpan Firestore DB ke dalam st.session_state jika belum ada
if 'db' not in st.session_state:
    st.session_state.db = firestore.client()

def app():
    # Inisialisasi session state untuk user data
    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    if 'signout' not in st.session_state:
        st.session_state.signout = False  # Awal status signout = False

    
    def send_verification_link_to_admin(email):
        try:
            # Siapkan detail email admin
            system_email = "harmoncorp2024@gmail.com"  
            admin_email = "dhaniaditya762@gmail.com"
            admin_app_password = "xhsy ubgs xpgu sxjx"  # Ganti dengan App Password yang sudah dibuat
            subject = "User Registration Verification"
            body = f"A new user has registered with the email {email}. Please verify the email address using the following link:\n\n"

            # Generate email verification link menggunakan Firebase Admin SDK
            verification_link = "https://harmoncorpmanager2024.streamlit.app/"
            body += verification_link

            # Siapkan MIME email
            message = MIMEMultipart()
            message['From'] = system_email
            message['To'] = admin_email
            message['Subject'] = subject

            # Lampirkan body email
            message.attach(MIMEText(body, 'plain'))

            # Kirim email menggunakan SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(system_email, admin_app_password)  # Gunakan App Password di sini
                server.sendmail(admin_email, admin_email, message.as_string())
                st.success("Verification link sent to admin.")
        
        except Exception as e:
            st.error(f"Error sending verification email: {e}")

    def save_login_logout(username, event_type):
        """Simpan data login atau logout ke Firestore dengan menambahkan tanggal dan waktu tanpa menghapus nilai yang sama."""
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")  # Hanya tanggal
        time = now.strftime("%H:%M:%S")  # Hanya waktu
        db = st.session_state.db
        doc_ref = db.collection("Absensi Karyawan").document(username)

        try:
            # Ambil dokumen yang ada
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()

                # Tambahkan data baru secara manual
                if event_type == "login":
                    login_dates = data.get("Login_Date", [])
                    login_times = data.get("Login_Time", [])
                    login_dates.append(date)
                    login_times.append(time)
                    doc_ref.update({
                        "Login_Date": login_dates,
                        "Login_Time": login_times
                    })
                elif event_type == "logout":
                    logout_dates = data.get("Logout_Date", [])
                    logout_times = data.get("Logout_Time", [])
                    logout_dates.append(date)
                    logout_times.append(time)
                    doc_ref.update({
                        "Logout_Date": logout_dates,
                        "Logout_Time": logout_times
                    })
            else:
                # Buat dokumen baru jika belum ada
                if event_type == "login":
                    doc_ref.set({
                        "Login_Date": [date],
                        "Login_Time": [time],
                        "Logout_Date": [],
                        "Logout_Time": []
                    })
                elif event_type == "logout":
                    doc_ref.set({
                        "Login_Date": [],
                        "Login_Time": [],
                        "Logout_Date": [date],
                        "Logout_Time": [time]
                    })

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def login():
        try:
            db = st.session_state.db  # Akses Firestore dari session_state
            user = auth.get_user_by_email(email)
            
            # Cek apakah email sudah terverifikasi
            if not user.email_verified:
                st.warning("Your email is not verified by admin. Please contact admin for verification.")

            else:
            # Login berhasil
                st.session_state.username = user.uid
                st.session_state.useremail = user.email
                st.session_state.signout = True
                save_login_logout(user.uid, "login")  # Simpan data login
        except Exception as e:
            st.warning(f"Login Failed: {e}")

    def logout():
        save_login_logout(st.session_state.username, "logout")  # Simpan data logout
        st.session_state.signout = False
        st.session_state.username = ''
        st.session_state.useremail = ''

    def calculate_age(dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    if not st.session_state.signout:
        # Jika belum login
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        if choice == "Login":
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")

            st.button("Login", on_click=login, use_container_width=True)
        else:
            username = st.text_input("Nama Sesuai KTP")
            email = st.text_input("Alamat Email")
            password = st.text_input("Password", type="password")
            address = st.text_input("Alamat")
            birth = st.text_input("Tempat lahir")
            dob = st.date_input("Tanggal lahir")
            experience = st.text_area("Pengalaman kerja (tambahkan url pendukung jika ada)", placeholder="Describe your work experience here...")

            # Menghitung umur
            age = calculate_age(dob)

            # Konversi dob menjadi string dalam format dd-mm-yyyy
            dob_str = dob.strftime("%d-%m-%Y")

            if st.button("Create my account",use_container_width=True):
                try:
                    db = st.session_state.db  # Akses Firestore dari session_state
                    # Membuat pengguna baru menggunakan Firebase Authentication
                    user = auth.create_user(email=email, password=password, uid=username)
                    
                    # Menyimpan data tambahan ke Firestore
                    user_ref = db.collection("Absensi Karyawan").document(username)
                    user_ref.set({
                        "alamat_email": email,
                        "alamat": address,
                        "tempat_lahir" : birth,
                        "teanggal_lahir": dob_str,  # Simpan sebagai string
                        "umur": age,
                        "status": "Belum terverifikasi",  # Status email akan diatur menjadi belum terverifikasi
                        "work_experience": experience if experience else "-"  # Simpan pengalaman kerja jika ada
                    })
                    
                    send_verification_link_to_admin(email)
                    st.success("Account created successfully!")
                    st.markdown("Please Login using your email and password")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error creating account: {e}")
    else:
        # Jika sudah login
        st.text(f'Hello, {st.session_state.username} Selamat bekerja!')
        st.text('Name: ' + st.session_state.username)
        st.text('Email: ' + st.session_state.useremail)
        st.button('Sign Out', on_click=logout)
