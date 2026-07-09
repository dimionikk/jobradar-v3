import voyageai
from app.core.config import settings

client = voyageai.AsyncClient(api_key=settings.VOYAGE_API_KEY)

EMBEDDING_MODEL = "voyage-3.5-lite"


async def embed_documents(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    result = await client.embed(texts, model=EMBEDDING_MODEL, input_type="document")
    return result.embeddings


async def embed_query(text: str) -> list[float]:
    result = await client.embed([text], model=EMBEDDING_MODEL, input_type="query")
    return result.embeddings[0]

