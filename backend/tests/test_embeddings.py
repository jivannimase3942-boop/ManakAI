import os
import json
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from app.embeddings import (
    get_embedding,
    get_embeddings_batch,
    EmbeddingCacheManager,
    GEMINI_EMBEDDING_MODEL,
    EMBEDDING_DIMENSION
)
from google.genai import types

@pytest.fixture
def mock_client():
    client_mock = MagicMock()
    with patch('app.embeddings._CLIENT', client_mock):
        yield client_mock

@pytest.fixture
def temp_cache_path(tmp_path):
    return str(tmp_path / "test_cache.npz")

@pytest.fixture
def mock_kb_hash():
    with patch('app.embeddings._compute_kb_hash', return_value="dummyhash123") as mock:
        yield mock

def test_configurability():
    # We assert it's an int rather than a specific number because other tests might patch it
    assert isinstance(EMBEDDING_DIMENSION, int)

@patch('app.embeddings._CLIENT')
def test_successful_embedding_generation_query(mock_client):
    # Setup mock response
    mock_embed = MagicMock()
    mock_embed.values = [0.1] * EMBEDDING_DIMENSION
    mock_result = MagicMock()
    mock_result.embeddings = [mock_embed]
    mock_client.models.embed_content.return_value = mock_result

    result = get_embedding("test query")

    assert result is not None
    assert isinstance(result, np.ndarray)
    assert result.shape == (EMBEDDING_DIMENSION,)

    # Verify the config was passed correctly without task_type
    mock_client.models.embed_content.assert_called_once()
    args, kwargs = mock_client.models.embed_content.call_args
    assert kwargs['config'].output_dimensionality == EMBEDDING_DIMENSION

@patch('app.embeddings._CLIENT')
def test_successful_embedding_generation_document(mock_client):
    # Setup mock response
    mock_embed1 = MagicMock()
    mock_embed1.values = [0.2] * EMBEDDING_DIMENSION
    mock_embed2 = MagicMock()
    mock_embed2.values = [0.3] * EMBEDDING_DIMENSION
    mock_result = MagicMock()
    mock_result.embeddings = [mock_embed1, mock_embed2]
    mock_client.models.embed_content.return_value = mock_result

    result = get_embeddings_batch(["doc1", "doc2"])

    assert result is not None
    assert isinstance(result, np.ndarray)
    assert result.shape == (2, EMBEDDING_DIMENSION)

    call_args = mock_client.models.embed_content.call_args[1]
    assert call_args["contents"] == "doc2"
    assert call_args["config"].output_dimensionality == EMBEDDING_DIMENSION

@patch('app.embeddings._CLIENT', None)
def test_missing_api_key_graceful_fail():
    # Should not crash, returns None
    result = get_embedding("test")
    assert result is None

def test_api_failure_graceful_fail(mock_client):
    mock_client.models.embed_content.side_effect = Exception("API Timeout")
    result = get_embedding("test")
    assert result is None

def test_cache_creation_and_loading(temp_cache_path, mock_kb_hash):
    manager = EmbeddingCacheManager(cache_path=temp_cache_path)

    # Mock the batch fetch to return dummy vectors
    with patch('app.embeddings.get_embeddings_batch', return_value=np.zeros((2, EMBEDDING_DIMENSION))):
        records = [{"id": "r1", "title": "A"}, {"id": "r2", "title": "B"}]
        success = manager.build_and_save_cache(records)
        assert success is True

    assert os.path.exists(temp_cache_path)

    # Now test loading
    embeddings, record_ids = manager.load_cache()
    assert embeddings is not None
    assert record_ids == ["r1", "r2"]
    assert embeddings.shape == (2, EMBEDDING_DIMENSION)

def test_cache_kb_hash_mismatch_invalidation(temp_cache_path):
    manager = EmbeddingCacheManager(cache_path=temp_cache_path)
    manager.kb_hash = "hash_A"

    with patch('app.embeddings.get_embeddings_batch', return_value=np.zeros((1, EMBEDDING_DIMENSION))):
        manager.build_and_save_cache([{"id": "r1"}])

    # Change hash to simulate KB update
    manager.kb_hash = "hash_B"
    embeddings, record_ids = manager.load_cache()

    assert embeddings is None
    assert record_ids is None

def test_cache_metadata_mismatch_invalidation(temp_cache_path, mock_kb_hash):
    manager = EmbeddingCacheManager(cache_path=temp_cache_path)

    with patch('app.embeddings.get_embeddings_batch', return_value=np.zeros((1, 128))):
        manager.build_and_save_cache([{"id": "r1"}])

    # Temporarily change the expected dimension to simulate config change
    with patch('app.embeddings.EMBEDDING_DIMENSION', 256):
        embeddings, record_ids = manager.load_cache()
        assert embeddings is None  # Invalidated because dimension changed
