""" Take the "summary prompts" for each article, and run them through a open source LLM to get article summaries """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARIES_ROOT, SUMMARY_PROMPTS_ROOT, MODEL_ID

import time
from context import ctx
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_prompt_files(start_utc_time: str) -> List[str]:
    """ Pull the current summary prompt files """

    prompt_folder = Path(SUMMARY_PROMPTS_ROOT) / start_utc_time
    return[str(p) for p in prompt_folder.glob("*")]


def load_prompt_file(prompt_file: str):
    """ Read the Markdown files """
    
    return Path(prompt_file).read_text(encoding="utf-8")


if __name__ == "__main__":

    # #load the tokenizer which will convert the prompt into tokens (Each model family has own special tokens)
    # tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    # #actually loads the model (neural net). This AutoModelForCausalLM is specifically for text generation
    # model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto")

    # prompt_files = get_prompt_files(ctx.start_utc_time)[:2] # Testing first 2 only

    # #create folder path for these generated article summaries
    # summary_folder = Path(SUMMARIES_ROOT) / ctx.start_utc_time
    # summary_folder.mkdir(parents=True, exist_ok=True)

    # for prompt_file in prompt_files:
        
    #     #save the article summaries somewhere
    #     base = Path(prompt_file).stem
    #     #print(base)
    #     summary_file = summary_folder / f"{base}.txt"

    #     prompt_text = load_prompt_file(prompt_file)

    #     #runs the tokenizer on my input, meaning each "prompt_text".  Encodes the prompt string into PyTorch tensors, moves to same device
    #     inputs = tokenizer(prompt_text, return_tensors="pt")

    #     #runs the model, use the input, producing new token IDs
    #     output = model.generate(**inputs, max_new_tokens=100, do_sample=False)
       
    #     #turns the output, tokenIDs, into actual text
    #     #summary = tokenizer.decode(output[0, prompt_len:], skip_special_tokens=True)
    #     summary = f"Article Summary for {base}\n\n(placeholder summary text)"
      
    #     #save the summary to a text file
    #     summary_file.write_text(summary, encoding="utf-8")
    #     print(f"Wrote: {summary_file}")