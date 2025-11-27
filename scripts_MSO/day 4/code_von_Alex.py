#%% pakete
import os
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pprint import pprint
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv
from langchain.vectorstores import FAISS


# %% Wikipedia Artikel laden
query = "Serielle Sanierung"


docs = WikipediaLoader(query=query,lang="de", load_max_docs=5).load()
len(docs)


# %%
for doc in docs:
    print(doc.metadata["title"])
    print(doc.page_content[0:500])
    print("-----")
 
#%% Text in kleinere Abschnitte splitten
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
docs_splitted = splitter.split_documents(docs)
docs_splitted
# %%
pprint(docs_splitted[0].page_content[0:500], width=50)


#%% Problem: docs_splitted [Document(), ...] # was wir brauchen ist [str, str, ...]
docs_splitted_texts = [doc.page_content for doc in docs_splitted]


# %% Embeddings Modell laden


load_dotenv(find_dotenv())
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
# %% Embeddings für alle Texte erstellen
embeddings = []
for i, doc in enumerate(docs_splitted_texts):
    print(i)
    embedding = embedding_model.embed_query(doc)
    embeddings.append(embedding)
#%% Embeddings und Texte paaren


text_embedding_pairs = zip(docs_splitted_texts, embeddings)


#%% Vector DB erstellen
vectordb = FAISS.from_embeddings(text_embedding_pairs, embedding_model)
 
# %% Vector DB
vectordb.save_local(folder_path="serSanierung_wiki")
 
#%% Retriever aufsetzen
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
 
# %% Datenbank abfragen
res = retriever.invoke(input="was ist ein Löffel?")
# %%
for doc in res:
    print(doc.page_content)
    print("-"*20)
# %%