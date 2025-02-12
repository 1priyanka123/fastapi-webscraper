import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF
import chromadb
from transformers import pipeline
from google.colab import files

# Install necessary dependencies in Colab
!apt - get
install
tesseract - ocr
!pip
install
pytesseract
!pip
install
selenium
!pip
install
chromadb
!pip
install
transformers


def fetch_document_text_with_ocr(document_path, password=None):
    """Extract text from a PDF, using OCR for scanned PDFs and handle encrypted PDFs"""
    if document_path.lower().endswith(".pdf"):
        try:
            doc = fitz.open(document_path)

            # If the document is encrypted, try to decrypt using a password
            if doc.is_encrypted:
                if password:
                    doc.authenticate(password)
                else:
                    print("Password required to decrypt the PDF.")
                    return None

            document_text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # Extract text if available
                page_text = page.get_text()
                if page_text:
                    document_text += page_text
                else:
                    # Perform OCR on the page image if no text is found
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    document_text += pytesseract.image_to_string(img)

            return document_text.strip()
        except Exception as e:
            print(f"Error reading PDF document: {e}")
            return None
    else:
        print("Unsupported file format.")
        return None


def store_in_chromadb(doc_name, text):
    """Store document content in ChromaDB"""
    client = chromadb.PersistentClient(path="/content/chroma_db")  # Persistent storage in Colab
    collection = client.get_or_create_collection("document_data")
    collection.add(ids=[doc_name], documents=[text])
    print("✅ Document content stored in ChromaDB.")


def retrieve_from_chromadb(doc_name):
    """Retrieve document content from ChromaDB"""
    client = chromadb.PersistentClient(path="/content/chroma_db")
    collection = client.get_or_create_collection("document_data")
    results = collection.get(ids=[doc_name])
    if results and 'documents' in results and results['documents']:
        return results['documents'][0]
    return None


def answer_question(document_text, question):
    """Answer a question based on the document's content using Hugging Face's QA pipeline"""
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Adjust parameters for more detailed answers
    result = qa_pipeline(
        question=question,
        context=document_text,
        max_answer_length=200,  # Controls the length of the answer
        min_answer_length=50,  # Ensure answers are not too short
    )

    print("Model Output:", result)  # Print the full output to debug
    return result['answer']


def upload_file():
    """Upload a file in Colab"""
    uploaded = files.upload()
    if uploaded:
        return list(uploaded.keys())[0]
    return None


def qa_bot():
    """Main function for interactive QA bot"""
    print("🤖 Hello! I'm your Document QA Bot.")
    print("Type 'exit' to quit at any time.")

    document_path = upload_file()

    if not document_path:
        print("❌ No file uploaded. Exiting...")
        return

    document_text = retrieve_from_chromadb(document_path)

    if not document_text:
        print("📡 Fetching document content...")
        document_text = fetch_document_text_with_ocr(document_path)
        if document_text:
            store_in_chromadb(document_path, document_text)

    if document_text:
        print("\n✅ Document text is ready. You can now ask questions.")
        while True:
            question = input("\n❓ Ask your question: ")
            if question.lower() == 'exit':
                print("👋 Goodbye!")
                break
            answer = answer_question(document_text, question)
            print(f"💡 Answer: {answer}")
    else:
        print("❌ Failed to fetch document content. Please check the file.")


if __name__ == "__main__":  # Changed _name_ to __name__
    qa_bot()