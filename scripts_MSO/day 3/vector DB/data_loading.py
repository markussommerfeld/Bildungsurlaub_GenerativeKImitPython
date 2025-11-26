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

#%% load different file types
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

def select_loader(file_path):
    _, file_extension = os.path.splitext(file_path)
    # format to lower case to ensure case insensitivity
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        #pass: this is just a placeholder when coding an if statement without any action
        return TextLoader(file_path, encoding='utf8')
    elif file_extension == '.pdf':
        return PyMuPDF4LLMLoader(file_path, mode='page')
        # mode literal: single, page (siehe MIRO board)
        # mode single: entire document as one page
        # mode page: each page as separate document)
    else:
        #raise ValueError(f"Unsupported file type: {file_extension}")
        return None
    
    
loader_all = DirectoryLoader(current_dir, glob="**/*",exclude = "*.py", loader_cls=select_loader,
                show_progress=True, 
                use_multithreading=True)
docs_all = loader_all.load()
print(f'Number of documents in directory with different file types: {len(docs_all)}')

# THIS IS FOR THE SPECIAL CASE THAT THE PDF CONTAINS IMAGES WITH TEXT
# If you do not know, first try detect as txt and if that is empty, try OCR

#text recognition in images (OCR) can be added with additional libraries such as pytesseract or easyocr
#however, this is not implemented in langchain yet as of June 2024
# install Poppler for Windows, Add to PATH or set POPPLER_PATH
# Install Tesseract OCR and add optionally set: TESSERACT_CMD
# Python deps: pip install: pdf2image, pytesseract
