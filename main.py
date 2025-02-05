import streamlit as st
from db_utils import init_db, add_user, get_user_by_email
from auth import hash_password, verify_password

init_db()

st.title("Tibbiyot AI")

menu = st.sidebar.selectbox("Bo'limlar", ["Ro'yxatdan o'tish", "Kirish", "Profil", "Dorilar"])

if menu == "Ro'yxatdan o'tish":
    st.header("Ro'yxatdan o'ting")
    username = st.text_input("Foydalanuvchi nomi")
    email = st.text_input("E-pochta")
    password = st.text_input("Parol", type="password")
    confirm_password = st.text_input("Parolni tasdiqlang", type="password")
    age = st.number_input("Yosh", min_value=0, max_value=120, step=1)
    gender = st.radio("Jinsi", ["Erkak", "Ayol"])
    phone = st.text_input("Telefon raqami")

    if st.button("Ro'yxatdan o'tish"):
        if password != confirm_password:
            st.error("Parollar mos emas!")
        else:
            password_hash = hash_password(password)
            if add_user(username, email, password_hash, age, gender, phone):
                st.success("Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            else:
                st.error("Foydalanuvchi nomi yoki e-pochta mavjud.")

elif menu == "Kirish":
    st.header("Hisobga kiring")
    email = st.text_input("E-pochta")
    password = st.text_input("Parol", type="password")

    if st.button("Kirish"):
        user = get_user_by_email(email)
        if user and verify_password(password, user[3]):
            st.success(f"Xush kelibsiz, {user[1]}!")
            st.session_state["user_id"] = user[0]
        else:
            st.error("E-pochta yoki parol noto‘g‘ri.")

elif menu == "Profil":
    if "user_id" not in st.session_state:
        st.warning("Avval hisobga kiring!")
    else:
        st.header("Profil")
        user = get_user_by_email(st.session_state["user_id"])
        st.write(f"Foydalanuvchi: {user[1]}")
        st.write(f"E-pochta: {user[2]}")

elif menu == "Dorilar":
    st.header("Dorilar")
    # Dorilarni qo'shish va boshqarish qismi
