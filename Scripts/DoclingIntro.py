#Can efficiently and correctly extract information from pdfs

#Does this all on CPU which means you can avoid costs from using GPU

#How to extract strcutred data from documentation you have

#pip install docling (added to the .toml file as a dependency)



#TEST USING DOCLING 

from docling.document_converter import DocumentConverter
from pathlib import Path
import requests


# source = "downloaded_papers/202512190000/2512.17136v1.pdf"


# converter = DocumentConverter()

# result = converter.convert(source)

# print(result.document.export_to_markdown())
# #print(result.document.export_to_dict())


start_utc_time = "202512190000"
pdf_path = "downloaded_papers/202512190000/2512.17136v1.pdf"
download_folder_md = Path(f'./TEST_downloaded_papers_md/{start_utc_time}')
download_folder_md.mkdir(parents=True, exist_ok=True)

base = Path(pdf_path).stem
md_path = download_folder_md / f"{base}.md"

converter = DocumentConverter()
result = converter.convert(pdf_path)
md_text = result.document.export_to_markdown()                 

try: 
    md_path.write_text(md_text, encoding="utf-8")
    print(f"✅ Saved Markdown: {md_path}")

except Exception as e:
        print(f"Failed to save Markdown for {pdf_path}: {e}")





# with open(md_path, 'wb') as f:
#         for chunk in md_text.iter_content(chunk_size=8192):
#             if chunk:
#                 f.write(chunk)
#     print(f"Successfully downloaded: {md_text}")