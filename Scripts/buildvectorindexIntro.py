
#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
#function formatting, ->
from typing import List, Dict
#uses config.py to bring in necessary global arguments
from config import MAX_CHARS, OVERLAP, DOWNLOAD_ROOT, MARKDOWN_ROOT, EMBEDDINGS_ROOT
#used for embedding / vector use
import numpy as np


import chromadb
from chromadb.config import Settings
import faiss


def get_start_utc_time() -> str:
    """ Recompute the same date window for reference """
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time


def get_embed_files(start_utc_time: str) -> List[str]:
    """  Pull the current embeddding files (.npy) """
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.npy")]


def get_meta_files(start_utc_time: str) -> List[str]:
    """  Pull the current embeddding metadata files (.jsonl) """
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.jsonl")]


def load_embeddings(embed_file: str) -> np.ndarray:
    """Read the embedding npy files into numpy arrays """
    return np.load(embed_file)

# def load_embeddingmeta(meta_files: str):
#      """Read the jsonl files """
#      return 





if __name__ == "__main__":

    start_utc_time = get_start_utc_time()

    embed_files = get_embed_files(start_utc_time)
    meta_files = get_meta_files(start_utc_time)

    print(f"Found {len(embed_files)} .npy files")


# Concatenate all vectors → normalize → build FAISS IndexFlatIP → 
# query with a normalized embedding → get top‑k row indices.

all_vecs = []
for npy_file in embed_files:
    X = load_embeddings(npy_file)
    all_vecs.append(X)

X_all = np.vstack(all_vecs)
print(f"Global shape: {X_all.shape}")

norms = np.linalg.norm(X_all, axis=1, keepdims = True)
Xn = X_all / np.maximum(norms, 1e-12)

d = Xn.shape[1]
index = faiss.IndexFlatIP(d)
index.add(Xn)
print(f"Index size: {index.ntotal}")

query = np.random.randn(d)
query /= np.linalg.norm(query)

k = 5
scores, indices = index.search(query.reshape(1,-1), k)
print("Top-k indices:", indices[0])
print("Scores:", scores[0])

# chroma_client = chromadb.EphemeralClient()
# chroma_collection = chroma_client.create_collection()

# chroma_collection.add(
#     ids = [str(i) for i in range(len(embed_files))],
#     embeddings = embeddings.tolist()
# )


