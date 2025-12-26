# # For advanced query syntax documentation, see the arXiv API User Manual:
# # https://arxiv.org/help/api/user-manual#query_details

import arxiv

# Construct the default API client. Handle communication with the API
client = arxiv.Client()

# .Search, which will define query. "query" - articles containing the word. "max_results" - when to stop, "sort_by" - date
# query checks - Title , Abstract , Author names , Comments (like “submitted to XYZ conference”)
search = arxiv.Search(
  query = "submittedDate:[202512170000 TO 202512172359]",
  max_results = 10,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

#actually sends the request, returns a "generator" of objects. each result gets one paper (title, summary, authors, published, pdf_url.. )
#generator that will produce arxiv.Result objects when you iterate over it.
# r.title, r.summary, r.authors, r.published, r.entry_id, r.links, r.pdf_url,etc
results = client.results(search)

print([r for r in results])

#for r in results:
    #print(r)







#first learn how to use api
#-gives atom xml response?
# <feed>: The root element for the entire response.
# <entry>: Each paper/article is an entry.
# Inside <entry>:

# <id>: The canonical URL for the paper.
# <title>: The paper’s title.
# <summary>: Abstract.
# <link>: Links to HTML and PDF versions.
# <author>: Repeated for each author.
# <category>: Subject classifications.
# <published> and <updated>: Dates.
# <arxiv:comment> and <arxiv:journal_ref>: Extra metadata.

# url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
#     data = urllib.request.urlopen(url)
#     print(data.read().decode('utf-8'))

#collect all articles (released today)
#query for all articles meeting certain criteria
#then, write program that automatically runs the api (feedparser?)

#first get current gmt 

# Get current time in Los Angeles
# tz = ZoneInfo("America/Los_Angeles")
# now_local = datetime.now(tz)
# yesterday_local = now_local - timedelta(days = 1)
# #print(now_local)


# #convert to UTC time
# start_utc = yesterday_local.astimezone(ZoneInfo("GMT"))
# end_utc   = now_local.astimezone(ZoneInfo("GMT"))
#print(start_utc, end_utc)

import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
base_url = "http://export.arxiv.org/api/query"




tz = ZoneInfo("UTC")
now_utc = datetime.now(tz) - timedelta(days=2)
twodaysago_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
twodaysago_end_utc = now_utc.replace(hour=23, minute=59, second=59, microsecond=0)
# clean way to look at the day you are looking at
yday_label = str(twodaysago_midnight_utc.date())


#format for query
fmt = "%Y%m%d%H%M"
start_utc_formatted =  twodaysago_midnight_utc.strftime(fmt)
end_utc_formatted =  twodaysago_end_utc.strftime(fmt)

time = "submittedDate:[{start_utc_formatted} TO {end_utc_formatted}]"

query = f"all:* AND {time}"
#print(query)
#"all:*+AND+submittedDate:[202512162300+TO+202512172300]"

params = {"search_query" : "submittedDate:[202512170000 TO 202512172359]" ,
          "max_results" : 10}



# Make request using the search query found
def allarticles():
    
    response = requests.get(base_url, params=params)
    print(response.text)
    

allarticles()


