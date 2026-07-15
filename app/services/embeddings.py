import logging

import voyageai

from app.core.config import settings

logger = logging.getLogger(__name__)

client = voyageai.AsyncClient(api_key=settings.VOYAGE_API_KEY, max_retries=3, timeout=30)

EMBEDDING_MODEL = "voyage-3.5-lite"
EMBED_BATCH_SIZE = 128


async def embed_documents(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        try:
            result = await client.embed(batch, model=EMBEDDING_MODEL, input_type="document")
        except Exception:
            logger.exception("Voyage API call failed for batch starting at index %s", i)
            raise
        all_embeddings.extend(result.embeddings)

    return all_embeddings


async def embed_query(text: str) -> list[float]:
    try:
        result = await client.embed([text], model=EMBEDDING_MODEL, input_type="query")
    except Exception:
        logger.exception("Voyage API call failed for embed_query")
        raise
    return result.embeddings[0]