""" Script to get all of the embedding npy files and metadata jsonl files that were put into . /downloaded_embeddings folder  (todays search)
    Now do I need to pick an LLM to process these somehow?
    Embed the query → compare it (cosine similarity) against all saved chunk embeddings → take the top k chunks → (optionally) pass those to an LLM to summarize."""

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


    print(embed_files)
    print(meta_files)

