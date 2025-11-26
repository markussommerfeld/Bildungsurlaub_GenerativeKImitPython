#%% 1. Ladet 10 artikel direkt von Wikipedia zum Thema "Künstliche Intelligenz" herunter und speichert sie in einer Liste von Dokumenten.

from langchain_community.document_loaders import WikipediaLoader
docs = WikipediaLoader(query="Superintelligenz", lang="de", load_max_docs=10).load()
len(docs)
 
for i in range(len(docs)):
    doc = docs[i]
    print(f"{i+1}. Page metadata: {doc.metadata}")
    text_preview = (doc.page_content or "").strip().replace("\n", " ")
    print("500 chars:", text_preview[:500])



#%% 2. Ladet eine Webseite direkt ueber das entsprechnde Paket herunter. 

from langchain_community.document_loaders import WebBaseLoader
loader_multiple_pages = WebBaseLoader(
    ["https://www.example.com/", "https://google.com"]
)
docs = loader_multiple_pages.load()
 
for i in range(len(docs)):
    doc = docs[i]
    print(f"{i+1}. Page metadata: {doc.metadata}")
    text_preview = (doc.page_content or "").strip().replace("\n", " ")
    print("500 chars:", text_preview[:500])
# %%