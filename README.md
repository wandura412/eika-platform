# Enterprise Intelligent Knowledge Assistant (EIKA) 🤖

**A secure, offline-first Retrieval-Augmented Generation (RAG) platform built with Python, FastAPI, and Local LLMs.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Llama 3](https://img.shields.io/badge/Model-Llama3-purple)

## 📖 Project Overview

EIKA is a microservices-based AI application designed to ingest corporate documents (PDFs) and allow users to query them using natural language. Unlike standard RAG demos, EIKA is built with **production-grade architecture** in mind:

* **Microservices Pattern:** Decoupled Backend (FastAPI) and Frontend (Streamlit).
* **Pure Python Logic:** Custom sliding-window chunking and retrieval algorithms (no heavy frameworks like LangChain used for core logic).
* **Privacy First:** Runs entirely offline using local embeddings and Llama 3 via Ollama.
* **Containerized:** Fully dockerized for easy deployment.

## 🏗️ Architecture

The system follows a **Clean Architecture** pattern, separating the "Storefront" (API) from the "Warehouse" (Business Logic).

```mermaid
graph LR
    User[User] -->|Interacts| UI[Streamlit Frontend]
    UI -->|HTTP Request| API[FastAPI Backend]
    API -->|Ingest/Search| Service[Vector Service]
    Service -->|Store/Retrieve| DB[(ChromaDB)]
    API -->|Generate Answer| LLM[LLM Service]
    LLM -->|Inference| Ollama[Ollama (Llama 3)]