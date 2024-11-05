# from langchain_community.llms.ollama import Ollama
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.retrieval_qa.base import RetrievalQA
from searcher import ddg_search
# import chromadb

# import pickle
# file_path = r"C:\newcodes\llm\finance_chatbot\data\vectorstore.pkl"
# embedding = OllamaEmbeddings(base_url= 'http://localhost:11434/', model='all-minilm')
# client = chromadb.HttpClient(host="localhost", port=8000)
# # print(client)
# llm = Ollama(base_url= 'http://localhost:11434/', model='llama2')


urls = ddg_search().serach(query="ratan tata", num_web=1)
# # print(urls)
# loader = UnstructuredURLLoader(urls= urls)
# data = loader.load()
# splitter = RecursiveCharacterTextSplitter(
#         separators=['\n\n', '\n', '.', ','],
#         chunk_size=500
#     )
# data_chunks = splitter.split_documents(data)

# vector_store = client.from_documents(documents=data_chunks, embedding=embedding, persist_directory='.\chroma\db')
# retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type= "stuff", retriever = vector_store.as_retriever())
# # print(retrieval_chain)
# res = retrieval_chain.invoke("who is ratan tata?")
# print(res)

# # print(vector_store)
# # with open(file_path, "wb") as f:
# #     pickle.dump(vector_store, f)
# # print("done")
# # # print(vector_store)


from chromadb import HttpClient
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from duckduckgo_search import ddg_search

# Define file path and embedding model
file_path = r"C:\newcodes\llm\finance_chatbot\data\vectorstore.pkl"
embedding = OllamaEmbeddings(base_url='http://localhost:11434/', model='all-minilm')

# Initialize ChromaDB HTTP client
client = HttpClient(host="localhost", port=8000)

# Initialize LLM model
llm = Ollama(base_url='http://localhost:11434/', model='llama2')

# Perform web search and load content
# urls = ddg_search().search(query="ratan tata", num_results=1)
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(separators=['\n\n', '\n', '.', ','], chunk_size=500)
data_chunks = splitter.split_documents(data)

# Create or access a collection in ChromaDB
collection = client.create_collection("my_collection")

# Embed and add each document to the collection
for chunk in data_chunks:
    embedding_vector = embedding.embed_text(chunk.page_content)
    collection.add(
        documents=[chunk.page_content],
        embeddings=[embedding_vector],
        metadatas=[{"source": chunk.metadata.get("source")}]
    )

# Configure Retrieval Chain
retriever = collection.as_retriever()
retrieval_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Run the query
res = retrieval_chain.invoke("Who is Ratan Tata?")
print(res)
