from langchain_openai import ChatOpenAI
from app.core.config import get_settings

settings = get_settings()

# Initialize OpenAI Chat model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.8,
    openai_api_key=settings.OPENAI_API_KEY,
)

async def generate_response(prompt: str, context: str = "") -> str:
    """
    Generate a GPT-based response with optional contextual data.
    """
    full_prompt = f"Context:\n{context}\n\nUser: {prompt}\nAI:"
    response = await llm.ainvoke(full_prompt)
    return response.content
