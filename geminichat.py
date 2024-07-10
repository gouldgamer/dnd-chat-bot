import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



genai.configure(api_key=GEMINI_API_KEY)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  # Controls the randomness of the output.
  # Values close to 0 will produce more deterministic outputs,
  # while values close to 1 will produce more random outputs.
  "temperature": 1,

  # Nucleus sampling parameter.
  # Top-p sampling will select the tokens with probabilities that
  # cumulatively add up to this value.
  "top_p": 0.95,

  # Top-k sampling parameter.
  # Select the k tokens with the highest probabilities.
  "top_k": 64,

  # Maximum number of tokens to generate.
  "max_output_tokens": 8192,

  # The MIME type of the generated response.
  "response_mime_type": "text/plain",
}


system_instructions="you are a dungen master playing dnd with the user."

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  generation_config=generation_config,
  system_instruction=system_instructions
)

chat = model.start_chat(
  history=[]
)





if "chat" not in st.session_state:
    st.session_state.chat = chat


st.title('Gemini Pro 1.5 Chat')


for message in st.session_state.chat.history:
    if message.role == "model":
        st.chat_message("ai", avatar = "thumbnail-ai-ak.jpg").write(message.parts[0].text)
    else:
        st.chat_message(message.role).write(message.parts[0].text)

prompt = st.chat_input("How can I help you?")

if prompt:

    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)

    st.chat_message("assistant").write(response.text)

with st.sidebar.markdown("Dungen master"):
    st.image("thumbnail-ai-ak.jpg", width=150)