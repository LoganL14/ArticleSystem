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
#emb_model = HuggingFaceEmbeddings(model_name = EMB_MODEL)


def get_start_utc_time() -> str:
    """ Recompute the same date window for reference """

    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc) 
    return start_utc_time


def get_md_files(start_utc_time: str) -> List[str]:
    """ Pull the current md_files for chunking and embedding """

    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    print(md_folder)
    print(Path(md_folder))
    # md_all_files = []
    # for file in Path(md_folder).glob("*.md"):
    #         md_all_files.append(str(file))
    # print(md_all_files)
    #return [str(path) for path in md_folder.glob("*.md")]



start_utc_time = get_start_utc_time()
    #print(start_utc_time)
get_md_files(start_utc_time)