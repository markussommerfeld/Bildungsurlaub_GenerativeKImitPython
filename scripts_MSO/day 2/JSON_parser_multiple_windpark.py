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
class WindparkOutput(BaseModel):
    name: str
    closest_city: str = Field(..., description="The name of the closest city to the windpark")
    year_of_construction: int
    number_of_turbines: str
    list_turbine_type: list[str]
    cumulative_capacity: int = Field(..., description="The cumulative capacity of the windpark in MW")
    confidence: float = Field(..., description="The confidence score of the answer between 0 and 1")
    
class WindparksOutput(BaseModel):
    WindPark: list[WindparkOutput]

parser = PydanticOutputParser[WindparkOutput](pydantic_object=WindparksOutput)
#parser.get_format_instructions()

#%% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
        "Du bist ein Experte fuer Windkraft in Deutschland. Anworte kurz und bündig. "
        "Finde die 5 größten Windparks in der gefragten Region. "
        "Sortiere dieses Windparks nach installierter Kapazität. "
        "Verwende das vorgegebene Schema {format_instructions} um die Antwort zu strukturieren."
    ),  
    ("user", "WindPark: <Region>{Region}</Region>")
]).partial(format_instructions=parser.get_format_instructions())
# partial uebergibt Informationen und fuellt das Template vor aus.

#%% Modell initilization
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0,seed=42)
# model = ChatGroq(model="openai/gpt-oss-120b")


#%% Chain erstellen
chain = prompt_template | model | parser

#%% run chain
res_Windparks = chain.invoke({"Region": "Nordsee"})

for res in res_Windparks.WindPark:
    print(res.name)
    print(res.closest_city)
    print(res.year_of_construction)
    print(res.number_of_turbines)
    print(res.cumulative_capacity)
    print(res.list_turbine_type)
    print(res.confidence)
    print("---" *20)

#%% Ausgabe
# console = Console()
# console.print(Markdown(res.content))
#print(res.title)

#pprint(parser.get_format_instructions())
