import os 
from dotenv import load_dotenv

load_dotenv()

# arXiv API & Request Settings
BASE_URL: str =  "https://export.arxiv.org/api/query"
MAX_RESULTS: int = 5
#could fill this (e.g., 'cat:cs.AI' or 'all:technology')
search_term: str | None = None
REQUEST_TIMEOUT: int = 60
 
# Date / Time
TZ_NAME: str = "UTC"         
DAYS_OFFSET: int = 12         
DATE_FMT_API: str = "%Y%m%d%H%M"  # format arXiv expects in submittedDate rang
 
# Directories
DOWNLOAD_ROOT: str = "./downloaded_papers"         
MARKDOWN_ROOT: str = "./downloaded_papers_md"  
EMBEDDINGS_ROOT: str = "./downloaded_embeddings"
SUMMARY_PROMPTS_ROOT: str = "./summary_prompts"
SUMMARIES_ROOT: str = "./summarized_articles"
# Chunking
MAX_CHARS: int = 2000
OVERLAP: int = 200
 
# Embedding 
# model has max tokens of 216, and fixed vector size of 384 dimensions
#EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
 
# model has max tokens of 512
#EMB_MODEL = "BAAI/bge-base-en-v1.5"
 
#model with higher max tokens, 8192 tokens. 1024 dimension size
EMB_MODEL = "BAAI/bge-m3"
 
 
#LLM Summarization
#MODEL_ID = "unsloth/Llama-3.2-3B-Instruct"
#MODEL_ID = "llama3.2"
#MODEL_ID = "t5-small"
MODEL_ID = "facebook/bart-large-cnn"
 
 
#Sending emails
 
#SMTP_SERVER = "smtp.gmail.com" or "smtp.comcast.net" or "smtp.office365.com"
SMTP_SERVER = "smtp.gmail.com"
 
SMTP_PORT = 587  # OR 465?
 
USERNAME = "logan.laszewski@gmail.com"
 
PASSWORD = os.getenv("PASSWORD")
 

RECEIVER = "logan.laszewski@gmail.com"