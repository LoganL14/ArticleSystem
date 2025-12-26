#NOW CREATE EMBEDDINGS 
# try MiniLM-L6-v2
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


emb_model = HuggingFaceBgeEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2" )
result = emb_model.embed_query("This is a test application")
print(result)