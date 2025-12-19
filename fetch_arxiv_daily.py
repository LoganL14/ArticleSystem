import requests
from datetime import datetime, timedelta
from typing import Optional, Tuple
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://export.arxiv.org/api/query"
MAX_RESULTS = 50
search_term = "all:Technology"



def get_utc_times_for_yesterday() -> Tuple[datetime, datetime, str]:
    """Function to get the todays time range from midnight to current (UTC).
     Returns: 
      tuple: (start_utc, end_utc, day_label) 
    """

    tz = ZoneInfo("UTC")
    now_utc = datetime.now(tz) - timedelta(days=2)
    yesterday_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_end_utc = now_utc.replace(hour=23, minute=59, second=59, microsecond=0)

    yday_label = str(yesterday_midnight_utc.date())
    
    return yesterday_midnight_utc, yesterday_end_utc, yday_label

def build_date_query(yesterday_midnight_utc : datetime, yesterday_end_utc : datetime, search_term=None) -> str:
    """Build an arXiv search query with date range.
    
    Args:
        start_utc: Start datetime in UTC
        end_utc: End datetime in UTC
        search_term: Optional search term (e.g., 'cat:cs.AI' or 'all:technology')
    
    Returns:
        str: Formatted search query. In a format the API accepts. 
        For example - submittedDate:[202512170800 TO 202512180010]
    """

    #format for query
    fmt = "%Y%m%d%H%M"
    start_utc_format =  yesterday_midnight_utc.strftime(fmt)
    end_utc_format  =  yesterday_end_utc.strftime(fmt)

    date_query = f"submittedDate:[{start_utc_format} TO {end_utc_format}]"
    
    if search_term:
        search_query = f"{search_term} AND {date_query}"
        return search_query
    else:
        search_query = date_query
    return search_query



def fetch_feed(search_query) -> requests.Response:
    """Fetch results from arXiv API.
    
    Args:
        search_query: The search query string
        max_results: Maximum number of results to return
    
    Returns:
        requests.Response object
    """
    
    params = {"search_query" : search_query ,
          "max_results" : MAX_RESULTS} 
    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'xml')
    all_links = soup.find_all("link")
    #print(all_links)
    all_href_links = [i["href"] for i in all_links if i.get("type") == 'application/pdf']
    print(all_href_links)
    # downloaded_path = Path('./downloaded_papers').mkdir(parents =True , exisr_ok =True )
    # for url in downloaded_path:
    #     filename = url.split("/")[-1] + '.pdf'
    #     fp_path = downloaded_path / filename

    #     print(f"Attempting to download {filename} to {fp_path}...")

    #     try:
    #         response = 


# #how to save this somewhere?
# def save_csv(): 




if __name__ == "__main__":
    
    # Build the time range for 'today so far'
    yesterday_midnight_utc, yesterday_end_utc, yday_label = get_utc_times_for_yesterday()
    print(yesterday_midnight_utc)
    #print(yesterday_midnight_utc, yesterday_end_utc, yday_label)

    #Build actual search query
    search_query = build_date_query(yesterday_midnight_utc, yesterday_end_utc)
    #print(search_query)
    #, search_term = "all:Physics"



#get actual result from query. How do i want to return this?
    results = fetch_feed(search_query)
    print(results)



#  params = {"search_query" :  all:tech AND submittedDate:[202512180800 TO 202512181702]
#            "max_results" : MAX_RESULTS} 
#      resp = requests.get(BASE_URL, params=params, timeout=60)
#      print(resp.text)



#submittedDate:[202512162330 TO 202512172330]