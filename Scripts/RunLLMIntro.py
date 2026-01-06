#Take the "summary prompts" for each article, and run them through a open source LLM to get article summaries """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARIES_ROOT, SUMMARY_PROMPTS_ROOT,  MODEL_ID

import time
from context import ctx
from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModelForSeq2SeqLM
import requests
import json




# prompt = "Summarize this: The quick brown fox jumps over the lazy dog."

# def summarize_with_ollama(prompt):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": MODEL_ID, "prompt" : prompt, "stream": False, "max_tokens": 50})
#     print(json.dumps(response.json(), indent=2))

# summarize_with_ollama(prompt)


#load the tokenizer which will convert the prompt into tokens (Each model family has own special tokens)
print("Loading tokenizer")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
print("tokenizer loaded")

#actually loads the model (neural net). This AutoModelForCausalLM is specifically for text generation
print("Loading Model")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, device_map="auto")
print("Model Loaded")

prompt_text = "Summarize this: The quick brown fox jumps over the lazy dog."
        
#runs the tokenizer on my input, meaning each "prompt_text".  Encodes the prompt string into PyTorch tensors, moves to same device
print("Tokenizing prompt")
inputs = tokenizer(prompt_text, return_tensors="pt")
prompt_len = inputs["input_ids"].shape[1]
print(inputs)
print("Prompt tokenized")

#runs the model, use the input, producing new token IDs
print("Generating summary")
output = model.generate(**inputs, max_new_tokens=50, do_sample=False)
print("Summary generated")
    
#turns the output, tokenIDs, into actual text
summary = tokenizer.decode(output[0], skip_special_tokens=True)
print(summary)



# AutoTokenizer - Class that determines how text is split into tokens for a specific model.

# AutoModelForCausalLM - Class for loading correct model architecture for (text generation).
# Causal Language Modeling (CLM) - Predicts the next token in a sequence, given all previous tokens.

# AutoTokenizer.from_pretrained() - Loads in pre-trained model and tokenizer weights.
# tokenizer() - converts input text into tokens the model can understand.
# model.generate() - Generates new tokens based on input tokens. (runs model)
# tokenizer.decode() - Converts generated tokens back into human-readable text.