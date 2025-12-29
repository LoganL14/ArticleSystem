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
CHUNK_SIZE_CHARS: int = 2000
CHUNK_OVERLAP_CHARS: int = 0
MAX_CHARS: int = 2000
OVERLAP: int = 0
