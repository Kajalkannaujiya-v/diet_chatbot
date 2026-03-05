import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()

# ✅ Proper CORS setup
origins = [
    "http://localhost:5173",
    "https://kk-chatbot.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
client = MongoClient(MONGO_URI)
db = client["chat"]
collection = db["users"]

class ChatRequest(BaseModel):
    user_id: str
    question: str

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("placeholder", "{history}"),
    ("user", "{question}")
])

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-8b-8192"
)

chain = prompt | llm


def get_history(user_id):
    chats = collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []

    for chat in chats:
        history.append((chat["role"], chat["message"]))

    return history


@app.get("/")
def home():
    return {"message": "AI Assistant API Running 🚀"}


@app.post("/chat")
def chat(request: ChatRequest):

    history = get_history(request.user_id)

    response = chain.invoke({
        "history": history,
        "question": request.question
    })

    # save user message
    collection.insert_one({
        "user_id": request.user_id,
        "role": "user",
        "message": request.question,
        "timestamp": datetime.now(timezone.utc)
    })

    # save assistant message
    collection.insert_one({
        "user_id": request.user_id,
        "role": "assistant",
        "message": response.content,
        "timestamp": datetime.now(timezone.utc)
    })

    return {"response": response.content}