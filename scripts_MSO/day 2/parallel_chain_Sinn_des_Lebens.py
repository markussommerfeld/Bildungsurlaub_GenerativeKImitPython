#%% pakete
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from rich.console import Console
from rich.markdown import Markdown
console = Console()
 
#%% Prompt Template
prompt_template_friendly = ChatPromptTemplate.from_messages([
    ("system", """Die bist ein freundlicher Assistent.
    Antworte freundlich, kurz und bündig.
    """),
    ("user", "Thema: <thema>{thema}</thema>")
])
 
prompt_template_unfriendly = ChatPromptTemplate.from_messages([
    ("system", """Die bist ein unfreundlicher Assistent.
    Antworte genervt, kurz und bündig.
    """),
    ("user", "Thema: <thema>{thema}</thema>")
])
 
# %% Modellinstanz erstellen
model = ChatGroq(model="openai/gpt-oss-120b")
 
 
#%% Chain erstellen
chain_friendly = prompt_template_friendly | model | StrOutputParser()
chain_unfriendly = prompt_template_unfriendly | model | StrOutputParser()
 
chain = RunnableParallel(
    unfriendly = chain_unfriendly,
    friendly = chain_friendly
)
 
 
#%% Chain ausführen
thema = "Sinn des Lebens"
 
res = chain.invoke({"thema": thema})
 
#%%
res
 
#%% Ausgabe
console.print(Markdown(res["friendly"]), width=50)
console.print(Markdown(res["unfriendly"]), width=50)
 