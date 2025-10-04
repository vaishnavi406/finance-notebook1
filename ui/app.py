import streamlit as st
import requests

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- UI Setup ---
st.set_page_config(page_title="Jigyasa", layout="wide", initial_sidebar_state="collapsed")

# --- Custom CSS for the new UI ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* --- Main Background & Font --- */
body {
    font-family: 'Poppins', sans-serif;
    color: #FFFFFF;
    overflow: hidden; /* Hide scrollbars */
}

.stApp {
    background: linear-gradient(-45deg, #11111d, #3a2d5c, #2c1e4f, #11111d);
    background-size: 400% 400%;
    animation: moveGradient 20s ease infinite;
}

/* Hide Streamlit's default header and footer */
[data-testid="stHeader"], footer {
    display: none !important;
}

/* --- Notes Button --- */
.notes-button-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 999;
}

/* --- Centered Layout --- */
.main .block-container {
    max-width: 750px;
    margin: 0 auto;
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    min-height: 95vh;
    justify-content: center;
}

/* --- Title & Subtitle --- */
.title-container {
    text-align: center;
    margin-bottom: 2rem;
}

.title-container h1 {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -2px;
    margin: 0;
}

.title-container p {
    font-size: 1.2rem;
    color: #a1a1aa; /* Light grey for subtitle */
}

/* --- Chat Input --- */
.stChatInput {
    background-color: rgba(0,0,0,0.2);
    border-radius: 1rem;
    border: 1px solid #333;
    backdrop-filter: blur(10px);
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 720px;
}

/* --- Chat Messages --- */
[data-testid="stChatMessage"] {
    background-color: #1E1E2F;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
}

/* --- Thinking Animation (Full-Screen Aurora) --- */
.aurora-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0; /* Behind main content but above background */
    pointer-events: none; /* Allow clicks to pass through */
}

.aurora__item {
    position: absolute;
    width: 60vw;
    height: 60vw;
    border-radius: 50%;
    filter: blur(100px);
    mix-blend-mode: screen;
    opacity: 0.5;
}

.aurora__item:nth-of-type(1) {
    background: radial-gradient(circle, #ffc107, transparent 50%);
    animation: aurora-1 12s ease-in-out infinite alternate;
}
.aurora__item:nth-of-type(2) {
    background: radial-gradient(circle, #ff9800, transparent 50%);
    animation: aurora-2 10s ease-in-out infinite alternate;
}
.aurora__item:nth-of-type(3) {
    background: radial-gradient(circle, #e75a7c, transparent 50%);
    animation: aurora-3 8s ease-in-out infinite alternate;
}

@keyframes aurora-1 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(100vw, 100vh) scale(1.5); }
}
@keyframes aurora-2 {
    0% { transform: translate(100vw, 100vh) scale(1.2); }
    100% { transform: translate(0, 0) scale(0.8); }
}
@keyframes aurora-3 {
    0% { transform: translate(50vw, 0) scale(0.7); }
    100% { transform: translate(0, 100vh) scale(1.3); }
}

@keyframes moveGradient {
	0% { background-position: 0% 50%; }
	50% { background-position: 100% 50%; }
	100% { background-position: 0% 50%; }
}

/* --- Cursor Hover Gradient Effect --- */
body::before {
    content: '';
    position: fixed;
    top: var(--y, 50%);
    left: var(--x, 50%);
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #ffc107, #ff9800, transparent 60%);
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.4;
    z-index: -1; /* Places it behind all content */
    transition: top 0.1s ease-out, left 0.1s ease-out;
}
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# --- JavaScript for Mouse Tracking ---
mouse_tracker_js = """
<script>
const body = document.querySelector('body');
body.addEventListener('mousemove', (e) => {
    body.style.setProperty('--x', e.clientX + 'px');
    body.style.setProperty('--y', e.clientY + 'px');
});
</script>
"""
st.markdown(mouse_tracker_js, unsafe_allow_html=True)

# --- Sidebar for Notes ---
with st.sidebar:
    st.header("My Notebook")
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

# --- UI Layout ---
# This container holds the button
st.markdown('<div class="notes-button-container"></div>', unsafe_allow_html=True)
with st.container():
    # This is a bit of a hack to get the button in the container
    st.button("My Notes")

if not st.session_state.get("messages"):
    st.markdown("""
        <div class="title-container">
            <h1>Ask something about your notes</h1>
            <p>Jigyasa helps you synthesize and chat with your research.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # Show the full-screen aurora animation while waiting for a response
        aurora_html = """
        <div class="aurora-container">
            <div class="aurora__item"></div>
            <div class="aurora__item"></div>
            <div class="aurora__item"></div>
        </div>
        """
        # We use a separate placeholder for the full-screen effect
        aurora_placeholder = st.empty()
        aurora_placeholder.markdown(aurora_html, unsafe_allow_html=True)

        # The original placeholder still shows the "Thinking..." text
        message_placeholder.markdown("🧠 Thinking...")
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