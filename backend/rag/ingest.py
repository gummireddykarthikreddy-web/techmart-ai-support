import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_vector_database():
    print("Loading documents...")
    # 1. Load the document (we will go up one folder level to find knowledge_base)
    file_path = os.path.join(os.path.dirname(__file__), "../../knowledge_base/faq.txt")
    loader = TextLoader(file_path)
    documents = loader.load()

    print("Chunking text...")
    # 2. Split the document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("Generating embeddings and building FAISS database...")
    # 3. Download the open-source embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Store the chunks in a FAISS vector database
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # 5. Save the database locally
    save_path = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_index")
    vectorstore.save_local(save_path)
    
    print("Vector database built successfully!")

if __name__ == "__main__":
    build_vector_database()