# 🤖 TechMart AI Support Architecture

A full-stack, multi-agent artificial intelligence customer support system designed to automatically classify, route, and resolve user queries. This project demonstrates a complete production-grade MLOps pipeline, from a vector database knowledge base to Docker containerization.

## 🚀 Features

* **Intelligent Routing (Master Orchestrator):** Utilizes an LLM to analyze the intent of a customer's message and dynamically route it to the correct specialized department (Billing, Technical, Product, Complaints, or FAQ).
* **Retrieval-Augmented Generation (RAG):** Employs FAISS and HuggingFace Embeddings to search a local database of company policies and ground the AI's answers in factual, company-specific documentation.
* **Long-Term Memory:** Implements a SQLite database to log session IDs, user queries, routing decisions, and AI responses, creating a permanent audit trail of conversations.
* **Full-Stack Architecture:** Features a robust FastAPI backend connected to a responsive Streamlit frontend chat interface.
* **Production-Ready Deployment:** Fully containerized using Docker and Docker Compose for seamless, portable execution across any environment.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI, Uvicorn, SQLite
* **AI & Machine Learning:** Google Gemini, LangChain, FAISS (Vector Store), HuggingFace (`sentence-transformers`)
* **DevOps & Infrastructure:** Docker, Docker Compose, Git

## ⚙️ How to Run Locally

### 1. Prerequisites
Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running on your machine.

### 2. Environment Setup
Create a `.env` file inside the `backend` directory and add your Google Gemini API key:
```ini
GEMINI_API_KEY=your_api_key_here