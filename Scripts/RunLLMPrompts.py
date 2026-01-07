""" Take the "summary prompts" for each article, and run them through a open source LLM to get article summaries """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARIES_ROOT, SUMMARY_PROMPTS_ROOT, MODEL_ID, TEMPERATURE, MAX_NEW_TOKENS, API_KEY
from context import ctx
import ollama
from groq import Groq

def get_prompt_files(start_utc_time: str) -> List[str]:
    """ Pull the current summary prompt files """

    prompt_folder = Path(SUMMARY_PROMPTS_ROOT) / start_utc_time
    return[str(p) for p in prompt_folder.glob("*")]


def load_prompt_file(prompt_file: str):
    """ Read the Markdown files """
    
    return Path(prompt_file).read_text(encoding="utf-8")


if __name__ == "__main__":

    client = Groq(api_key = API_KEY)

    prompt_files = get_prompt_files(ctx.start_utc_time)

    #create folder path for these generated article summaries
    summary_folder = Path(SUMMARIES_ROOT) / ctx.start_utc_time
    summary_folder.mkdir(parents=True, exist_ok=True)

    for prompt_file in prompt_files:
        
        #save the article summaries somewhere
        base = Path(prompt_file).stem
        summary_file = summary_folder / f"{base}.txt"

        prompt_text = load_prompt_file(prompt_file)

        chat_completion = client.chat.completions.create(
            model= MODEL_ID,
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )

        # response = ollama.chat(
        #     model= MODEL_ID,
        #     messages=[
        #         {"role": "user", "content": prompt_text}],        
        #     options={
        #         "temperature": TEMPERATURE,
        #         "num_predict": MAX_NEW_TOKENS
        #     }   
        # )
        
        #save the summary to a text file
        summary_file.write_text(chat_completion.choices[0].message.content, encoding="utf-8")
        print(f"Wrote: {summary_file}")
