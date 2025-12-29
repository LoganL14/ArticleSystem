#defines constants and settings used across the project:

# arXiv API & Request Settings
BASE_URL: str =  "https://export.arxiv.org/api/query"
MAX_RESULTS: int = 5
search_term: str | None = None
REQUEST_TIMEOUT: int = 60 

# Date / Time
TZ_NAME: str = "UTC"         
DAYS_OFFSET: int = 5         
DATE_FMT_API: str = "%Y%m%d%H%M"  # format arXiv expects in submittedDate rang

# I/O Directories
DOWNLOAD_ROOT: str = "./downloaded_papers"         
MARKDOWN_ROOT: str = "./downloaded_papers_md"  
EMBEDDINGS_ROOT: str = "./downloaded_embeddings"
    
# Chunking / Splitting
MAX_CHARS: int = 2000
OVERLAP: int = 0


# Embedding 
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
