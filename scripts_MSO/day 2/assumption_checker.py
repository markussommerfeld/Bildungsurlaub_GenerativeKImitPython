#%%
from groq import Groq
import base64
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv(find_dotenv())

# Create a LANGSMITH_API_KEY in Settings > API Keys
from langsmith import Client
client = Client() # wenn hier API key vorhanden dann kann man eigene Fragen hochladen
pompt_template = client.pull_prompt("jgwill/assumption-checker", include_model=True)
pompt_template

model = ChatGroq(model="openai/gpt-oss-120b")
chain = pompt_template | model
res = chain.invoke({"question": "Wie alt kann der Mensch werden?"})

#print(res.content)
console = Console()
console.print(Markdown(res.content))



##%% Das hier ist copy paste von Bert und seinem API key, die zu .env hinzugefuegt werden muss.
#%% pakete
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from langsmith import Client
hub_client = Client()
# %% Prompt Template
prompt_template = hub_client.pull_prompt("jgwill/assumption-checker", include_model=True)
prompt_template
# %% Modellinstanz erstellen
model = ChatGroq(model="openai/gpt-oss-120b")
 
#%% chain
chain = prompt_template | model | StrOutputParser()
 
#%%
question = "Wie alt kann der Mensch werden?"
res = chain.invoke({"question": question})
# %%
from rich.markdown import Markdown
from rich.console import Console
console = Console()
console.print(Markdown(res), width=50)
 
#%% save prompt to LangChain Hub
hub_client.push_prompt(prompt_identifier="my_copy_of_assumption_checker", object=prompt_template, description="My copy of the assumption checker prompt", is_public=True)
# %%
 
 