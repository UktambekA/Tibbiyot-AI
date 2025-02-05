import os
import PyPDF2
import streamlit as st
from llama_index.core import GPTVectorStoreIndex, Document
from sentence_transformers import SentenceTransformer

# PDF reading function
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Streamlit interface
st.title("Tibbiyot Psixologiyasi Chatbot")
st.write("PDF asosida savollarga javob beruvchi oddiy chatbot (Llama)")

# User PDF upload
uploaded_file = st.file_uploader("PDF faylni yuklang:", type=["pdf"])

if uploaded_file:
    # Read PDF text
    st.write("PDF yuklandi. Iltimos, kuting...")
    pdf_text = read_pdf(uploaded_file)

    # Convert text to LlamaIndex document
    document = Document(text=pdf_text)

    # Create vector store
    st.write("Vektor bazasini yaratish...")
    hf_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight, free model
    index = GPTVectorStoreIndex.from_documents([document], embed_model=hf_model)

    # User query
    query = st.text_input("Savolingizni kiriting:")
    if query:
        response = index.query(query)
        st.write("Javob:")
        st.write(response.response)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

# Chat-botga ko'rsatma:
"""
Siz aqlli suhbatdosh bo'lgan virtual yordamchi sifatida ishlaysiz. 
Foydalanuvchi bilan muloqotda aniq va foydali javoblar bering. 
Agar savolga javob bera olmasangiz, ochiqchasiga ayting.
"""

# Misol kirish va chiqish:
# User: "Python dasturlash tili haqida ma'lumot berishingiz mumkinmi?"
# Bot: "Albatta! Python - bu umumiy maqsadli, 
# yuqori darajadagi dasturlash tili bo'lib, 
# oson sintaksis va kuchli kutubxonalari bilan mashhur."

import openai

def chatbot_response(user_input):
    """
    OpenAI API yordamida foydalanuvchi savollariga javob qaytaruvchi funksiya.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Siz aqlli suhbatdosh bo'lgan virtual yordamchisiz."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Test uchun kirish:
user_input = "Menga GPT-4 modeli haqida tushuntirib bera olasizmi?"
bot_output = chatbot_response(user_input)
print("Bot javobi:", bot_output)
