import requests


BASE_URL = "https://export.arxiv.org/api/query"



params = {'search_query': 'all:Physics AND submittedDate:[202512180800 TO 202512182001]', 'max_results': 50}


resp = requests.get(BASE_URL, params=params, timeout=60)
print(resp.text)