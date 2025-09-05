# -*- coding: utf-8 -*-
"""app.py"""

import streamlit as st
import openai
import pickle

# Load the chatbot function from pickle
with open("Pedictric_Help_bot.pkl", "rb") as f:
    chatbot_data = pickle.load(f)

chatbot = chatbot_data()  # this gives us the chatbot function

st.set_page_config(page_title="Pediatrician Chatbot", page_icon="🧸")

st.title("🧸 Pediatrician Chatbot")
st.markdown("Your friendly assistant specialized in **pre-teens, teens, child abuse, and children's developmental issues**.")

# --- API Key Input ---
api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a Pediatrician specialize in pre-teens and teens, child abuse, or children's developmental issues."},
        ]

    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]

            with st.chat_message("assistant"):
                st.write(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"Error: {e}")

    # Button to clear chat
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a Pediatrician specialize in pre-teens and teens, child abuse, or children's developmental issues."},
        ]
        st.experimental_rerun()
else:
    st.warning("⚠️ Please enter your OpenAI API key to start chatting.")
