from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings

settings = get_settings()

# Initialize embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.OPENAI_API_KEY,
)

async def get_text_embedding(text: str):
    """
    Generate vector embedding for given text.
    """
    vector = await embedding_model.aembed_query(text)
    return vector
