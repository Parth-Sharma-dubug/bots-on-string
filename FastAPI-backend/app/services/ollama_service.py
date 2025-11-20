# app/services/ollama_service.py

import os
import httpx
from app.services.qdrant_service import search_similar_vectors
from app.services.qdrant_service import retrieve_chunks

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3.2")  # change to the model you pulled via `ollama pull`

# 🔥 Toxicity / Offensive Word Filter
OFFENSIVE_WORDS = {
    "madarchod", "mc", "bc", "bhenchod", "lawda", "lawde", "lawdeya", "chutiya",
    "chutiye", "lund", "gaand", "gandu", "fuck", "fucker", "fucking", "bitch",
    "asshole", "dumbass", "nigger", "slut", "whore"
}

def is_offensive(text: str) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in OFFENSIVE_WORDS)


# chat history
def build_chat_history(history: list[dict]) -> str:
    if not history:
        return "No previous messages."

    formatted = []
    for item in history:
        formatted.append(f"User: {item['query']}")
        formatted.append(f"Bot: {item['answer']}")

    return "\n".join(formatted)


async def generate_reply(message: str, chatbot_id: str, history: list[dict]):

    print("🔵 OLLAMA_URL =", OLLAMA_URL)
    print("chatbot_id =", chatbot_id)
    print("message =", message)

    if is_offensive(message):
        return "I am sorry, but I cannot respond to offensive language."

    # 1️⃣ Retrieve relevant context from Qdrant
    user_message = message
    chunks = retrieve_chunks(user_message, chatbot_id)

    context = (
        "No relevant knowledge was found for this query."
        if not chunks else "\n\n".join(chunks)
    )

    chat_history = build_chat_history(history)

    # 2️⃣ STRICT RAG + BASIC COMMUNICATION PROMPT
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a STRICT RAG-based assistant used by a company.\n"
                "Follow these rules exactly:\n"
                "\n"
                "1️⃣ If the user's query requires factual information, you MUST answer ONLY using the knowledge-base context provided.\n"
                "2️⃣ If the required information is NOT found in the context, respond with:\n"
                "   'I don’t have information about that.'\n"
                "3️⃣ NEVER invent facts, policies, numbers, or details.\n"
                "4️⃣ Basic polite conversation IS allowed (e.g., 'hi', 'ok', 'thank you', 'yes', simple small talk).\n"
                "5️⃣ DO NOT generate jokes, games, riddles, or creative content.\n"
                "6️⃣ Keep all responses short, formal, and precise.\n"
                "7️⃣ Only use the knowledge-base for factual answers. Never use outside knowledge.\n"
            )
        },
        {
            "role": "user",
            "content": (
                f"Knowledge Base Context:\n{context}\n\n"
                f"Conversation History:\n{chat_history}\n\n"
                f"User Message:\n{user_message}\n\n"
                "IMPORTANT:\n"
                "- If the user message is casual (hi/ok/thanks/yes), just reply politely.\n"
                "- If the user message is a factual question, you MUST use only the context.\n"
            )
        }
    ]

    # 3️⃣ Query Ollama
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": LLM_MODEL, "messages": prompt, "stream": False}
        )

    data = response.json()
    print("🔥 OLLAMA RAW RESPONSE:", data)

    # 4️⃣ Extract reply safely
    if "message" in data:
        return data["message"]["content"]

    if "messages" in data and isinstance(data["messages"], list):
        return data["messages"][-1]["content"]

    if "response" in data:
        return data["response"]

    return "⚠️ Could not read response from Ollama."
