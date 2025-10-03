Jigyasa - Your AI Research Notebook
Jigyasa (from Sanskrit, "the desire to know") is an AI-powered research assistant designed to solve the problem of "context collapse" during complex research. It acts as a second brain, allowing users to build a curated knowledge base from across the web and have intelligent, context-aware conversations with their findings.

🚀 The Problem: The Cognitive Chasm
When we do research, our process is chaotic. We read articles, watch videos, and talk to AI chatbots in separate, disconnected conversations. The user is left to connect all the dots alone, which is overwhelming and leads to "analysis paralysis." Jigyasa provides the infrastructure for the user's learning journey itself.

✨ The Solution: A Stateful Synthesis Engine
Jigyasa uses a Retrieval-Augmented Generation (RAG) pipeline to create a persistent, stateful "notebook" of a user's research. The AI's knowledge is strictly limited to this curated context, allowing for deep, cross-source synthesis without the noise of the open internet.

Core Features (Hackathon MVP)
Frictionless Capture: A browser bookmarklet to capture any highlighted text from any website.

Persistent Notebook: A backend that collects and stores all captured notes.

Conversational RAG: A chat interface to have intelligent, context-based conversations with the AI, which synthesizes answers from the collected notes.

Local-First AI: Runs 100% locally using Ollama, ensuring privacy and zero cost.

🛠️ Tech Stack
Backend: Python, FastAPI

AI Pipeline: LangChain, Ollama, ChromaDB (In-Memory), FastEmbed

Frontend / UI: Streamlit

Web Clipper: Plain JavaScript (Bookmarklet)

🏃‍♀️ How to Run This Project
Follow these steps to get Jigyasa running on your local machine.

Prerequisites
Python 3.9+

Git

Ollama installed and running.

1. Set Up the Environment

# Clone the repository

git clone <your-repo-url>
cd jigyasa-ai-notebook

# Create and activate a virtual environment for the backend

cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install all backend dependencies

pip install -r requirements.txt

2. Download the Local AI Model
   You only need to do this once. Open a new, clean terminal (no venv active) and run:

ollama run gemma:2b

3. Run the Application
   You will need two separate terminals running simultaneously.

Terminal 1: Start the Backend Server

# Make sure you are in the 'backend' folder with your venv active

(venv) $ uvicorn main:app --reload

Terminal 2: Start the Streamlit UI

# Make sure you are in the main project folder

$ cd ../ui

# Install UI dependencies

pip install streamlit requests

# Run the app

streamlit run app.py

4. Create the Bookmarklet
   Open your browser's Bookmark Manager.

Create a new bookmark.

Name: Add to Jigyasa

URL: Copy and paste the entire single line of code from the bookmarklet.js file in the repository.

You can now navigate to a webpage, highlight text, and click the bookmarklet to add notes to your notebook, which is visible in the Streamlit UI running in your browser.
