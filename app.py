import streamlit as st
import pandas as pd
import os

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Sistem Nilai Mahasiswa", layout="wide")

DATA_FILE = "data_mahasiswa.csv"

# ========================
# LOAD DATA
# ========================
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["NIM", "Nama", "Tugas", "UTS", "UAS", "Nilai Akhir", "Grade", "Keterangan"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ========================
# HITUNG NILAI
# ========================
def hitung_nilai(tugas, uts, uas):
    nilai_akhir = (0.3 * tugas) + (0.3 * uts) + (0.4 * uas)

    if nilai_akhir >= 85:
        grade = "A"
        ket = "Lulus (Sangat Baik)"
    elif nilai_akhir >= 75:
        grade = "B"
        ket = "Lulus (Baik)"
    elif nilai_akhir >= 65:
        grade = "C"
        ket = "Lulus (Cukup)"
    elif nilai_akhir >= 50:
        grade = "D"
        ket = "Tidak Lulus"
    else:
        grade = "E"
        ket = "Tidak Lulus"

    return round(nilai_akhir, 2), grade, ket

# ========================
# LOGIN SEDERHANA
# ========================
def login():
    st.title("🔐 Login Sistem")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state["login"] = True
            st.success("Login berhasil!")
        else:
            st.error("Username / Password salah!")

# ========================
# CRUD
# ========================
def tambah_data(df):
    st.subheader("➕ Tambah Data")

    with st.form("form_tambah"):
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        tugas = st.number_input("Nilai Tugas", 0, 100)
        uts = st.number_input("Nilai UTS", 0, 100)
        uas = st.number_input("Nilai UAS", 0, 100)

        submit = st.form_submit_button("Simpan")

        if submit:
            nilai_akhir, grade, ket = hitung_nilai(tugas, uts, uas)

            data_baru = pd.DataFrame([{
                "NIM": nim,
                "Nama": nama,
                "Tugas": tugas,
                "UTS": uts,
                "UAS": uas,
                "Nilai Akhir": nilai_akhir,
                "Grade": grade,
                "Keterangan": ket
            }])

            df = pd.concat([df, data_baru], ignore_index=True)
            save_data(df)

            st.success("Data berhasil ditambahkan!")
    return df

def tampil_data(df):
    st.subheader("📊 Data Mahasiswa")
    st.dataframe(df, use_container_width=True)

def edit_data(df):
    st.subheader("✏️ Edit Data")

    if len(df) == 0:
        st.warning("Data kosong!")
        return df

    pilih_nim = st.selectbox("Pilih NIM", df["NIM"])

    data = df[df["NIM"] == pilih_nim].iloc[0]

    tugas = st.number_input("Nilai Tugas", 0, 100, int(data["Tugas"]))
    uts = st.number_input("Nilai UTS", 0, 100, int(data["UTS"]))
    uas = st.number_input("Nilai UAS", 0, 100, int(data["UAS"]))

    if st.button("Update"):
        nilai_akhir, grade, ket = hitung_nilai(tugas, uts, uas)

        df.loc[df["NIM"] == pilih_nim, ["Tugas", "UTS", "UAS", "Nilai Akhir", "Grade", "Keterangan"]] = [
            tugas, uts, uas, nilai_akhir, grade, ket
        ]

        save_data(df)
        st.success("Data berhasil diupdate!")

    return df

def hapus_data(df):
    st.subheader("🗑️ Hapus Data")

    if len(df) == 0:
        st.warning("Data kosong!")
        return df

    pilih_nim = st.selectbox("Pilih NIM untuk dihapus", df["NIM"])

    if st.button("Hapus"):
        df = df[df["NIM"] != pilih_nim]
        save_data(df)
        st.success("Data berhasil dihapus!")

    return df

# ========================
# MAIN APP
# ========================
def main():
    if "login" not in st.session_state:
        st.session_state["login"] = False

    if not st.session_state["login"]:
        login()
        return

    st.sidebar.title("📚 Menu")
    menu = st.sidebar.radio("Pilih Menu", [
        "Dashboard",
        "Tambah Data",
        "Edit Data",
        "Hapus Data"
    ])

    df = load_data()

    if menu == "Dashboard":
        tampil_data(df)

    elif menu == "Tambah Data":
        df = tambah_data(df)

    elif menu == "Edit Data":
        df = edit_data(df)

    elif menu == "Hapus Data":
        df = hapus_data(df)

# ========================
# RUN
# ========================
if __name__ == "__main__":
    main()