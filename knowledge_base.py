import os
from pymongo import MongoClient
import chromadb
from chromadb.config import Settings
from config import (
    MONGO_URI,
    MONGO_DB_NAME,
    MONGO_COLLECTION_NAME,
    CHROMA_DB_DIR,
    GEMINI_API_KEY
)
import google.generativeai as genai

chroma_collection_name = "knowledge_base"


def create_embeddings():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.get_model("models/embedding-001")

    mongo_client = MongoClient(MONGO_URI)
    collection = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

    kb_entries = list(collection.find({}, {"_id": 0}))
    if not kb_entries:
        print("❌ No documents found in MongoDB collection.")
        return

    print(f"✅ Found {len(kb_entries)} documents in MongoDB.")
    documents = []
    embeddings = []
    ids = []

    print("🚀 Generating embeddings...")

    for i, entry in enumerate(kb_entries):
        text = entry.get("content") or entry.get("text")
        if not text or not text.strip():
            print(f"⚠️ Skipping empty entry {i}")
            continue

        try:
            response = model.embed_content(
                content=text.strip(),
                task_type="retrieval_document"
            )
            embedding = response.get("embedding")

            if not embedding:
                print("❌ Empty embedding returned for:", text)
                continue

            documents.append(text.strip())
            embeddings.append(embedding)
            ids.append(str(i))

        except Exception as e:
            print(f"💥 Error generating embedding for entry {i}: {e}")
            continue

    if not documents:
        print("❌ No valid documents to store.")
        return

    print("✅ Embeddings generated. Storing in ChromaDB...")

    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = chroma_client.get_or_create_collection(name=chroma_collection_name)

    chroma_collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    print("✅ Vector store updated with", len(documents), "documents.")


def search_knowledge_base(query: str, top_k=2):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.get_model("models/embedding-001")

    try:
        response = model.embed_content(
            content=query,
            task_type="retrieval_query"
        )
        query_embedding = response["embedding"]
    except Exception as e:
        print("❌ Failed to embed query:", e)
        return None

    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = chroma_client.get_or_create_collection(name=chroma_collection_name)

    results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    if not documents:
        return None

    return "\n\n".join(documents)
