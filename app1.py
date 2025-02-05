import streamlit as st
import sqlite3
from transformers import AutoModelForCausalLM, AutoTokenizer
import datetime

# SQLite database connection
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    name TEXT,
    age INTEGER,
    gender TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    medication TEXT,
    time TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
conn.commit()

# Hugging Face Llama Model Initialization
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Model nomi
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Llama Chatbot function
def chat_with_llama(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs.input_ids, max_length=200, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit UI
st.title("Tibbiyot AI Ilovasi")
st.subheader("Xush kelibsiz!")

menu = ["Kirish", "Ro'yxatdan o'tish", "Profil", "Chatbot", "Dori Eslatmalari"]
choice = st.sidebar.selectbox("Menyuni tanlang", menu)

# User Login
if choice == "Kirish":
    st.subheader("Kirish")
    email = st.text_input("E-mail", key="login_email")
    password = st.text_input("Parol", type="password", key="login_password")
    if st.button("Kirish"):
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        if user:
            st.success(f"Xush kelibsiz, {user[3]}!")
        else:
            st.error("Email yoki parol noto'g'ri!")

# User Registration
elif choice == "Ro'yxatdan o'tish":
    st.subheader("Ro'yxatdan o'tish")
    email = st.text_input("E-mail", key="register_email")
    password = st.text_input("Parol", type="password", key="register_password")
    name = st.text_input("Ism")
    age = st.number_input("Yosh", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Jins", ["Erkak", "Ayol"])
    if st.button("Ro'yxatdan o'tish"):
        try:
            cursor.execute("INSERT INTO users (email, password, name, age, gender) VALUES (?, ?, ?, ?, ?)",
                           (email, password, name, age, gender))
            conn.commit()
            st.success("Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        except sqlite3.IntegrityError:
            st.error("Bu email allaqachon ro'yxatdan o'tgan.")

# User Profile
elif choice == "Profil":
    st.subheader("Profil")
    email = st.text_input("Emailingizni kiriting:")
    if st.button("Ma'lumotni ko'rish"):
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if user:
            st.write(f"Ism: {user[3]}")
            st.write(f"Yosh: {user[4]}")
            st.write(f"Jins: {user[5]}")

# Chatbot
elif choice == "Chatbot":
    st.subheader("Tibbiyot savollari uchun Chatbot")
    user_input = st.text_input("Savolingizni kiriting:")
    if st.button("Javobni ko'rish"):
        if user_input:
            response = chat_with_llama(user_input)
            st.write(f"Chatbot javobi: {response}")
        else:
            st.warning("Savolingizni kiriting!")

# Medication Reminders
elif choice == "Dori Eslatmalari":
    st.subheader("Dori Eslatmalari")
    email = st.text_input("Emailingizni kiriting:")
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    if user:
        medication = st.text_input("Dorining nomi")
        time = st.time_input("Dorini ichish vaqti", value=datetime.time(9, 0))
        if st.button("Qo'shish"):
            cursor.execute("INSERT INTO medications (user_id, medication, time) VALUES (?, ?, ?)",
                           (user[0], medication, str(time)))
            conn.commit()
            st.success("Dori muvaffaqiyatli qo'shildi!")
    else:
        st.warning("Bunday foydalanuvchi topilmadi.")

conn.close()
