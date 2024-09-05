from dotenv import load_dotenv

import streamlit as st
import os
import google.generativeai as  genai



load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text



st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Applications")
input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")


if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is: \n")
    st.write(response)

