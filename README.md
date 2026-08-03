# 🧠 Enterprise Knowledge Assistant

> An enterprise-grade Retrieval-Augmented Generation (RAG) application that enables users to search and interact with organizational knowledge using natural language.

Built with **FastAPI**, **ChromaDB**, **Sentence Transformers**, and **Qwen 3 (running locally with Ollama)**, the application combines semantic search with modern Large Language Models to deliver grounded, context-aware responses from uploaded documents.

---

## ✨ Key Highlights

- 📄 Upload and process PDF documents
- 🧩 Intelligent document chunking
- 🔍 Semantic search using vector embeddings
- 🗂 ChromaDB vector database
- 🤖 Local LLM inference with Qwen 3 via Ollama
- 💬 Natural language question answering
- 📚 Source-aware responses using RAG architecture
- 🏗 Modular FastAPI backend with service-oriented design

## 🏗 Architecture

```text
                User
                  │
                  ▼
          FastAPI REST API
                  │
                  ▼
         PDF Upload & Parsing
                  │
                  ▼
         Intelligent Chunking
                  │
                  ▼
      Sentence Transformers
           (Embeddings)
                  │
                  ▼
             ChromaDB
          Vector Database
                  │
                  ▼
        Semantic Retrieval
                  │
                  ▼
          Prompt Builder
                  │
                  ▼
      Qwen 3 (via Ollama)
                  │
                  ▼
      Context-Aware Response
```
## Overview

This project demonstrates how modern AI applications can help organizations search and interact with their internal knowledge base instead of manually browsing documents.

Users can upload documents, ask questions in natural language, and receive context-aware answers with supporting references.

## Key Features

- PDF document ingestion
- Intelligent document chunking
- Semantic search
- Retrieval-Augmented Generation (RAG)
- OpenAI integration
- FastAPI backend
- React frontend
- Context-aware responses
- Source citations
- Conversation history

## Tech Stack

- Python
- FastAPI
- React
- OpenAI API
- ChromaDB
- PyMuPDF
- Docker

## Project Status

🚧 Currently under active development.
