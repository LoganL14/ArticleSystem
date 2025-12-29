""" Script to get all of the embedding npy files that were put into . /downloaded_embeddings folder  (todays search)
    Now do I need to pick an LLM to process these somehow?"""


from pathlib import Path
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
from typing import List, Dict
from config import CHUNK_SIZE_CHARS, CHUNK_OVERLAP_CHARS, MAX_CHARS, OVERLAP, DOWNLOAD_ROOT, MARKDOWN_ROOT, EMBEDDINGS_ROOT
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


def load_embeddings(embed_file: str) -> np.ndarray:
    """Read the embedding npy file into a numpy array """
    return np.load(embed_file)



if __name__ == "__main__":

    start_utc_time = get_start_utc_time()

    embed_files = get_embed_files(start_utc_time)

    print(embed_files)

