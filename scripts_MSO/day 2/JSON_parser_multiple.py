#%% pakete
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
from rich.markdown import Markdown
from pprint import pprint
load_dotenv(find_dotenv())
#%% parser
# This defines the structure of the output!
class MovieOutput(BaseModel):
    title: str
    director: str = Field(..., description="The name of the director of the movie, formatted as last name, first name")
    release_year: int
    genre: str
    role_name: list[str]
    actor_name: list[str]
    revenue: int = Field(..., description="The commercial revenue of the movie in million USD")
    confidence: float = Field(..., description="The confidence score of the answer between 0 and 1")
    
class MoviesOutput(BaseModel):
    movies: list[MovieOutput]

parser = PydanticOutputParser[MovieOutput](pydantic_object=MoviesOutput)
#parser.get_format_instructions()

#%% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
        "Du bist ein Filmexperte. Anworte kurz und bündig. "
        "Gib 5 Filme, die zur Beschreibung passen. "
        "Sortiere dieses Filme nach kommerziellem Erfolg. "
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
res_movies = chain.invoke({"Beschreibung": "Western"})

for res in res_movies.movies:
    print(res.title)
    print(res.actor_name)
    print(res.director)
    print(res.release_year)
    print(res.revenue)
    print(res.confidence)
    print("---" *20)

#%% Ausgabe
# console = Console()
# console.print(Markdown(res.content))
#print(res.title)

# this prints the format instructions for the parser
#pprint(parser.get_format_instructions())
