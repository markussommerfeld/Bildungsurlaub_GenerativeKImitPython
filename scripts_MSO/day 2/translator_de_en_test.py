#%%
# Use a pipeline as a high-level helper
# lokal gehostetes experten Model.

from transformers import pipeline

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")

pipe(["Ich bin ein Berliner.", "Das Wetter ist heute schön."])

# Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
# model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")


# %% below is a complete sentence example.
#%% Use a pipeline as a high-level helper
from transformers import pipeline
 
pipe = pipeline(task="translation", model="Helsinki-NLP/opus-mt-de-en")
# %%
pipe(["Ich bin ein Berliner.", "Das Wetter ist schön."])
 
#%% Beispiel: Lückentext
task = "fill-mask"
pipe = pipeline(task=task)
 
pipe("Tief unten im <mask> liegt ein Schatz.")
 