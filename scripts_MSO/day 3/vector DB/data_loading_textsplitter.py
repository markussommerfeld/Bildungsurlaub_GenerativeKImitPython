#%% import pakete 
from langchain.document_loaders import TextLoader
import os
from pprint import pprint
import seaborn as sns
# Get the current file path to change directory so we always have the correct path
# regardless of where we run the script from
os.path.abspath(__file__)
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

file_path_txt = os.path.join(current_dir, 'frankenstein.txt')
#file_path_txt

#alternatively 
# os.getcwd()
# os.chdir(Path(__file__).resolve().parent)
# print("Working directory:", Path.cwd())

#%% load data
loader = TextLoader(file_path_txt, encoding='utf8')
docs = loader.load()

# inspect data
print(f'Number of documents: {len(docs)}')
print(f'First document content: {docs[0].page_content[:500]}...')  # print first 500 characters
print(f'First document metadata: {docs[0].metadata}')

#%% load all files in a directory
from langchain.document_loaders import DirectoryLoader

loader_dir = DirectoryLoader(current_dir, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding':'utf8'})
docs_dir = loader_dir.load()
# glob = "*.txt"  # only load .txt files
# glob = "*"       # load all files
# glob = "**/*.txt" # load all .txt files recursively in subdirectories


print(f'Number of documents in directory: {len(docs_dir)}')
print(f'First document in directory content: {docs_dir[1].page_content[5300:5500]}...')  # print first 500 characters
print(f'First document in directory metadata: {docs_dir[1].metadata}')

#%% text splitter
#from langchain_text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
#1. splitter with fixe chunk size
splitter = characterTextSplitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs_splitted = splitter.split_documents(docs_dir)
len(docs_splitted)

pprint(docs_splitted[1000].page_content[:500])


#%% recursive text splitter
# This is the preferred method for text splitting and the standard
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200,
    separators=["\n\n"]#, "\n", " ", ""]
)
# 2. splitter with recursive strategy
docs_splitted = text_splitter.split_documents(docs_dir)
len(docs_splitted)

pprint(docs_splitted[1000].metadata)
pprint(docs_splitted[1000].page_content[:500])

#%% get chunk size statistics

[len(doc.page_content) for doc in docs_splitted] 

sns.histplot([len(doc.page_content) for doc in docs_splitted], bins=30)

#%% embedding model
# 1. locally hosted model

from langchain_ollama.embeddings import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model="embeddinggemma:300m")
docs_split_texts = [doc.page_content for doc in docs_splitted]

embeddings = embedding_model.embed_documents(docs_split_texts[:2])
#%%
len(embeddings), len(embeddings[0])
pprint(embeddings[0][:10])  # print first 10 dimensions of the first embedding