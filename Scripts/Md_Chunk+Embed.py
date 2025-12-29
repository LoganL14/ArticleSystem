""" Script to get all of the markdown files put into . /downloaded_papers_md folder (todays search)
    Chunk the md files using langchain. Then use embedding model (sentence-transformers/all-MiniLM-L6-v2).
    Putting resulting vectors into a . /downloaded_embeddings folder (npy files)"""

from pathlib import Path
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
from typing import List, Dict
from langchain_text_splitters import MarkdownTextSplitter
from config import MAX_CHARS, OVERLAP, MARKDOWN_ROOT, EMBEDDINGS_ROOT, EMB_MODEL
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
import json

emb_model = HuggingFaceEmbeddings(model_name = EMB_MODEL)

#Need to get the md files that were grabbed today. (Involves reusing the get_utc_times_for_2daysago(), build_search_query() functions )

def get_start_utc_time() -> str:
    """ Recompute the same date window for reference """
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time

def get_md_files(start_utc_time: str) -> List[str]:
    """ Pull the current md_files for chunking and embedding """
    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    return [str(p) for p in md_folder.glob("*.md")]

def load_markdown(md_file: str) -> str:
    """Read the Markdown files """
    return Path(md_file).read_text(encoding="utf-8")


def chunk_langchain(text: str, MAX_CHARS, OVERLAP) -> List[str]:
    """
    Split text into chunks (USING LANGCHAIN), each up to max_chars characters.
    """
    markdown_splitter = MarkdownTextSplitter(
        chunk_size = MAX_CHARS,
        chunk_overlap = OVERLAP
    )
    docs = markdown_splitter.create_documents([text])
    chunks = markdown_splitter.split_text(text)
    return chunks


def save_embeddings_and_metadata(chunks: List[str], md_file: str, start_utc_time: str):
    """ Save both embeddings and metadata into new folder, . /downloaded_embeddings  """
    out_dir = Path(EMBEDDINGS_ROOT) / start_utc_time
    out_dir.mkdir(parents=True, exist_ok=True)

    #embed
    doc_embs = emb_model.embed_documents(chunks)
    emb_matrix = np.array(doc_embs, dtype=np.float32)

    #paths
    base = Path(md_file).stem  # e.g., '2512.21078v1'
    vec_path = out_dir / f"{base}_vectors.npy"
    meta_path = out_dir /f"{base}.jsonl"
    
    #save vectors
    np.save(vec_path, emb_matrix)
    print(f"[SAVE] Vectors: {vec_path} (shape={emb_matrix.shape})")

    #save metadata (confusing part?)
    with meta_path.open("w", encoding = "utf-8") as f:
        for i, chunk_text in enumerate(chunks):
            row = {
                "paper_id": base,
                "title": "",          # optional; fill later if you have it
                "url": "",            # optional; add arXiv if desired
                "md_path": md_file,
                "chunk_id": f"{base}-{i:04d}",
                "chunk_index": i,
                "chunk_text": chunk_text
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[SAVE] Metadata: {meta_path} rows={len(chunks)}")


###############################################################


if __name__ == "__main__":
    
    start_utc_time = get_start_utc_time()
    #print(start_utc_time)
    md_files = get_md_files(start_utc_time)
    #print(md_files)

    #put all the chunks into a dictonary. Where the file name is the key and the chunk is the value 
    #all_chunks: Dict[str, List[str]] = {}  # md_path -> list of chunks
    #all_embeddings: Dict[str, List[List[float]]] = {}
    #all_chunks[md_file] = chunksMD
    #all_embeddings[md_file] = doc_embs

#for each md file. You will see "Total Chunks: X", npy file saved and its shape, .jsonl file saved and rows 
    for md_file in md_files:
        text = load_markdown(md_file)
        chunksMD = chunk_langchain(text, MAX_CHARS, OVERLAP)  # try 1000, 1500, 2000, etc.
        print(f"[LangChain Split] Total chunks: {len(chunksMD)}")
        save_embeddings_and_metadata(chunksMD, md_file, start_utc_time)
        
    