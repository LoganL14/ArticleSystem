#Focus on semantic chunks (paragraph/sentence-aware) 
#keep chunks within reasonable token limits for your embedding model (often 500–1,000 tokens).

#Pick your embedding model (OpenAI, HuggingFace, etc.) and store vectors in a local index (FAISS/Chroma) or a managed service (Pinecone). 
# Include metadata per chunk: paper_id, title, authors, section, page_range md_path and maybe the original pdf_path

#“Text chunking for embeddings”

# Explains why you split text into smaller, semantically coherent pieces for better embedding quality.
# Covers token limits and chunk size trade-offs.

# “Semantic chunking vs fixed-size chunking”

# Shows why splitting by sentences or paragraphs is better than blindly cutting every N characters.

# Working with research papers , the goal is to summarize


#fixed-size chunking (decide how many tokens each chunk should be). easiest
#content-aware chunking (sentence level spliting, langchain???)
#recursive chunking (uses specific seperators... goes until reaching desired chunk size)
#specialized chunking (GOOD FOR MARKDOWN CONTENT)
#semantic chunking (preserves thematic coherence). most complicated

#create embeddings using different chunk sizes, store them in vector databases, run queries to evaluate performance (relevance, accuracy, speed)
#OpenAIs text-embedding-3-small
#Anthropic Claude Embedding Model
#Open source? all-MiniLM-L6-v2

# download_papers_vectors/
#   202512190000/
#     2512.18520v1/
#       chunks.json              # list[str]
#       embeddings.npy           # 2D array: (num_chunks x dim)
#       metadata.json            # chunk_index, file, offsets, etc.
#     2512.18524v1/
#       chunks.json
#       embeddings.npy
#       metadata.json
#     ...


# Embedding models
#MiniLM-L6-v2
#E5-Base-v2
#BGE-Base-v1.5
#Nomic-Embed-v1


from pathlib import Path
from typing import Iterable, List, Dict
from langchain_text_splitters import MarkdownTextSplitter

def load_markdown(md_file: str) -> str:
    """Read the Markdown file as a single string."""
    return Path(md_file).read_text(encoding="utf-8")

def chunk_by_size(text: str, max_chars: int = 2000) -> list[str]:
    """
    Split text into chunks, each up to max_chars characters.
    This is a naive splitter: it doesn't try to respect sentences/paragraphs.
    """
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunks.append(text[start:end])
        start = end
    return chunks


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

#NOW CREATE EMBEDDINGS 



if __name__ == "__main__":
    
    #Create a Dictonary with key:str and value:List
    all_chunks: Dict[str, List[str]] = {}
    all_chunks_md: Dict[str, List[str]] = {}
    
    md_file = 'downloaded_papers_md\\202512200000\\2512.18524v1.md'
    raw_text = load_markdown(md_file)
    

    #populate the Dictonary with key [file path] and value [chunk 1, chunk 2, etc]
    
    chunks = chunk_by_size(raw_text) 
    print(f"[Naive Split] Total chunks: {len(chunks)}")
    all_chunks[md_file] = chunks
    #print(all_chunks)
    
    chunksMD = chunk_langchain(raw_text)
    print(f"[LangChain Split] Total chunks: {len(chunksMD)}")
    all_chunks_md[md_file] = chunksMD
    #print(all_chunks_md)