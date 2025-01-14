import streamlit as st
from streamlit_option_menu import option_menu

import dashboard, search, account, pay, update

st.set_page_config(
    page_title="Offline Store APP",
    page_icon="👟",
)

class homepage:
    def __init__(self):
        self.apps = []
    
    def add_app(self, title, function):
        self.apps.append({
            "tittle": title,
            "function": function,  
        })

    def run():
        # CSS untuk mengubah warna latar belakang aplikasi
        st.markdown("""
        <style>
        /* Mengubah warna latar belakang utama aplikasi */
        .stApp {
        background-color: #FFF0DC; /* Ganti dengan warna yang diinginkan */
        }
        div[data-baseweb="select"] > div {
        background-color: #FFE0B5; /* Warna latar belakang */
        color: black; /* Warna teks */
        border-radius: 5px; /* Sudut membulat */
        }
        div[data-baseweb="input"] > div {
        background-color: #FFE0B5; /* Warna latar belakang */
        color: black; /* Warna teks */
        border-radius: 5px; /* Sudut membulat */
        }
        .reportview-container {
        background-color: #f0f0f0;
        }
        .stSidebar{
        background-color: #FFF0DC; /* Ganti dengan warna yang diinginkan */
        }
        .stAppHeader{
        background-color: #FFF0DC; /* Ganti dengan warna yang diinginkan */
        }
        .icon bi-chat-text-fill{
        style-color : white; /* Ganti dengan warna yang diinginkan */
        }
        </style>
        """, unsafe_allow_html=True)

        with st.sidebar:
            # Menambahkan logo kecil di sidebar
            st.image("images/logo_harmoncorps.png")
            
            app = option_menu(
                menu_title="Select Menu",
                
                options=["Dashboard", "Pencarian", "Karyawan", "Pembayaran", "Update"],
                icons=["bar-chart", "search", "person-circle", "credit-card-fill", "clock-history"],
                menu_icon="chat-text-fill",
                styles={
                    "container": {"padding": "5!important", "background-color": "#FFE0B5"},
                    "icon": {"color": "black", "font-size": "23px"},
                    "nav-link": {"color": "black", "font-size": "20px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#B59F78"}
                }
            )

        if app == 'Dashboard':
            dashboard.app()

        if app == 'Pencarian':
            search.app()
        
        if app == 'Karyawan':
            account.app()

        if app == 'Pembayaran':
            pay.app()

        if app == 'Update':
            update.app()

    run()
