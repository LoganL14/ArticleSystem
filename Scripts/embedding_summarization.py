# take each .npy file I have (which holds chunks for a specific article)
#find the "average embedding" mean(all_chunk_embeddings)
#compute similarity between each chunk embedding and the paper centroid 
#select top-k chunks 
#summarize these selected chunks (only feed these into the LLM)
#have a set prompt to give like ("summarize the key methods and findings from the following excerpts of a research paper")

#loop through and do this for each .npy file I have? leading to short summary for each unique article?

#shouldnt need similiarity search for this method... as even if there are 100 articles a day (50 chunks each), only 5,000 vectors


#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import get_utc_times_for_2daysago, build_search_query
#function formatting, ->
from typing import List, Dict
#uses config.py to bring in necessary global arguments
from config import SUMMARY_ROOT, EMBEDDINGS_ROOT
#used for embedding / vector use
import numpy as np
import json


def get_start_utc_time() -> str:
    """ Recompute the same date window for reference """
    twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
    search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
    return start_utc_time


def get_embed_files(start_utc_time: str) -> List[str]:
    """  Pull the current embeddding files (.npy) """
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.npy")]


def get_meta_files(start_utc_time: str) -> List[str]:
    """  Pull the current embeddding metadata files (.jsonl) """
    embed_folder = Path(EMBEDDINGS_ROOT) / start_utc_time
    return [str(p) for p in embed_folder.glob("*.jsonl")]


def load_embedding(embed_file: str) -> np.ndarray:
    """Read the embedding npy files into numpy arrays """
    return np.load(embed_file)


def load_meta_file(meta_file: str):
    with open(meta_file, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

####################

def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))



def get_top5_embeddings(embed_file: str):
    
    embeddings = load_embedding(embed_file)
    centroid = embeddings.mean(axis = 0)

    scores = []
    for i, emb in enumerate(embeddings):
        score = cosine_similarity(emb, centroid)
        scores.append((i, score))

    top5 = sorted(scores, key=lambda x:x[1], reverse= True)[:5]
    return top5

def top_texts(meta_file: str, top5: list[tuple[int,float]]) -> list[str]:
    meta = load_meta_file(meta_file)
    texts = []
    for idx, _ in top5:
        texts.append(meta[idx].get("chunk_text", ""))
    return texts

    ###################

def make_prompt(article_id: str, top_texts: list[str]) -> str:
    prompt = f"Summarize the following article ({article_id}) based on these key passages. Start response with something signifying your summarizing an article:\n\n"
    for i, text in enumerate(top_texts, 1):
        prompt += f"Passage {i}:\n{text.strip()}\n\n"
    prompt += "Provide a concise summary of the article."
    return prompt

##########################


def save_summary_prompt(prompt: str):
    summary_prompt_folder = Path(SUMMARY_ROOT) / start_utc_time
    summary_prompt_folder.mkdir(parents=True,exist_ok=True)
    base = article_id
    prompt_path = summary_prompt_folder / f"{base}.md"
    
    try:
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"Saved Markdown: {prompt_path}")
    except Exception as e:
            print(f"Failed to save Markdown for {prompt_path}: {e}")
    

if __name__ == "__main__":

    start_utc_time = get_start_utc_time()
    embed_files = get_embed_files(start_utc_time)
    meta_files = get_meta_files(start_utc_time)
    print(meta_files)

    for embed_file in embed_files:
        
        top5 = get_top5_embeddings(embed_file)
        meta_file = str(Path(embed_file).parent / (Path(embed_file).stem.replace('_vectors', '') + '.jsonl'))  # match file   
        texts = top_texts(meta_file, top5)
        article_id = Path(embed_file).stem.replace('_vectors', '')
        
        # print("article:", article_id)
        # print("top5 idx:", [i for i, _ in top5])
        # meta = load_meta_file(meta_file)
        # print("meta rows:", len(meta))
        # print("sample keys:", list(meta[0].keys()) if meta else [])
        # empty_count = sum(1 for idx, _ in top5 if not meta[idx].get("chunk_text", "").strip())
        # print(f"empty passages in top5: {empty_count}")

        prompt = make_prompt(article_id, texts)
        save_summary_prompt(prompt)


    #     ###########