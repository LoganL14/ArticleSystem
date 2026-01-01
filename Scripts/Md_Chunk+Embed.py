""" Script to get all of the markdown files put into . /downloaded_papers_md folder (todays search)
    Chunk the md files using langchain. Then use embedding model (sentence-transformers/all-MiniLM-L6-v2).
    Putting resulting vectors into a . /downloaded_embeddings folder (npy files)"""

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
#function formatting, -> 
from typing import List
#Langchain for chunking and embedding 
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
#uses config.py to bring in necessary global arguments
from config import MAX_CHARS, OVERLAP, MARKDOWN_ROOT, EMBEDDINGS_ROOT, EMB_MODEL
#used for embedding / vector use
import numpy as np
#used for embedding metadata
import json

#saving the model used for embedding
emb_model = HuggingFaceEmbeddings(model_name = EMB_MODEL)

from context import ctx

#REMOVE SINCE CONTEXT.PY FILE
# def get_start_utc_time() -> str:
#     """ Recompute the same date window for reference """

#     twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
#     search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc) 
#     return start_utc_time


def get_md_files(start_utc_time: str) -> List[str]:
    """ Pull the current md_files for chunking and embedding """

    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    # md_all_files = []
    # for file in Path(md_folder).glob("*.md"):
    #         md_all_files.append(str(file))
    # print(md_all_files)
    return [str(path) for path in md_folder.glob("*.md")]


def load_markdown(md_file: str) -> str:
    """Read the Markdown files """

    return Path(md_file).read_text(encoding="utf-8")


def chunk_langchain(text: str, MAX_CHARS, OVERLAP) -> List[str]:
    """ Used to create chunks. Set parameters like max_chars and overlapping chunks.
     Returns:
        Split text into chunks (USING LANGCHAIN), each up to max_chars characters."""
    
    markdown_splitter = MarkdownTextSplitter(
        chunk_size = MAX_CHARS,
        chunk_overlap = OVERLAP
    )
    chunks = markdown_splitter.split_text(text)
    return chunks


def save_embeddings_and_metadata(chunks: List[str], md_file: str, start_utc_time: str) -> None:
    """Save both embeddings and metadata into new folder, . /downloaded_embeddings  
    Returns:
        Confirmation of vectors and metadata saved... and the shape of these outputs."""
    
    #create directory for files
    out_dir = Path(EMBEDDINGS_ROOT) / start_utc_time
    out_dir.mkdir(parents=True, exist_ok=True)

    #embedding model
    doc_embs = emb_model.embed_documents(chunks)
    emb_matrix = np.array(doc_embs, dtype=np.float32)

    #create paths
    base = Path(md_file).stem  # e.g., '2512.21078v1'
    vec_path = out_dir / f"{base}_vectors.npy"
    meta_path = out_dir /f"{base}.jsonl"
    
    #save vectors to path 
    np.save(vec_path, emb_matrix)
    print(f"[SAVE] Vectors: {vec_path} (shape={emb_matrix.shape})")

    #save metadata to path (confusing part?)
    with meta_path.open("w", encoding = "utf-8") as f:
        for i, chunk_text in enumerate(chunks):
            row = {
                "paper_id": base,
                "md_path": md_file,
                "chunk_id": f"{base}-{i:04d}",
                "chunk_index": i,
                "chunk_text": chunk_text
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[SAVE] Metadata: {meta_path} rows={len(chunks)}")


if __name__ == "__main__":
    
    md_files = get_md_files(ctx.start_utc_time)
    #print(md_files)

    #put all the chunks into a dictonary. Where the file name is the key and the chunk is the value 
    #all_chunks: Dict[str, List[str]] = {}  # md_path -> list of chunks
    #all_embeddings: Dict[str, List[List[float]]] = {}
    #all_chunks[md_file] = chunksMD
    #all_embeddings[md_file] = doc_embs

    #for each md file. You will see "Total Chunks: X", npy file saved and its shape, .jsonl file saved and rows 
    for md_file in md_files:
        text = load_markdown(md_file)
        chunksMD = chunk_langchain(text, MAX_CHARS, OVERLAP)
        print(f"[LangChain Split] Total chunks: {len(chunksMD)}")
        save_embeddings_and_metadata(chunksMD, md_file, ctx.start_utc_time)
        
    



