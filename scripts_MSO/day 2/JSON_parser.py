#%% pakete
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
from rich.markdown import Markdown
load_dotenv(find_dotenv())
#%% parser
# This defines the structure of the output!
class MovieOutput(BaseModel):
    title: str
    director: str
    release_year: int
    genre: str
    role_name: list[str]
    actor_name: list[str]
    
# class MoviesOutput(BaseModel):
#     movies: list[MovieOutput]
parser = PydanticOutputParser[MovieOutput](pydantic_object=MovieOutput)
#parser.get_format_instructions()

#%% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
        "Du bist ein Filmexperte. Anworte kurz und bündig. "
        "Verwende das vorgegebene Schema {format_instructions} um die Antwort zu strukturieren."
    ),  
    ("user", "Filmbeschreibung: <Beschreibung>{Beschreibung}</Beschreibung>")
]).partial(format_instructions=parser.get_format_instructions())
# partial uebergibt Informationen und fuellt das Template vor aus.

#%% Modell initilization
model = ChatGroq(model="openai/gpt-oss-120b")

#%% Chain erstellen
chain = prompt_template | model | parser

#%% run chain
res = chain.invoke({"Beschreibung": "Ein Schiff sinkt."})

#%% Ausgabe
# console = Console()
# console.print(Markdown(res.content))
print(res.title)

