# Generative AI Chatbot (Backend)

This project is a Generative AI Chatbot built using FastAPI and integrated with a Large Language Model (LLM).

## 🚀 Tech Stack
- Python
- FastAPI
- LLM API Integration
- Render (Deployment)

## 📌 Features
- /chat endpoint for user interaction
- Prompt handling and response generation
- REST API architecture
- Swagger UI testing support

## 🛠 Installation

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the server:
   uvicorn app:app --reload

## 🌐 Deployment
The backend is deployed on Render.

## 📖 API Endpoint
POST /chat  
Request Body:
{
  "user_id": "xyz",
  "question": "Your question here"
}

Response:
{
  "response": "AI generated answer"
}

---

Currently working on frontend integration to complete full-stack implementation.
