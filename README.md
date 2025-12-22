# Automating the collection of Arxiv Articles (pdfs), embedding model to summarize, and send scheduled emails to AI team

## Overview
This project automates the collection of scientific articles from https://arxiv.org, summarizes them using an embedding model, and sends scheduled email updates to the AI team. The goal is to provide concise daily summaries of relevant research in AI, technology, and related fields.

## Project Steps

### Article Collection
- Query arXiv API for articles from two days ago (UTC).
- Parse XML response using BeautifulSoup.
- Extract PDF links and download articles into a structured folder system.

### Processing & Summarization
- Parse PDFs using tools like Docling or similar.
- Chunk text with LangChain.
- Generate embeddings and summaries using an appropriate model.

### Email Workflow
- Automate sending summarized articles via email to the AI team.
- Schedule tasks for daily execution.


## Tech Stack
- Python (requests, BeautifulSoup, pathlib, zoneinfo)
- LangChain for chunking and embeddings
- Airflow or similar for scheduling
- Git/GitHub for version control



### Full Pipeline 
1) Finds new arXiv papers (from two days ago, UTC).
2) Downloads their PDFs into an organized folder structure.
3) Extracts clean text from those PDFs.
4) Chunks the text, then creates embeddings and summaries.
5) Sends a daily email to team with specifics (titles, abstracts, links, and short summaries).
6) Runs on a schedule (daily).