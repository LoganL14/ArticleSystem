

# arXiv API & Request Setting
BASE_URL = "https://export.arxiv.org/api/query"
MAX_RESULTS = 5
search_term = None
REQUEST_TIMEOUT: int = 60

# Date / Time
TZ_NAME: str = "UTC" 
DAYS_OFFSET: int = 2
DATE_FMT_API: str = "%Y%m%d%H%M"

# I/O Directories
DOWNLOAD_ROOT: str = "./downloaded_papers"
MARKDOWN_ROOT: str = "./downloaded_papers_md"

# Chunking / Splitting
CHUNK_SIZE_CHARS: int = 2000
CHUNK_OVERLAP_CHARS: int = 0

# Embeddings
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"