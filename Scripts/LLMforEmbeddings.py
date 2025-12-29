from pathlib import Path
from Scripts.Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
from typing import Iterable, List, Dict
from langchain_text_splitters import MarkdownTextSplitter
from config import CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS, MAX_CHARS, OVERLAP, DOWNLOAD_ROOT, MARKDOWN_ROOT, EMBEDDINGS_ROOT
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import numpy as np


def get_start_utc_time() -> str:
    # Recompute the same date window & run id
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time

def get_embed_files(start_utc_time: str) -> List[str]:
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.npy")]


def load_embeddings(embed_file: str) -> str:
    """Read the embedding npy files """
    return Path(embed_file).read_text(encoding="")



if __name__ == "__main__":

    start_utc_time = get_start_utc_time()

    embed_files = get_embed_files(start_utc_time)

    print(embed_files)

