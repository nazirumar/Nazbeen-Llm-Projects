import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_pdf_text(pdf_docs):
    text =''
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text+=page.extract_text()
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local('faiss_index')
    return vector_store



def get_converstional_chain():
    prompt_template ="""
    Answer the question as detailed as possible from the provided context,make sure to provide context just say, answer is not available
    in the context, don't provide the wrong answer
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model='models/gemini-pro', temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    chain =load_qa_chain(model, chain_type='stuff', prompt=prompt)
    return chain

def user_input(user_question):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local('faiss_index', allow_dangerous_deserialization=True,embeddings=embedding)
    docs = new_db.similarity_search(user_question)

    chain = get_converstional_chain()

    response = chain(
        {
            'input_documents': docs,
            'question': user_question
        },
        return_only_outputs=True
    )

    print(response)
    st.write("Reply:", response['output_text'])

def main():
    st.set_page_config("Chat With Multiple PDF")
    st.header("Chat with  PDF using Gemini")
    user_question  = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)
    
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and click on the", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing....."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunk = get_text_chunks(text=raw_text)
                get_vector_store(text_chunk)
                st.success("Successfully")


if __name__ == '__main__':
    main()