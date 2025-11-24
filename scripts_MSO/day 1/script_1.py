#%% load environment variables  
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

os.getenv("GROQ_API_KEY")