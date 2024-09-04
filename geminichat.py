import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

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
    GOOGLE_API_KEY=os.getenv("GEMINI_API_KEY")
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


system_instructions1="you are a dungen master Named Bob playing dnd with the user."
system_instructions2="you are going to respond to Bob your DM like you are playing dnd"

model1 = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instructions1
)

model2 = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instructions2
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


for chatbot in [st.session_state.chat1, st.session_state.chat2]:
    for message in chatbot.history:
        if message.role == "model":
            if chatbot == st.session_state.chat1:
                with st.chat_message("DM"):
                    st.write(message.parts[0].text)
            else:
                with st.chat_message("Player"):
                    st.write(message.parts[0].text)
        else:
            st.chat_message(message.role).write(message.parts[0].text)


prompt = st.chat_input("How can I help you?")
if st.button("coninue"):
    prompt = "continue"
if prompt or prompt == "continue":
    # ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).
    
    if prompt == "continue":
        if st.session_state.chat2.history:
            try:
                Player_response= st.session_state.chat2.history[-1].parts[0].text
                DM_response = st.session_state.chat1.send_message(Player_response)
                st.chat_message("Player").write(DM_response.text)
                # time.sleep(2)

                DM_response= st.session_state.chat1.history[-1].parts[0].text
                Player_response= st.session_state.chat2.send_message(DM_response)
                st.chat_message("DM").write(Player_response.text)
                # time.sleep(2)

                st.chat_message("user").markdown(prompt)
                DM_response = st.session_state.chat1.send_message(prompt)
                st.chat_message("DM").write(DM_response.text)
                # time.sleep(2)

                Player_response = st.session_state.chat2.send_message(DM_response.text)
                st.chat_message("Player").write(Player_response.text)
            except Exception as e:
                st.error("the servers are over loded try again.")
                # st.error(f"An error occurred while getting response: {e}")
    else:
        # User prompts Gorc with a new input
        response1 = st.session_state.chat1.send_message(prompt)
        st.chat_message("user").write(prompt)
        with st.chat_message("DM"):
            # st.image("images/orc_avatar-2024-06-18-16-32-10.webp", width=100)
            st.write(response1.text)

        # Add a short delay before getting Momos' response
        time.sleep(2)

        # Momos responds to Gorc's statement
        response2 = st.session_state.chat2.send_message(response1.text)
        with st.chat_message('Player'):
            # st.image("images/dwarf-2024-06-18-17-24-27.webp", width=100)
            st.write(response2.text)


with st.sidebar.markdown("Dungen master"):
    st.image("thumbnail-ai-ak.jpg", width=150)