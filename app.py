import streamlit as st
from openai import OpenAI

st.title('Cintas Chat Bot - POC')

st.write('This is a simple example of a chatbot that can help you with your questions about Cintas.')

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini-2024-07-18"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 20

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["context"])

if len(st.session_state.messages) >= st.session_state.max_messages:
    st.info("You have reached the maximum number of messages. Please refresh the page to start a new conversation.")

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "context": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try: 
                stream = client.chat.completions.create(
                    model = st.session_state["openai_model"],
                    messages = [
                        {"role" : m["role"], "content" : m["context"]} for m in st.session_state.messages
                    ],
                    stream = True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "context": response})
            except:
                st.session_state.max_messages = len(st.session_state.messages)
                rate_limit_message = "You have reached the rate limit of the OpenAI API. Please wait a few minutes before starting a new conversation."
                st.session_state.messages.append({"role": "assistant", "context": rate_limit_message})
                st.rerun()