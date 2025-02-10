import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from htmlTemplates import css, bot_template, user_template
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    pdf_docs = "E:\Projects\Chatbot_Application\Indian constitution.pdf"
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")  # Save the vector store locally

def load_vector_store():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return vector_store
    except Exception as e:
        return None  # Return None if the vector store doesn't exist

def get_conversational_chain():

    prompt_template = """
    Answer the question with the highest level of detail possible based on the provided context. 
    Ensure that all relevant details are included.

    If the answer is available in the context:
    Provide the answer with all relevant details in a structured and concise manner.

    If the answer is not available in the context:
    Respond with: "The answer is not available in the context."
    Then, suggest a helpful chat prompt to clarify or expand the context\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=1, top_k=30, top_p=0.95)

    prompt = PromptTemplate(template = prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", response["output_text"]), unsafe_allow_html=True)

def main():
    st.set_page_config("Chat with PDFs", page_icon=":open_file_folder:") 
    
    # Inject the CSS   
    st.write(css, unsafe_allow_html=True)
    
    # Header
    st.header(":rainbow[**Chat with PDFs** :material/docs:]")
    
    # User Input
    user_question = st.text_input(":orange[Ask a Question from the PDF Files :file_folder:]")
    if user_question:
        user_input(f'You asked: {user_question}')
        
    # Sidebar
    with st.sidebar:
        st.subheader(":green[**Upload Your Documents** :material/docs:]")
        st.title(":blue[Menu]")
        pdf_docs = st.file_uploader(":red[Upload your PDF Files and Click on the Submit & Process Button]", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()