#%%
from groq import Groq
import base64
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "waldo.jpg"
#image_path = "C:/Users/M_Sommerfeld/Pictures/IMG_8335.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)
#%% create Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

user_query = """Can you find the famous character Waldo?
                He wears glasses, a red and white striped shirt and a red hat.
                Return his location using relative coordinates between 0 and 1 for x and y
                starting from the top left corner."""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model ="meta-llama/llama-4-maverick-17b-128e-instructt",
)
##model="meta-llama/llama-4-scout-17b-16e-instruct",
print(chat_completion.choices[0].message.content)