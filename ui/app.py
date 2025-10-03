import streamlit as st
import requests

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000" 

# --- UI Setup ---
st.set_page_config(page_title="Jigyasa", layout="wide")
st.title("🧠 Jigyasa - Your AI Research Notebook")
st.write("Use the 'Add to Jigyasa' bookmarklet in your browser to add notes, then ask questions here.")

# --- THE NEW SIDEBAR ---
with st.sidebar:
    st.header("My Notebook")
    if st.button("Show My Notes"):
        try:
            response = requests.get(f"{BACKEND_URL}/notes")
            if response.status_code == 200:
                notes = response.json().get("notes", [])
                if notes:
                    for i, note in enumerate(notes):
                        with st.expander(f"Note {i+1}"):
                            st.markdown(note)
                else:
                    st.write("Your notebook is empty.")
            else:
                st.error("Failed to fetch notes from the backend.")
        except requests.exceptions.RequestException:
            st.error("Could not connect to the backend.")

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question about your notes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 Thinking... (the local AI is warming up)")
        try:
            response = requests.post(f"{BACKEND_URL}/ask", json={"question": prompt})
            if response.status_code == 200:
                answer = response.json().get("answer")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_message = f"Error from backend: {response.status_code} - {response.text}"
                message_placeholder.text(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend. Please ensure it's running. Details: {e}")