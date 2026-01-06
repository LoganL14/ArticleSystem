#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
#function formatting, -> 
from typing import List, Dict
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



def get_start_utc_time() -> str:
    """ Recompute the same date window for reference """

    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc) 
    return start_utc_time


def get_md_files(start_utc_time: str) -> List[str]:
    """ Pull the current md_files for chunking and embedding """

    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    #print(MARKDOWN_ROOT) / start_utc_time
    #print(Path(MARKDOWN_ROOT) / start_utc_time)
    # md_all_files = []
    # for file in Path(md_folder).glob("*.md"):
    #         md_all_files.append(str(file))
    # print(md_all_files)

    #from pathlib import Path... .glob lets you search for files in the specified directory for any ending in .md (using the *)
    return [str(path) for path in md_folder.glob("*.md")]


def load_markdown(md_file: str) -> str:
    """Read the Markdown files """

#You use Path(), when the path is a str and need to give python a way of understanding it.
#use read_text for text files: .md, .txt, .py, .json... tkaes the information and returns string
#other helpful functions on a file are .mkdir(), .open(), .read_bytes(), .write_text(), .write_bytes(), .exists(), .is_file(), .glob(), .resolve()
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


def chunk_langchain_docs(text: str, MAX_CHARS, OVERLAP):
    """ Used to create chunks. Set parameters like max_chars and overlapping chunks.
     Returns:
        Split text into chunks (USING LANGCHAIN), each up to max_chars characters."""
    
    markdown_splitter = MarkdownTextSplitter(
        chunk_size = MAX_CHARS,
        chunk_overlap = OVERLAP
    )
    docs = markdown_splitter.create_documents([text])
    return docs


def save_embeddings_and_metadata(chunks: List[str], md_file: str, start_utc_time: str) -> None:
    """Save both embeddings and metadata into new folder, . /downloaded_embeddings  
    Returns:
        Confirmation of vectors and metadata saved... and the shape of these outputs."""
    
    #create directory for files
    out_dir = Path("downloaded_embeddings_TEST") / start_utc_time
    out_dir.mkdir(parents=True, exist_ok=True)

    #embedding model
    doc_embs = emb_model.embed_documents(chunks)
    emb_matrix = np.array(doc_embs, dtype=np.float32)

    #create paths
    base = Path(md_file).stem  # e.g., '2512.21078v1'
    vec_path = out_dir / f"{base}_vectors"
    meta_path = out_dir /f"{base}.jsonl"
    
    #save vectors to path 
    np.save(vec_path, emb_matrix)
    print(f"[SAVE] Vectors: {vec_path} (shape={emb_matrix.shape})")

    #save metadata to path 
    #first, open the metadata path, say you are writting in it (w), specifically utf-8
    with meta_path.open("w", encoding = "utf-8") as f:
        #loops through each index and chunk_text
        for i, chunk_text in enumerate(chunks):
            row = {
                "paper_id": base,
                "md_path": md_file,
                "chunk_id": f"{base}-{i:04d}",
                "chunk_index": i,
                "chunk_text": chunk_text
            }
            #need to convert the python dict into a json formatted string
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"[SAVE] Metadata: {meta_path} rows={len(chunks)}")




start_utc_time = get_start_utc_time()
#print(start_utc_time)
md_files = get_md_files(start_utc_time)
#print(md_files)

all_chunksex = []
for file in md_files:
    text = load_markdown(file)
    chunks = chunk_langchain(text, MAX_CHARS, OVERLAP)
    print(f"[LangChain Split] Total chunks: {len(chunks)}")
    save_embeddings_and_metadata(chunks, file, start_utc_time)


# all_docs = []
# for file in md_files:
#     text = load_markdown(file)
#     docs = chunk_langchain_docs(text, MAX_CHARS, OVERLAP)
#     all_docs.extend(docs)
# first_doc = all_docs[0]
# print(first_doc)



# .create_documents()  This keeps metadata as well
# could use this to add metadata... (still need to extract and put into a jsonl file after)

# .split_text() This will only extract the chunks
# use this, and then later create rows of metadata and write into a jsonl file

# .extend() gives one long list of all the chunks, no seperation by files
# .append() will add each element at the end of current loop... which will make it a list of lists (but can differeniate files by this)

#list of lists
#doc_embs = emb_model.embed_documents(chunks)
#Numpy array, to clean up the embedding vectors
#emb_matrix = np.array(doc_embs, dtype=np.float32)

#for i, chunk_text in enumerate(chunks):
# enumerate)(chunks)   ---- (0, chunks[0])  , (1, chunks[1]) , etc
# i, chunk_text   = (i, chunk_text) , (i1, chunk_text1) , etc

# find max tokens for each embedding model I can use. change max_char to fit the embedding model

# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# for i, chunk in enumerate(chunks):
#     token_count = len(tokenizer.tokenize(chunk))
#     if token_count > 512:
#         print(f"Chunk {i} exceeds limit: {token_count} tokens")



