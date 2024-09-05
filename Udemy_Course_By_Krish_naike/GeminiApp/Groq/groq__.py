import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


groq_api_key = os.getenv('GROQ_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

st.title('Gemma Model Document Q&A')

llm = ChatGroq(api_key=groq_api_key, model='Gemma-7b-it')

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided context only.
    Please provide the most accurate response based on the question <content>
    {context}
    <context>
    Questions: {input}
"""
)

def vector_embedding():
    if 'vectors' not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
        st.session_state.loader = PyPDFDirectoryLoader('./pdf_books')
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

prompt1 =st.text_input("What you want ask from the documents?")

if st.button('Creating Vector Store'):
    vector_embedding()
    st.write('Vector Store Created Successfully!')

import time

if prompt1:
    st.write('Processing...')
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriver = st.session_state.vectors.as_retriever()
    chain = create_retrieval_chain(retriver, document_chain)
    start = time.process_time()
    response = chain.invoke({"input":prompt1})
    st.write(time.process_time())
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i,docs, in enumerate(response['context']):
            st.write(docs.page_content)
            st.write("----------------------------------------")