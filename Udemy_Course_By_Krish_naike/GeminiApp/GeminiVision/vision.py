from dotenv import load_dotenv

import streamlit as st
import os
import google.generativeai as  genai
from PIL import Image


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_gemini_response(input, image):
    if input !='':
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text



st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini LLM Applications")
input = st.text_input("Input:", key="input")
uploaded_file = st.file_uploader(label="Upload Image", type=['jpg', 'png', 'gif'])
image = ""


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image. ",  use_column_width=True)

submit = st.button("Tall me About the Image ")
if submit:
    response =get_gemini_response(input, image)
    st.subheader("Response: ")
    st.write(response)

