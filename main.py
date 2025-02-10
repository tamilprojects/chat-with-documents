import os
import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "chatbot"

# Create Pinecone index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud='aws', region='us-east-1')  # Adjust region as needed
    )

# Connect to the Pinecone index
index = pc.Index(index_name)

# Streamlit App Title
st.title("Document Chatbot with Streamlit")

# Function to load a PDF document
def load_pdf(file):
    st.write("Loading PDF document...")
    loader = PyPDFLoader(file)
    return loader.load()

# Function to split documents into smaller chunks
def split_documents(docs, chunk_size=500, chunk_overlap=30):
    st.write("Splitting document into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

# Function to download Hugging Face embeddings
def download_hugging_face_embeddings():
    st.write("Loading Hugging Face embeddings...")
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Function to initialize vector store using LangChain's Pinecone integration
def initialize_vector_store(docs, embeddings):
    st.write("Setting up Pinecone vector store...")
    vector_store = LangchainPinecone.from_documents(
        documents=docs,
        embedding=embeddings,
        index=index,  # Pass the Pinecone index instance directly
    )
    return vector_store

# Main App Workflow
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file is not None:
    # Step 1: Load PDF document
    docs = load_pdf(uploaded_file)

    # Step 2: Split the document into chunks
    docs = split_documents(docs)

    # Step 3: Load embeddings
    embeddings = download_hugging_face_embeddings()

    # Step 4: Initialize vector store
    vector_store = initialize_vector_store(docs, embeddings)

    # Step 5: Set up Retrieval QA
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = OpenAI(temperature=0)  # Use OpenAI model or equivalent
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Step 6: Enter and process question
    question = st.text_input("Enter your question:")
    if question:
        st.write("Retrieving documents...")
        result = qa_chain({"query": question})
        st.write("Answer:")
        st.write(result["result"])
        st.write("Sources:")
        for doc in result["source_documents"]:
            st.write(doc.page_content)
else:
    st.write("Please upload a PDF file to get started.")
