from pathlib import Path
from Fetch_PDFs_Daily import get_utc_times_for_2daysago, build_search_query
from typing import Iterable, List, Dict
from langchain_text_splitters import MarkdownTextSplitter
from config import CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS, MAX_CHARS, OVERLAP, DOWNLOAD_ROOT, MARKDOWN_ROOT, EMBEDDINGS_ROOT
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import numpy as np

#Need to get the md files that were grabbed today. (Involves reusing the get_utc_times_for_2daysago(), build_search_query() functions )

def get_start_utc_time() -> str:
    # Recompute the same date window & run id
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time

def get_md_files(start_utc_time: str) -> List[str]:
    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    return [str(p) for p in md_folder.glob("*.md")]


###############################################################

def load_markdown(md_file: str) -> str:
    """Read the Markdown files """
    return Path(md_file).read_text(encoding="utf-8")


def chunk_langchain(text: str, MAX_CHARS, OVERLAP) -> List[str]:
    """
    Split text into chunks (USING LANGCHAIN INSTEAD), each up to max_chars characters.
    """
    markdown_splitter = MarkdownTextSplitter(
        chunk_size = MAX_CHARS,
        chunk_overlap = OVERLAP
    )
    docs = markdown_splitter.create_documents([text])
    chunks = markdown_splitter.split_text(text)
    return chunks



###############################################################


if __name__ == "__main__":
    
    start_utc_time = get_start_utc_time()
    #print(start_utc_time)
    md_files = get_md_files(start_utc_time)
    #print(md_files)

    emb_model = HuggingFaceBgeEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    out_dir = Path(EMBEDDINGS_ROOT) / start_utc_time
    out_dir.mkdir(parents=True, exist_ok=True)


    #put all the chunks into a dictonary. Where the file name is the key and the chunk is the value 
    all_chunks: Dict[str, List[str]] = {}  # md_path -> list of chunks
    all_embeddings: Dict[str, List[List[float]]] = {}

    for md_file in md_files:
        text = load_markdown(md_file)
        chunksMD = chunk_langchain(text, MAX_CHARS, OVERLAP)  # try 1000, 1500, 2000, etc.
        print(f"[LangChain Split] Total chunks: {len(chunksMD)}")
        all_chunks[md_file] = chunksMD
        
        doc_embs = emb_model.embed_documents(chunksMD)
        all_embeddings[md_file] = doc_embs
        
        base = Path(md_file).stem  # e.g., '2512.21078v1'
        vec_path = out_dir / f"{base}_vectors.npy"

        
        emb_matrix = np.array(doc_embs, dtype=np.float32)
        np.save(vec_path, emb_matrix)
        print(f"[SAVE] Vectors: {vec_path} (shape={emb_matrix.shape})")


    print(f"[SAVE] Vectors: {vec_path} (shape={emb_matrix.shape})")