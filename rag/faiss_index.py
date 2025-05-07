# rag/faiss_index.py
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# Load tokenizer and model once
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def encode_text(texts):
    """
    Encode list of texts to dense vectors using BERT mean pooling.
    """
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    return embeddings

def build_faiss_index(text_list):
    """
    Build FAISS index from a list of text strings.
    """
    embeddings = encode_text(text_list)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, text_list  # return original texts to map results

def search_faiss_index(query, index, corpus_texts, top_k=5):
    """
    Search FAISS index and return top-k matching texts.
    """
    query_vec = encode_text([query])
    distances, indices = index.search(query_vec, top_k)
    return [corpus_texts[i] for i in indices[0]]
