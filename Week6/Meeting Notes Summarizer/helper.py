from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

from prompt import (
    SYSTEM_PROMPT,
    QUESTION_PROMPT,
    SUMMARY_PROMPT,
    ACTION_ITEMS_PROMPT
)

# Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Load vector DB
vectorstore = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# LLM
llm = ChatOllama(
    model="llama3.1:8b-instruct-q4_K_M",
    temperature=0.2
)

def get_context(question):

    docs = retriever.invoke(question)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    return context


def ask_meeting(question):

    context = get_context(question)

    final_prompt = f"""
    {SYSTEM_PROMPT}

    {QUESTION_PROMPT.format(
        context=context,
        question=question
    )}
    """

    response = llm.invoke(final_prompt)

    return response.content


def generate_summary():

    context = get_context("meeting summary")

    final_prompt = f"""
    {SYSTEM_PROMPT}

    {SUMMARY_PROMPT.format(
        context=context
    )}
    """

    response = llm.invoke(final_prompt)

    return response.content


def extract_action_items():

    context = get_context("action items")

    final_prompt = f"""
    {SYSTEM_PROMPT}

    {ACTION_ITEMS_PROMPT.format(
        context=context
    )}
    """

    response = llm.invoke(final_prompt)

    return response.content