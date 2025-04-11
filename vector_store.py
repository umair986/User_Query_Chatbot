# vector_store.py

import os
import chromadb
from config import CHROMA_DB_DIR, GEMINI_API_KEY
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection("kb_collection")

def embed_text(text, task="retrieval_document"):
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type=task
        )
        return response["embedding"]
    except Exception as e:
        print(f"❌ Error embedding text: {e}")
        return [0.0] * 768  # Fallback embedding

def add_to_vector_store(docs):
    ids = [f"doc_{i}" for i in range(len(docs))]
    embeddings = [embed_text(doc, task="retrieval_document") for doc in docs]
    collection.add(documents=docs, embeddings=embeddings, ids=ids)
    chroma_client.persist()

def query_vector_store(query, top_k=3):
    query_embedding = embed_text(query, task="retrieval_query")
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results.get("documents", [[]])[0]
