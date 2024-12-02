import streamlit as st
import json
import os
from datetime import datetime

# File untuk menyimpan data pengguna dan transaksi
USERS_FILE = "users.json"

# Fungsi untuk memuat data pengguna
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

# Fungsi untuk menyimpan data pengguna
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# Memuat data pengguna
users = load_users()

# Fungsi untuk login
def login(user_id, password):
    if user_id in users and users[user_id]["password"] == password:
        return True
    return False

# Fungsi untuk memuat data pengguna tertentu
def load_user_data(user_id):
    return users.get(user_id, {"balance": 0, "transactions": []})

# Fungsi untuk menyimpan data pengguna tertentu
def save_user_data(user_id, data):
    users[user_id] = data
    save_users(users)

# Inisialisasi Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_data = {}

# Halaman Login
if not st.session_state.logged_in:
    st.title("Dompet Digital - Login")
    user_id = st.text_input("Masukkan ID Pengguna:")
    password = st.text_input("Masukkan Password:", type="password")

    if st.button("Login"):
        if login(user_id, password):
            st.success("Login berhasil!")
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.user_data = load_user_data(user_id)
            st.experimental_rerun()  # Reload halaman untuk masuk ke halaman utama
        else:
            st.error("ID atau Password salah!")

    # Tombol untuk membuat akun baru jika belum punya akun
    st.subheader("Belum punya akun? Daftar sekarang!")
    new_user_id = st.text_input("Buat ID Pengguna:")
    new_password = st.text_input("Buat Password:", type="password")
    
    if st.button("Daftar"):
        if new_user_id in users:
            st.error("ID Pengguna sudah terdaftar!")
        else:
            users[new_user_id] = {"password": new_password, "balance": 0, "transactions": []}
            save_users(users)
            st.success("Pendaftaran berhasil! Silakan login.")

# Halaman Utama setelah Login
if st.session_state.logged_in:
    st.title("Dompet Digital")
    st.subheader(f"Selamat datang, {st.session_state.user_id}!")
    
    # Data pengguna
    user_data = st.session_state.user_data

    # Tampilkan saldo saat ini
    st.markdown(f"### Saldo Saat Ini: {user_data['balance']:,} IDR")
    
    # Input untuk menambah atau menarik saldo
    amount = st.number_input("Masukkan jumlah IDR:", min_value=1, step=1)

    # Tombol untuk menambah saldo
    if st.button("Tambah Saldo"):
        user_data["balance"] += amount
        user_data["transactions"].append({
            "type": "Tambah", 
            "amount": amount, 
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_user_data(st.session_state.user_id, user_data)
        st.success(f"Berhasil menambahkan {amount:,} IDR ke saldo Anda!")

    # Tombol untuk menarik saldo
    if st.button("Tarik Saldo"):
        if amount > user_data["balance"]:
            st.error("Saldo tidak mencukupi!")
        else:
            user_data["balance"] -= amount
            user_data["transactions"].append({
                "type": "Tarik", 
                "amount": amount, 
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_user_data(st.session_state.user_id, user_data)
            st.success(f"Berhasil menarik {amount:,} IDR dari saldo Anda!")

    # Tampilkan riwayat transaksi
    st.subheader("Riwayat Transaksi")
    if user_data["transactions"]:
        for transaction in reversed(user_data["transactions"]):
            st.write(f"- [{transaction['date']}] {transaction['type']} - {transaction['amount']:,} IDR")
    else:
        st.write("Belum ada transaksi.")

    # Tombol logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_data = {}
        st.success("Logout berhasil!")
        st.experimental_rerun()  # Reload halaman untuk kembali ke login
