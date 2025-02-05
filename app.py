import streamlit as st
import pandas as pd
import datetime
import requests

# Foydalanuvchi ma'lumotlarini saqlash uchun
USER_DATA_FILE = "user_data.csv"

# Ma'lumotlarni yuklash va saqlash funksiyasi
def load_user_data():
    try:
        return pd.read_csv(USER_DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Age", "Gender", "Weight", "Height", "Medications"])

def save_user_data(data):
    data.to_csv(USER_DATA_FILE, index=False)

# Kirish sahifasi
def login_page():
    st.title("Tibbiyot AI - Kirish")
    name = st.text_input("Ismingizni kiriting")
    password = st.text_input("Parolingizni kiriting", type="password")
    if st.button("Kirish"):
        st.success(f"Xush kelibsiz, {name}!")

# Shaxsiy ma'lumotlar bo‘limi
def profile_page():
    st.header("Shaxsiy Ma'lumotlar")
    user_data = load_user_data()

    with st.form("profile_form"):
        name = st.text_input("Ism", value="")
        age = st.number_input("Yosh", min_value=0, max_value=120, step=1)
        gender = st.radio("Jins", options=["Erkak", "Ayol"])
        weight = st.number_input("Og‘irlik (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Bo‘yi (sm)", min_value=30.0, step=0.1)
        medications = st.text_area("Dorilar ro‘yxati")
        submitted = st.form_submit_button("Saqlash")
        
        if submitted:
            user_data = user_data._append({"Name": name, "Age": age, "Gender": gender, 
                                          "Weight": weight, "Height": height, 
                                          "Medications": medications}, ignore_index=True)
            save_user_data(user_data)
            st.success("Ma'lumotlar saqlandi!")

# Kaloriya kalkulyatori
def calorie_calculator():
    st.header("Kaloriya Kalkulyatori")
    weight = st.number_input("Og‘irlik (kg)", min_value=1.0, step=0.1)
    height = st.number_input("Bo‘yi (sm)", min_value=30.0, step=0.1)
    age = st.number_input("Yosh", min_value=0, max_value=120, step=1)
    gender = st.radio("Jins", options=["Erkak", "Ayol"])
    
    if st.button("Hisoblash"):
        bmi = weight / ((height / 100) ** 2)
        if gender == "Erkak":
            calories = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        else:
            calories = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
        
        st.success(f"Sizning BMI: {bmi:.2f}")
        st.info(f"Tavsiya etilgan kunlik kaloriyalar miqdori: {calories:.2f} kcal")

# Foydali maqolalar
def helpful_articles():
    st.header("Foydali Maqolalar")
    # Har kuni yangilanadigan API orqali maqola yuklash
    article = requests.get("https://jsonplaceholder.typicode.com/posts/1").json() # Misol uchun
    st.write(f"### {article['title']}")
    st.write(article['body'])

# Chatbot
def chatbot():
    st.header("Tibbiy Chatbot")
    user_input = st.text_input("Savolingizni kiriting")
    if st.button("Yuborish"):
        # Hugging Face NLP API orqali javob olish
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            headers={"Authorization": "Bearer YOUR_API_KEY"},
            json={"inputs": user_input}
        )
        answer = response.json().get("generated_text", "Kechirasiz, javob topilmadi.")
        st.success(answer)

# Asosiy sahifa
st.sidebar.title("Menu")
menu = st.sidebar.radio("Bo'limni tanlang", 
                        options=["Kirish", "Shaxsiy Ma'lumotlar", "Kaloriya Kalkulyatori", 
                                 "Dori Eslatmalari", "Foydali Maqolalar", "Chatbot"])

if menu == "Kirish":
    login_page()
elif menu == "Shaxsiy Ma'lumotlar":
    profile_page()
elif menu == "Kaloriya Kalkulyatori":
    calorie_calculator()
elif menu == "Dori Eslatmalari":
    st.warning("Bu bo‘lim hali ishga tushirilmagan.")
elif menu == "Foydali Maqolalar":
    helpful_articles()
elif menu == "Chatbot":
    chatbot()

