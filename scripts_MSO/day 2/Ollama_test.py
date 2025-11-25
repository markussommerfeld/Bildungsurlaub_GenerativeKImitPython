#%% pakete
import os
from langchain_ollama import ChatOllama
 
# %% Modellinstanz erstellen
model = ChatOllama(model="gemma3:270m")  # Alternativ: "gemma3:2.7b" oder "gemma3:13b"
 
# %% Anfrage ans Modell schicken
user_query = "Wieviele E sind in Erdbeere?"
res = model.invoke(user_query)
 
# %% Ausgabe ansehen
res.model_dump()
 
# %%
from pprint import pprint
pprint(res.content)