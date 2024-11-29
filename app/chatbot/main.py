from langchain.chains.combine_documents import create_stuff_documents_chain
from app.chatbot.src.helper import download_hugging_face_embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_pinecone import PineconeVectorStore
from fastapi.responses import JSONResponse
from app.chatbot.src.prompt import *
from fastapi import FastAPI, Form
from langchain.llms import Cohere
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

# Initialize FastAPI
app = FastAPI()

# Hugging Face embeddings and Pinecone setup
embeddings = download_hugging_face_embeddings()

index_name = "medicalbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = Cohere(
    cohere_api_key=COHERE_API_KEY,
    model="command-xlarge",
    temperature=0.4,
    max_tokens=500
)

# Define the ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



