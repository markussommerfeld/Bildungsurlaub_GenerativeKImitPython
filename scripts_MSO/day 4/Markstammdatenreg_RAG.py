#%%
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from pprint import pprint
from langchain.document_loaders import TextLoader
import pandas as pd 
import csv
from langchain.schema import Document
 
#%% TODO TableRAG in scripts M07 fuer strukturierte Datein versuchen
# das ist der bessere Ansatz fuer Strukturierte Daten
# mit SQL kann man auch diese Queries nutzen

data = csv_to_langchain_documents('Wind_MVP.csv', content_column='text')
 
 
 
#%%

loader = CSVLoader(file_path="Wind_MVP.csv")

data = loader.load()

print(data)

#%% This code creates a list of all entries of the CSV
# # doesn't work atm
# from langchain_core.documents import Document
# all_docs = []

# for row in range(data.shape[0]):
#     for key in list(data.keys()):
#     #Document(page_content=row["feld]..., )
#     #MaStR-Nr. der Einheit	Anzeige-Name der Einheit	Betriebs-Status	Inbetriebnahmedatum der Einheit	Registrierungsdatum der Einheit	Energieträger	Bruttoleistung der Einheit	Nettonennleistung der Einheit	Postleitzahl	Ort	Name des Anlagenbetreibers (nur Org.)	"	MaStR-Nr. des Anlagenbetreibers"	Letzte Aktualisierung
#         print(data.iloc[row][key])

#         # current_doc=Document(page_content=data.iloc[row][key])
#         # all_docs.append(current_doc)

# # koennte auch von Hand selbst machen:
# #from langchain_core.documents import Document
 
# #my_document = Document(     page_content=content,     metadata=meta_data )
 
#%%
from langchain_ollama.embeddings import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model="embeddinggemma:300m")
# docs_splitted_texts = [doc.page_content for doc in docs_splitted]
# len(docs_splitted_texts)

docs_splitted = [doc for doc in data] 

#%% data storing

from langchain.vectorstores import FAISS
# hier Faiss ist nur in Arbeitsspeicher, nicht persistent
vector_store = FAISS.from_documents(docs_splitted, embedding_model)
#vector_db = FAISS.from_embeddings(docs_splitted)

#%% inspect vector store
print(f"Number of vectors in the store: {vector_store.index.ntotal}")  
# save vector DB
vector_store.save_local(folder_path="Markstammdatenregister")


 
#%% Retriever aufsetzen
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
 
# %% Datenbank abfragen
res = retriever.invoke(input="Gib mir Ergenisse mit dem Datum: 20.09.2024")
# %%
for doc in res:
    print(doc.page_content)
    print("-"*20)
 

#%% RAG function 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
def my_rag(query: str, k: int=3, llm_model: str="gemma3:4b") -> str:
    # return the best k (3) answers
    # retriever
    # der Retriever embedded die Anfrage und sucht in der Vektordatenbank nach den k ähnlichsten Dokumenten
    embedding_model = OllamaEmbeddings(model="embeddinggemma")
    vectordb = FAISS.load_local(folder_path="Markstammdatenregister", embeddings=embedding_model, allow_dangerous_deserialization=True)
    
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    res = retriever.invoke(input=query)
    
    # augmentation
    # gegeben: [Document, ...], gesucht [str, str, ...] -> str "context: ...; context: ..."
    # Augmentation bedeutet hier, dass die gefundenen Dokumente in einen einzigen String umgewandelt werden
    res_list_str = [doc.page_content for doc in res]
    context_infos = "; context: ".join(res_list_str)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Du bist ein freundlicher Assistent, der Fragen beantwortet.
        Dir werden Kontextinformationen bereitgestellt und du beantwortest die Frage des Nutzers ausschließlich auf Basis der Kontextinfos."""),
        ("user", "Frage: {question}; Kontextinformationen: {context_infos}")
    ])# Antworte kurz und bündig und in der Sprache in der die Frage gestellt wurde.
    
    # generation
    model = ChatOllama(model=llm_model)
    
    # chain
    chain = prompt_template | model | StrOutputParser()
    rag_out = chain.invoke({"question": query, "context_infos": context_infos})
    pprint(rag_out)
    
    

#%% test RAG function
query = "Gibt mir alle Parks mit Inbetriebnahmedatum vor 2020"

my_rag(query=query, k=2, llm_model="gemma3:4b")
