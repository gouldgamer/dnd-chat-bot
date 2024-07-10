from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import sys

load_dotenv()


# Access the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")


# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)


if len(sys.argv) < 2:
    print("Usage: python dalleImage.py <title> <prompt>")
    sys.exit(1)

title = sys.argv[1]
prompt = sys.argv[2]

# Add a system prompt to the user prompt
system_prompt = ""
full_prompt = f"{system_prompt} {prompt}"

response = client.images.generate(
    model="dall-e-3",
    prompt=full_prompt,
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url

# Send a GET request to the image URL
response = requests.get(image_url)

# Generate a unique filename based on the current date and time
current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
image_path = f"{title}-{current_time}.jpg"

# Save the image to a file
with open(image_path, "wb") as f:
    f.write(response.content)