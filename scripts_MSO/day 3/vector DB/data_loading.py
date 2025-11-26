#%% import pakete 
from langchain.document_loaders import TextLoader
import os
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

# %% inspect data
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