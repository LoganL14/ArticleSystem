# take each .npy file I have (which holds chunks for a specific article)
#find the "average embedding" mean(all_chunk_embeddings)
#compute similarity between each chunk embedding and the paper centroid 
#select top-k chunks 
#summarize these selected chunks (only feed these into the LLM)
#have a set prompt to give like ("summarize the key methods and findings from the following excerpts of a research paper")

#loop through and do this for each .npy file I have? leading to short summary for each unique article?


