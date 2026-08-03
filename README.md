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

## 🚀 Core Capabilities

### 📄 Intelligent Document Processing
Upload PDF documents and automatically extract, clean, and split content into meaningful chunks for efficient retrieval.

### 🧠 Semantic Search
Instead of keyword matching, the system converts both documents and user queries into vector embeddings, enabling context-aware semantic retrieval.

### 🤖 Retrieval-Augmented Generation (RAG)
Relevant document chunks are retrieved from ChromaDB and supplied to the language model, allowing answers to remain grounded in the uploaded knowledge base.

### ⚡ Local AI Inference
Uses **Qwen 3** running locally through **Ollama**, eliminating dependency on cloud-hosted LLM APIs while providing fast and private inference.

### 🏗 Modular Service-Oriented Architecture
The application separates document processing, embedding generation, retrieval, prompt construction, vector storage, and LLM interaction into independent services, making the project scalable and easy to maintain.

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
