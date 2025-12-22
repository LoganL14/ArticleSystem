""" Script to collect pdfs of all of the previous days articles. /downloaded_papers folder"""

""" Packages to download"""
#uses config.py to bring in necessary global arguments
from config import BASE_URL, MAX_RESULTS, search_term
#this lets you extract information from an API
import requests
#work with dates, +/-, etc
from datetime import datetime, timedelta
#function formatting, -> 
from typing import Optional, Tuple
#work with specific timezones
from zoneinfo import ZoneInfo
#to pull from xml request, the data I need (PDFs)
from bs4 import BeautifulSoup
#Representing file and directory paths
from pathlib import Path



def get_utc_times_for_2daysago() -> Tuple[datetime, datetime, str]:
    """Function to get the  time range from midnight to end of day (UTC).
    2 days ago to avoid confusion with UTC time. Later used as a way to filter for specific articles
     Returns:
      tuple: (start_utc, end_utc, day_label)
    """
    # Specify time zone, subtract 2 days off of current day. Replace with 12:00am and 11:59pm of that day
    tz = ZoneInfo("UTC")
    now_utc = datetime.now(tz) - timedelta(days=3)
    yesterday_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_end_utc = now_utc.replace(hour=23, minute=59, second=59, microsecond=0)
    # clean way to look at the day you are looking at
    yday_label = str(yesterday_midnight_utc.date())

    return yesterday_midnight_utc, yesterday_end_utc, yday_label

def build_search_query(yesterday_midnight_utc : datetime, yesterday_end_utc : datetime, search_term=None) -> Tuple[str, str] :
    """Build a search query with date range and other information (optional).

    Args:
        start_utc: Start of day (2 days prior) in UTC
        end_utc: End datetime (2 days prior) in UTC
        search_term: Optional search term (e.g., 'cat:cs.AI' or 'all:technology')

    Returns:
        str: Formatted search query. In a format the API accepts.
    """

    #format the dates for query. 202512170000
    fmt = "%Y%m%d%H%M"
    start_utc_format =  yesterday_midnight_utc.strftime(fmt)
    end_utc_format  =  yesterday_end_utc.strftime(fmt)
    #build the date query. Example - submittedDate:[202512170000 TO 202512180000] 
    date_query = f"submittedDate:[{start_utc_format} TO {end_utc_format}]"
    
    # check if search term is added to create full query. Otherwise, just the date query
    if search_term:
        search_query = f"{search_term} AND {date_query}"
        return search_query, start_utc_format
    else:
        search_query = date_query
    return search_query, start_utc_format



def fetch_papers(search_query: str, paper_date: str):
    """Using search_query, get all (max_results) papers from 2 days ago. 
    Using the result, get PDFs for each one and download locally. 

    Args:
        search_query: The search query string
        paper_date: The date your grabbing from for submitted papers

    Returns:
        Folder full of the articles for this search
    """
    #set up parameters which specify search
    params = {"search_query" : search_query ,
          "max_results" : MAX_RESULTS}
    # send request
    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    #parses the XML string into a navigable tree
    soup = BeautifulSoup(resp.text, "xml")
    #Give me every <link> tag in the entire document
    all_entries = soup.find_all('link')
    # Extracts only those <link>s whose type="application/pdf", returning a list of PDF URLs (https://arxiv.org/pdf/2512.12345v1)
    # i['href'] pulls the URL out of the attribute
    all_href_links = [i['href'] for i in all_entries if i.get('type') == 'application/pdf']
    # Download the papers into specific folder 
    download_folder = Path(f'./downloaded_papers/{paper_date}')
    download_folder.mkdir(parents=True, exist_ok=True)
    #naming each pdf that is downloaded
    downloaded = []
    for url in all_href_links:
        filename = url.split('/')[-1] + '.pdf'
        fp_path = download_folder / filename
        print(f"Attempting to download {filename} to {fp_path}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
    # Dont know what this below does???
            with open(fp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully downloaded: {filename}")
            downloaded.append(str(fp_path))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during download: {e}")
    return downloaded

from docling.document_converter import DocumentConverter





def parse_pdf_to_markdown(fp_path: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(fp_path)
    return result.document.export_to_markdown()


if __name__ == "__main__":

    #Get the dates that will be used to query later
    yesterday_midnight_utc, yesterday_end_utc, yday_label = get_utc_times_for_2daysago()
    #print(yesterday_midnight_utc, yesterday_end_utc, yday_label)

    #Call the function to build the search query
    search_query, start_utc_time = build_search_query(yesterday_midnight_utc, yesterday_end_utc)
    print(search_query, start_utc_time)

    #download the resulting pdfs, store the pdfs in a list "results"
    results = fetch_papers(search_query, start_utc_time)



#     download_folder_md = Path(f'./downloaded_papers_md/{start_utc_time}')
#     download_folder_md.mkdir(parents=True, exist_ok=True)

#     for pdf in results:
#         base = Path(pdf).stem
#         md_path = download_folder_md / f"{base}.md"
#         try:
#             md_text = parse_pdf_to_markdown(pdf)

#         #
#         #
        
#         except Exception as e:
#             print(f"Docling parse failed for {pdf}: {e}")



# for url in all_href_links:
#         filename = url.split('/')[-1] + '.pdf'
#         fp_path = download_folder / filename



""" NOTES """

## each entry has these (resp.text)
 #   <link href="https://arxiv.org/abs/2512.14974v1" rel="alternate" type="text/html"/>
 #   <link href="https://arxiv.org/pdf/2512.14974v1" rel="related" type="application/pdf" title="pdf"/>
## Grab only the <link> tags above (  soup = BeautifulSoup(resp.text, 'xml') -> all_entries = soup.find_all('link')  )
    
## To get only the actual https.  ( all_href_links = [i['href'] for i in all_entries if i.get('type') == 'application/pdf'] )
# 'https://arxiv.org/pdf/2512.15091v1'

## Create the destination folder  (./downloaded_papers/<paper_date> (e.g., ./downloaded_papers/2025-12-18).
#download_folder = Path(f'./downloaded_papers/{paper_date}')    ->   download_folder.mkdir

## Create a local filename for each pdf   ( filename = url.split('/')[-1] + '.pdf' )
# Example: "https://arxiv.org/pdf/2512.12345v1" → "2512.12345v1.pdf"


## Construct the full file path 
# fp_path = download_folder / filename (Result: ./downloaded_papers/<paper_date>/<filename>.)


## Get the content within each url (downladed in chunks)
 #response = requests.get(url, stream=True)

## Opens a file at fp_path in binary write mode ('wb')??
#with open(fp_path, 'wb')


## Understand the rest?

# for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)