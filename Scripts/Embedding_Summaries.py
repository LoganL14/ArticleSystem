""" Script to take embeddings for each article, find centroid (mean) embedding for each article. 
Then find the closest embeddings - embeddings that best represent the articles theme.
Finally fill a prompt template with each articles "top" embeddings and save the summary prompts that LLM will use. """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARY_ROOT, EMBEDDINGS_ROOT
#used for embedding / vector use
import numpy as np

import json
from context import ctx

#REMOVE CAUSE OF CONTEXT.PY
# def get_start_utc_time() -> str:
#     """ Recompute the same date window for reference """
#     twodaysago_midnight_utc, twodaysago_end_utc, yday_label = get_utc_times_for_2daysago()
#     search_query, start_utc_time = build_search_query(twodaysago_midnight_utc, twodaysago_end_utc)  # you can ignore `_query` here
#     return start_utc_time


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



def get_top5_embeddings(embed_file: str) -> list[tuple[int,float]]:
    
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


def save_summary_prompt(prompt: str, article_id: str, start_utc_time: str):
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

    embed_files = get_embed_files(ctx.start_utc_time)
    meta_files = get_meta_files(ctx.start_utc_time)

    for embed_file in embed_files:
        
        top5 = get_top5_embeddings(embed_file)
        meta_file = str(Path(embed_file).parent / (Path(embed_file).stem.replace('_vectors', '') + '.jsonl'))
        texts = top_texts(meta_file, top5)
        article_id = Path(embed_file).stem.replace('_vectors', '')
        prompt = make_prompt(article_id, texts)
        save_summary_prompt(prompt, article_id, ctx.start_utc_time)