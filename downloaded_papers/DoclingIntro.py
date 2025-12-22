#Can efficiently and correctly extract information from pdfs

#Does this all on CPU which means you can avoid costs from using GPU

#How to extract strcutred data from documentation you have

#pip install docling (added to the .toml file as a dependency)



#TEST USING DOCLING 

from docling.document_converter import DocumentConverter


source = "downloaded_papers/202512190000/2512.17136v1.pdf"


converter = DocumentConverter()

result = converter.convert(source)

print(result.document.export_to_markdown())
#print(result.document.export_to_dict())


