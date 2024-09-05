from dotenv import load_dotenv
from PIL import Image

import streamlit as st
import os
import google.generativeai as  genai


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("models/gemini-1.5-flash")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_part =[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("Gemini LLM Applications")
input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader(label="Choice an Image of the invoice........", type=['jpg', 'png', 'gif'])

image= ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image. ",  use_column_width=True)

submit = st.button("Tell me about the invoice")


input_prompt = """
You are expert in understanding invoices. We will upload a a image as invoice and you will have answer any question based on the uploaded invoice image
"""
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is: \n")
    st.write(response)

