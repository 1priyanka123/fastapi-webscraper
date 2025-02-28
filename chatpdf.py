import pdfplumber
import tkinter as tk
from tkinter import filedialog
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Load Ollama embeddings model
embedding_model = OllamaEmbeddings(model="llama3.2")

# Function to create ChromaDB vector store
def create_chroma_vector_store(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(pdf_text)

    # Create ChromaDB index
    chroma_db = Chroma.from_texts(chunks, embedding_model, persist_directory="./chroma_db")
    return chroma_db

# Retrieve relevant text from ChromaDB
def retrieve_relevant_text(chroma_db, query):
    """Retrieve the most relevant text chunk from ChromaDB."""
    docs = chroma_db.similarity_search(query, k=3)  # Get top 3 most similar chunks
    retrieved_text = " ".join([doc.page_content for doc in docs])
    return retrieved_text

# Load AI model using Ollama
llm = ChatOllama(model="llama3.2")

# Function to generate chatbot response
def chat_with_pdf(chroma_db, user_query):
    relevant_text = retrieve_relevant_text(chroma_db, user_query)
    prompt = f"PDF Content:\n{relevant_text}\n\nUser Query: {user_query}\nAnswer:"
    response = llm.invoke(prompt)
    return response

# Select PDF using Tkinter
root = tk.Tk()
root.withdraw()
pdf_path = filedialog.askopenfilename(title="Select a PDF File", filetypes=[("PDF Files", "*.pdf")])

if pdf_path:
    print(f"Processing: {pdf_path}")

    # Extract text and create ChromaDB index
    pdf_text = extract_text_from_pdf(pdf_path)
    chroma_db = create_chroma_vector_store(pdf_text)

    # Get user query
    user_query = input("Enter your question: ")
    response = chat_with_pdf(chroma_db, user_query)

    print("\n🤖 Chatbot Response:\n", response)
else:
    print("No PDF file selected.")
