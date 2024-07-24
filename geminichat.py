import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

if "api_key" not in st.session_state:
    st.session_state.api_key = None  # Initialize the API key

with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("Enter your Google API Key", value="", type="password")
    submit_btn = st.button("Save API Key")

    if submit_btn:
        st.session_state.api_key = api_key_input 
        st.success("API key saved!")

if st.session_state.api_key:
    GOOGLE_API_KEY = st.session_state.api_key
    genai.configure(api_key=GOOGLE_API_KEY)

    # ... rest of your code ...
else:
    st.warning("Please enter your Google API Key in the sidebar.") 
    
genai.configure(api_key=GOOGLE_API_KEY)

print(GOOGLE_API_KEY)
# st.write(st.session_state)
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
  "max_output_tokens": 600,

  # The MIME type of the generated response.
  "response_mime_type": "text/plain",
}


system_instructions1="you are a dungen master playing dnd with the user."
system_instructions2="you are playing dnd"

model1 = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  generation_config=generation_config,
  system_instruction1=system_instructions1
)

model2 = genai.GenerativeModel(
  model_name="gemini-1.5-pro-latest",
  generation_config=generation_config,
  system_instruction2=system_instructions2
)


chat1 = model1.start_chat(
  history=[]
)
chat2 = model2.start_chat(
  history=[]
)




if "chat1" not in st.session_state:
    st.session_state.chat1 = chat1

if "chat2" not in st.session_state:
    st.session_state.chat2 = chat2

st.title('DND THE GAME')


for chatbot in [st.session_state.chat1.history, st.session_state.chat2.history]:
    for message in chatbot.history:
        if message.role == "model":
            if chatbot == st.session_state.chat1:
                with st.chat_message("model"):
                    st.write(message.parts[0].text)
        else:
            st.chat_message(message.role).write(message.parts[0].text)


prompt = st.chat_input("How can I help you?")

if prompt:

    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)

    st.chat_message("assistant").write(response.text)

with st.sidebar.markdown("Dungen master"):
    st.image("thumbnail-ai-ak.jpg", width=150)