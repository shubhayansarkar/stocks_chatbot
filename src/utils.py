import os

import chromadb
import dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma.vectorstores import Chroma
from langchain import hub
from langchain_core.output_parsers import StrOutputParser

from .logger import logger

# load environment variables
_flag = dotenv.load_dotenv('.env')
if not _flag:
    logger.critical('unable to read or locate `.env` file')
    exit(1)
else:
    logger.debug('[OK] loaded `.env` file')
    
# Vector Database
try:
    chroma_client = chromadb.HttpClient(
        host = os.getenv('CHROMA_HOSTNAME'),
        port = os.getenv('CHROMA_PORT')
    )
    logger.info('[OK] connected to remote chroma database')
    
except TypeError as e:
    logger.error(str(e))
    logger.critical('invalid arguments for chromadb in `.env` file')
    exit(1)
    
except ValueError as e:
    logger.error(str(e))
    logger.critical('unable to connect to chromadb server')
    exit(1)
    
# Ollama
try:
    logger.debug(f'Connecting to ollama server at: {os.getenv("OLLAMA_BASE_URL")}')
    chat_model = ChatOllama(
        base_url = os.getenv('OLLAMA_BASE_URL'),
        model = os.getenv('OLLAMA_CHAT_MODEL'),
        temperature = float(os.getenv('OLLAMA_TEMPERATURE')),
        keep_alive = int(os.getenv('OLLAMA_KEEP_ALIVE'))
    )
    logger.info(f'[OK] chat model: {os.getenv("OLLAMA_CHAT_MODEL")}')
    
    embedding_model = OllamaEmbeddings(
        base_url = os.getenv('OLLAMA_BASE_URL'),
        model = os.getenv('OLLAMA_EMBEDDING_MODEL')
    )
    logger.info(f'[OK] embedding model: {os.getenv("OLLAMA_EMBEDDING_MODEL")}')
    
except TypeError as e:
    logger.error(str(e))
    logger.critical('invalid arguments for ollama in `.env` file')
    exit(1)
    
except Exception as e:
    logger.error(str(e))
    raise e

text_splitter = RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=16)

prompt = ChatPromptTemplate.from_messages([
    ('system', "You are a DuckDuckGo Chatbot who answers user's queries from the search results."),
    ('human', "Explain the user's query: {query} using the search results: {search}")
])


def embed_documents(chunks: list[str]):
    vectorstore = Chroma(
        collection_name = os.urandom(8).hex(),
        embedding_function = embedding_model,
        client = chroma_client
    )
    vectorstore.add_texts(chunks)
    return vectorstore

# Chains
web_scraper = (
    DuckDuckGoSearchResults()
    | RunnableLambda(text_splitter.split_text)
    | RunnableLambda(embed_documents)
    | RunnablePassthrough.assign(search=RunnableLambda(lambda store: store.as_retriever()))
)
    
rag = (
    prompt
    | chat_model
    | StrOutputParser()
)