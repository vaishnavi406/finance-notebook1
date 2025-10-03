# The imports have changed slightly
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- No API Keys Needed! ---

# --- The Master Prompt (Stays the same) ---
synthesis_prompt_template = """
You are Jigyasa, an expert financial research assistant. Your user has provided you with several research notes they've captured. 
Your task is to synthesize these notes to provide a clear, concise, and unbiased answer to their question.
IMPORTANT: You must base your answer ONLY on the information provided in the "Context" notes below. Do not use any outside knowledge.
If the context does not contain the answer, you must state that the information is not available in the notebook.

Context:
---
{context}
---

Question: {question}

Synthesized Answer:
"""
SYNTHESIS_PROMPT = PromptTemplate(
    template=synthesis_prompt_template, input_variables=["context", "question"]
)

# --- The Core RAG Function (with the final optimized engine) ---
def get_jigyasa_response(question: str, notes: list[str]) -> str:
    if not notes:
        return "The notebook is empty."

    docs = [Document(page_content=note) for note in notes]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    # --- THE NEW, SPECIALIST LIBRARIAN (Embeddings) ---
    # This model is specifically designed to be small, fast, and run on a CPU.
    embeddings = FastEmbedEmbeddings()

    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # --- THE NEW, FASTER THINKER (LLM) ---
    # We are now using the gemma:2b model, which is optimized for speed.
    llm = Ollama(model="gemma:2b")

    # The RAG chain logic stays exactly the same!
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | SYNTHESIS_PROMPT
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)
    vectorstore.delete_collection()
    return answer