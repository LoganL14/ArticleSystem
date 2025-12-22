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

import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
base_url = "http://export.arxiv.org/api/query"


#first get current gmt 

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

time = "submittedDate:[{start_utc_formatted} TO {end_utc_formatted}]"

query = f"all:* AND {time}"
#print(query)
#"all:*+AND+submittedDate:[202512162300+TO+202512172300]"

params = {"search_query" : "submittedDate:[202512170000 TO 202512172359]" ,
          "max_results" : 10}
# AND submittedDate:[202512160800 TO 202512172330"
def allarticles():
    
    response = requests.get(base_url, params=params)
    print(response.text)
    
    #return response
    #print(response.text)


allarticles()


#submittedDate:[202512180800 TO 202512182332]