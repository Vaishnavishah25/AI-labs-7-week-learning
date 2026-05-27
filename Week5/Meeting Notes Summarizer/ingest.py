from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
import os
loader = DirectoryLoader(
    "data/meetings",
    glob="*.txt",
    loader_cls=TextLoader
)

documents = loader.load()
# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = splitter.split_documents(documents)

print(docs)
print(len(docs))
# Embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Create vector DB
vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

# Save DB
vectorstore.save_local("vector_db")

print("Vector database created successfully!")