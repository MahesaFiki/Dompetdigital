import streamlit as st
import json
import os
from datetime import datetime #add this

# File untuk menyimpan data transaksi
DATA_FILE = "transactions.json"

# Fungsi untuk memuat data dari file JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"balance": 0, "transactions": []}

# Fungsi untuk menyimpan data ke file JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Memuat data saat aplikasi dijalankan
data = load_data()

# Header aplikasi
st.title("Dompet Digital")
st.subheader("Kelola saldo dan riwayat transaksi Anda dengan mudah!")

# Tampilkan saldo saat ini
st.markdown(f"### Saldo Saat Ini: {data['balance']:,} IDR")

# Input untuk menambah atau menarik saldo
amount = st.number_input("Masukkan jumlah IDR:", min_value=1, step=1)

# Tombol untuk menambah saldo
if st.button("Tambah Saldo"):
    data["balance"] += amount
    data["transactions"].append({"type": "Tambah", "amount": amount, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) #add this
    save_data(data)
    st.success(f"Berhasil menambahkan {amount:,} IDR ke saldo Anda!")

# Tombol untuk menarik saldo
if st.button("Tarik Saldo"):
    if amount > data["balance"]:
        st.error("Saldo tidak mencukupi!")
    else:
        data["balance"] -= amount
        data["transactions"].append({"type": "Tarik", "amount": amount, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) #add this
        save_data(data)
        st.success(f"Berhasil menarik {amount:,} IDR dari saldo Anda!")

# Tampilkan riwayat transaksi
st.subheader("Riwayat Transaksi")
if data["transactions"]:
    for transaction in reversed(data["transactions"]):
        st.write(f"- [{transaction['date']}] {transaction['type']} - {transaction['amount']:,} IDR")
else:
    st.write("Belum ada transaksi.")
