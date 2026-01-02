""" Take the "summary prompts" for each article, and run them through a open source LLM to get article summaries """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARY_ROOT, MODEL_ID

from context import ctx
import requests

from transformers import AutoModelForCausalLM, AutoTokenizer


def get_prompt_files(start_utc_time: str) -> List[str]:
    """  Pull the current summary prompt files """

    prompt_folder = Path(SUMMARY_ROOT) / start_utc_time
    return[str(p) for p in prompt_folder.glob("*")]


def load_prompt_file(prompt_file: str):
    """Read the Markdown files """
    return Path(prompt_file).read_text(encoding="utf-8")



# def summarize_article(prompt_text: str):
#     response = requests.post("",
#             json = {
#                     "model": "",
#                     "prompt": prompt_text,
#                     "stream": False
                                 
#                              })
#     return response.json()["response"]



if __name__ == "__main__":

    #load the tokenizer which will convert the prompt into tokens (Each model family has own special tokens)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    #actually loads the model (neural net). This AutoModelForCausalLM is specifically for text generation
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

    prompt_files = get_prompt_files(ctx.start_utc_time)

    for prompt_file in prompt_files:
        
        prompt_text = load_prompt_file(prompt_file)
        
        #runs the tokenizer on my input, meaning each "prompt_text".  Encodes the prompt string into PyTorch tensors, moves to same device
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        
        #runs the model, use the input, producing new token IDs
        output = model.generate(**inputs, max_new_tokens=600)
       
        #turns the output, tokenIDs, into actual text
        summary = tokenizer.decode(output[0], skip_special_tokens=True)

        print(f"\nSummary for {prompt_file}:\n{summary}\n")
