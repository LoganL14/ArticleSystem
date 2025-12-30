#defines constants and settings used across the project:

# arXiv API & Request Settings
BASE_URL: str =  "https://export.arxiv.org/api/query"
MAX_RESULTS: int = 5
#could fill this (e.g., 'cat:cs.AI' or 'all:technology')
search_term: str | None = None
REQUEST_TIMEOUT: int = 60 

# Date / Time
TZ_NAME: str = "UTC"         
DAYS_OFFSET: int = 6         
DATE_FMT_API: str = "%Y%m%d%H%M"  # format arXiv expects in submittedDate rang

# Directories
DOWNLOAD_ROOT: str = "./downloaded_papers"         
MARKDOWN_ROOT: str = "./downloaded_papers_md"  
EMBEDDINGS_ROOT: str = "./downloaded_embeddings"
    
# Chunking
MAX_CHARS: int = 1400
OVERLAP: int = 0

# Embedding 
# model has max tokens of 216, and fixed vector size of 384 dimensions
#EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# model has max tokens of 512
EMB_MODEL = "BAAI/bge-small-en-v1.5"