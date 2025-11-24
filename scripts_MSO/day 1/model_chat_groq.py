#%% load environment variables  
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
import os
load_dotenv(find_dotenv())

# Test if key available
#os.getenv("GROQ_API_KEY")
#os.getenv("OPEN_ROUTER_API_KEY")
# %% create Groq model
model = ChatGroq(model="openai/gpt-oss-120b") #finds automatically this API:, api_key=os.getenv("GROQ_API_KEY")
# %% Anfrage ans model
user_query = "Was ist der Sinn des Lebens?"
response = model.invoke(user_query)

# %% Ausgabe ansehen
print(response.content)
# response.model_dump()