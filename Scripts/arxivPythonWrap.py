# # For advanced query syntax documentation, see the arXiv API User Manual:
# # https://arxiv.org/help/api/user-manual#query_details

import arxiv

# Construct the default API client. Handle communication with the API
client = arxiv.Client()

# .Search, which will define query. "query" - articles containing the word. "max_results" - when to stop, "sort_by" - date
# query checks - Title , Abstract , Author names , Comments (like “submitted to XYZ conference”)
search = arxiv.Search(
  query = "quantum",
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



