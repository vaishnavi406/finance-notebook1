# The imports have changed slightly
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# --- No API Keys Needed! ---

# --- The Master Prompt (Stays the same) ---
synthesis_prompt_template = """
You are Jigyasa, a brilliant and cautious financial research assistant. Your goal is to help users connect the dots in their own research. You must follow these rules:
1.  Prioritize using the 'user_research_notebook_search' tool to find answers in the user's notes first.
2.  If you cannot find the answer in the user's notes, you may then use the 'wikipedia' tool for general financial terms.
3.  When you find conflicting information, point it out clearly.
4.  After providing the main insight, you MUST analyze all the user's notes for signs of common investor biases like 'Recency Bias' (focusing only on recent performance). If a bias is detected, you MUST add a gentle, helpful warning about it.
5.  Always conclude your final answer by suggesting a single, clear, and actionable 'next logical step' for the user's research.

You have access to the following tools: {tools}
Use the following format to reason through your answer:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: [Your synthesized insight, your bias warning if any, and the next logical step]

Begin!

Question: {input}
{agent_scratchpad}
"""
SYNTHESIS_PROMPT = PromptTemplate(
    template=synthesis_prompt_template, input_variables=["context", "question"]
)
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