import os
import time
import argparse
from typing import List
from tqdm import tqdm

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import chromadb

# Ensure necessary dependencies are installed
try:
    import pymupdf
except ImportError:
    print("Missing dependency: 'pymupdf'. Install it using: pip install pymupdf")
    exit(1)

# Set environment variables
PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY", "db")
EMBEDDINGS_MODEL_NAME = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
MODEL = os.environ.get("MODEL", "mistral")
TARGET_SOURCE_CHUNKS = int(os.environ.get("TARGET_SOURCE_CHUNKS", 4))


def load_documents(pdf_path: str) -> List[Document]:
    """Loads a single PDF document manually specified by the user."""
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        exit(1)

    print(f"Loading PDF: {pdf_path}")
    loader = PyMuPDFLoader(pdf_path)
    return loader.load()


def process_documents(pdf_path: str) -> List[Document]:
    """Processes the manually provided PDF file."""
    documents = load_documents(pdf_path)
    if not documents:
        print("No content found in the PDF.")
        exit(0)

    print(f"Loaded PDF with {len(documents)} pages")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} text chunks")
    return texts


def does_vectorstore_exist(persist_directory: str) -> bool:
    """Check if a vectorstore already exists."""
    return os.path.exists(os.path.join(persist_directory, 'chroma-collections.parquet'))


def create_vectorstore(pdf_path: str):
    """Creates a vectorstore from the provided PDF file."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
    texts = process_documents(pdf_path)

    if does_vectorstore_exist(PERSIST_DIRECTORY):
        print("Updating existing vectorstore")
        db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
        db.add_documents(texts)
    else:
        print("Creating new vectorstore")
        db = Chroma.from_documents(texts, embeddings, persist_directory=PERSIST_DIRECTORY)  # Fixed issue with persist()


def chat():
    """Starts the chatbot for querying the PDF contents."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})
    callbacks = [StreamingStdOutCallbackHandler()]
    llm = Ollama(model=MODEL, callbacks=callbacks)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    while True:
        query = input("\nEnter a query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        if not query.strip():
            continue
        start = time.time()
        res = qa(query)
        answer, docs = res['result'], res['source_documents']
        end = time.time()

        print("\n> Question:")
        print(query)
        print("\n> Answer:")
        print(answer)

        for document in docs:
            print(f"\n> Source: {document.metadata['source']}")
            print(document.page_content)


def main():
    parser = argparse.ArgumentParser(description="ChatPDF using Ollama")
    parser.add_argument("--ingest", action="store_true", help="Process and store PDF data.")
    parser.add_argument("--chat", action="store_true", help="Start the chatbot.")
    parser.add_argument("--pdf", type=str, help="Path to the PDF file (Required for --ingest)")
    args = parser.parse_args()

    if args.ingest:
        if not args.pdf:
            print("Error: You must provide a PDF file path using --pdf <file_path>")
            exit(1)
        create_vectorstore(args.pdf)

        # Automatically start chat after ingestion
        print("\nPDF processed successfully! Starting chat...\n")
        chat()
    elif args.chat:
        chat()
    else:
        print("Usage: python web.py --ingest --pdf <file_path> OR python web.py --chat")


#if _name_ == "_main_":
if __name__ == "__main__":

    main()