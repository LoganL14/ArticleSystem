from pathlib import Path
from Fetch_PDFs_Daily import get_utc_times_for_2daysago, build_search_query
from typing import Iterable, List, Dict
from langchain_text_splitters import MarkdownTextSplitter


#Need to get the md files that were grabbed today. (Involves reusing the get_utc_times_for_2daysago(), build_search_query() functions )

def get_start_utc_time() -> str:
    # Recompute the same date window & run id
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time

def get_md_files(start_utc_time: str) -> list[str]:
    md_folder = Path(f"./TEST_downloaded_papers_md/{start_utc_time}")
    return [str(p) for p in md_folder.glob("*.md")]


###############################################################


def load_markdown(md_file: str) -> str:
    """Read the Markdown files """
    return Path(md_file).read_text(encoding="utf-8")

# def chunk_by_size(text: str, max_chars: int = 2000) -> list[str]:
#     """
#     Split text into chunks, each up to max_chars characters.
#     This is a naive splitter: it doesn't try to respect sentences/paragraphs.
#     """
#     chunks = []
#     start = 0
#     n = len(text)
#     while start < n:
#         end = min(start + max_chars, n)
#         chunks.append(text[start:end])
#         start = end
#     return chunks


def chunk_langchain(text: str, max_chars: int = 2000, overlap: int = 0) -> list[str]:
    """
    Split text into chunks (USING LANGCHAIN INSTEAD), each up to max_chars characters.
    """
    markdown_splitter = MarkdownTextSplitter(
        chunk_size = max_chars,
        chunk_overlap = overlap
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

    
    #put all the chunks into a dictonary. Where the file name is the key and the chunk is the value 
    all_chunks: Dict[str, List[str]] = {}  # md_path -> list of chunks

    for md_file in md_files:
        text = load_markdown(md_file)
        chunks = chunk_langchain(text, max_chars=2000)  # try 1000, 1500, 2000, etc.
        print(f"[LangChain Split] Total chunks: {len(chunks)}")
        all_chunks[md_file] = chunks
        

