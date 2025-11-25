#%% pakete
import os
from langchain_ollama import ChatOllama
 
# %% Modellinstanz erstellen
model = ChatOllama(model="gemma3:4b")
 
# %% Anfrage ans Modell schicken
user_query = "Was ist der beste 17 Zoll Monitor?"
res = model.invoke(user_query)
 
# %% Ausgabe ansehen
res.model_dump()
 
# %%
from pprint import pprint
pprint(res.content)