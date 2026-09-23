import os
import json
import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Configurable defaults
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "768"))
CACHE_PATH = os.getenv("EMBEDDING_CACHE_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "data", "embeddings_cache.npz"))
KB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base.json")

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)
_API_KEY = os.getenv("GEMINI_API_KEY")
_CLIENT = None
if _API_KEY:
    _CLIENT = genai.Client(api_key=_API_KEY)


def get_embedding(text: str) -> Optional[np.ndarray]:
    """
    Fetches an embedding from Gemini using the google-genai SDK.
    Gracefully handles missing keys, timeouts, and API errors.
    Returns None on failure.
    """
    if not _CLIENT:
        logger.warning("GEMINI_API_KEY missing. Embedding API unavailable.")
        return None

    try:
        result = _CLIENT.models.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIMENSION
            )
        )
        if not result.embeddings or not result.embeddings[0].values:
            return None
        return np.array(result.embeddings[0].values, dtype=np.float32)
    except Exception as e:
        logger.error(f"Embedding API failed: {e}")
        return None


def get_embeddings_batch(texts: List[str]) -> Optional[np.ndarray]:
    """
    Fetches a batch of embeddings from Gemini using the google-genai SDK.
    """
    if not _CLIENT:
        logger.warning("GEMINI_API_KEY missing. Embedding API unavailable.")
        return None

    try:
        vectors = []
        for text in texts:
            result = _CLIENT.models.embed_content(
                model=GEMINI_EMBEDDING_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=EMBEDDING_DIMENSION
                )
            )
            if not result.embeddings or not result.embeddings[0].values:
                return None
            vectors.append(result.embeddings[0].values)

        if len(vectors) != len(texts):
            return None

        return np.array(vectors, dtype=np.float32)
    except Exception as e:
        logger.error(f"Batch embedding API failed: {e}")
        return None


def _compute_kb_hash() -> str:
    """Computes a SHA256 hash of the knowledge base JSON file."""
    if not os.path.exists(KB_PATH):
        return ""
    with open(KB_PATH, "rb") as f:
        file_bytes = f.read()
    return hashlib.sha256(file_bytes).hexdigest()


class EmbeddingCacheManager:
    def __init__(self, cache_path: str = CACHE_PATH):
        self.cache_path = cache_path
        self.kb_hash = _compute_kb_hash()

    def load_cache(self) -> Tuple[Optional[np.ndarray], Optional[List[str]]]:
        """
        Loads the .npz cache if valid. Returns (embeddings, record_ids) or (None, None).
        """
        if not os.path.exists(self.cache_path):
            logger.info("Embedding cache not found.")
            return None, None

        try:
            data = np.load(self.cache_path, allow_pickle=True)
            metadata = json.loads(str(data['metadata']))

            # Validation
            if metadata.get("kb_hash") != self.kb_hash:
                logger.info("KB Hash mismatch. Cache invalidated.")
                return None, None

            if metadata.get("model") != GEMINI_EMBEDDING_MODEL:
                logger.info("Embedding model mismatch. Cache invalidated.")
                return None, None

            if metadata.get("dimension") != EMBEDDING_DIMENSION:
                logger.info("Embedding dimension mismatch. Cache invalidated.")
                return None, None

            embeddings = data['embeddings']
            record_ids = list(data['record_ids'])

            logger.info("Successfully loaded embedding cache.")
            return embeddings, record_ids

        except Exception as e:
            logger.error(f"Failed to load embedding cache: {e}")
            return None, None

    def build_and_save_cache(self, records: List[Dict[str, Any]]) -> bool:
        """
        Builds the cache by calling the API and saving as .npz.
        """
        texts = []
        record_ids = []
        for r in records:
            # Concatenate relevant fields for document embedding
            content = f"{r.get('title', '')}. {r.get('summary', '')}. " + " ".join(r.get('keywords', []))
            texts.append(content.strip())
            record_ids.append(r['id'])

        if not texts:
            return False

        logger.info(f"Generating embeddings for {len(texts)} records...")
        embeddings = get_embeddings_batch(texts)

        if embeddings is None:
            logger.error("Failed to build embedding cache due to API failure.")
            return False

        metadata = {
            "model": GEMINI_EMBEDDING_MODEL,
            "dimension": EMBEDDING_DIMENSION,
            "kb_hash": self.kb_hash,
            "version": "1.0",
            "created_at": datetime.utcnow().isoformat()
        }

        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            np.savez_compressed(
                self.cache_path,
                embeddings=embeddings,
                record_ids=np.array(record_ids),
                metadata=np.array(json.dumps(metadata))
            )
            logger.info("Successfully saved embedding cache to .npz.")
            return True
        except Exception as e:
            logger.error(f"Failed to save embedding cache: {e}")
            return False
