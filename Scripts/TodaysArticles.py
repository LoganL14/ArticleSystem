import arxiv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# big_slow_client = arxiv.Client(
#   page_size = 1000,
#   delay_seconds = 10.0,
#   num_retries = 5
# )


client = arxiv.Client()


# The API provides one date filter, submittedDate, that allow you to select data within a given date range of when the data was submitted to arXiv. 
# The expected format is [YYYYMMDDTTTT+TO+YYYYMMDDTTTT] were the TTTT is provided in 24 hour time to the minute, in GMT. 
# We could construct the following query using submittedDate.

#submittedDate is the searchable metadata field in the arXiv API query syntax.
#published is the Atom feed element returned in the API response.


#from 2025-12-16 00:00 UTC to 2025-12-17 23:59 UTC
#CHANGE TO DIFFERENT TIME ZONE?


# Get current time in Los Angeles
tz = ZoneInfo("America/Los_Angeles")
now_local = datetime.now(tz)
yesterday_local = now_local - timedelta(days = 1)
#print(now_local)


#convert to UTC time
start_utc = yesterday_local.astimezone(ZoneInfo("GMT"))
end_utc   = now_local.astimezone(ZoneInfo("GMT"))
#print(start_utc, end_utc)


#format for query
fmt = "%Y%m%d%H%M"
start_utc_formatted =  start_utc.strftime(fmt)
end_utc_formatted =  end_utc.strftime(fmt)

time = f"submittedDate:[{start_utc_formatted} TO {end_utc_formatted}]"

query = f"all:data AND {time}"
#print(query)

search = arxiv.Search(
    query= query,
    max_results=10,
    sort_by= arxiv.SortCriterion.SubmittedDate)


results = client.results(search)
for r in results:
   print(results)