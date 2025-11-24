#%% load environment variables  
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
import os
load_dotenv(find_dotenv())

# Test if key available
#os.getenv("GROQ_API_KEY")
#os.getenv("OPEN_ROUTER_API_KEY")
# %% create Groq model
model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPEN_ROUTER_API_KEY"),base_url="https://openrouter.ai/api/v1") #finds automatically this API:, api_key=os.getenv("GROQ_API_KEY")
# %% Anfrage ans model
user_query = "Was ist der Sinn des Lebens?"
response = model.invoke(user_query)
#%%
response.model_dump()
input_tokens = response.model_dump()["usage_metadata"]["input_tokens"]
output_tokens = response.model_dump()["usage_metadata"]["output_tokens"]
total_tokens = response.model_dump()["usage_metadata"]["total_tokens"]
input_cost = 0.3/1e6
output_cost = 2.5/1e6



# %% Ausgabe ansehen
print(response.content)

