from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

def get_qdrant() -> QdrantClient:
    """
    Returns a configured Qdrant client.
    Uses environment variables for host and API key.
    """
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Qdrant: {str(e)}")
