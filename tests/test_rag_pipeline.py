import numpy as np
import pytest

from src.rag.pipeline import ChunkingStrategy, Document, RAGPipeline


def _pipeline(**kwargs) -> RAGPipeline:
    return RAGPipeline(chunking_strategy=ChunkingStrategy.FIXED_SIZE, **kwargs)


def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        RAGPipeline(chunk_size=100, chunk_overlap=100)


def test_fixed_size_chunking_skips_tiny_chunks():
    pipeline = _pipeline(chunk_size=100, chunk_overlap=10)
    doc = Document(id="doc1", content="x" * 260, metadata={})
    chunks = pipeline._chunk_fixed_size(doc)
    assert chunks
    assert all(len(c.content) <= 100 for c in chunks)
    assert all(chunk.id.startswith("doc1_chunk_") for chunk in chunks)


def test_recursive_chunking_respects_max_size():
    pipeline = _pipeline(chunk_size=80, chunk_overlap=10)
    content = "\n\n".join(
        f"This is paragraph number {i} with meaningful words." for i in range(30)
    )
    doc = Document(id="doc2", content=content, metadata={})
    chunks = pipeline._chunk_recursive(doc)
    assert chunks
    assert all(len(c.content) <= 80 for c in chunks)
    assert all(len(c.content) >= 50 for c in chunks)


def test_structure_chunking_splits_headings():
    pipeline = _pipeline()
    content = (
        "# Intro\n" + "Overview of the document body content here.\n\n"
        "# Sales\n" + "Quarterly sales grew strongly across all regions.\n\n"
        "# Taxes\n" + "Fiscal obligations are reconciled every month."
    )
    doc = Document(id="doc3", content=content, metadata={})
    chunks = pipeline._chunk_by_structure(doc)
    assert len(chunks) >= 3
    assert any("# Intro" in c.content for c in chunks)
    assert any("# Sales" in c.content for c in chunks)


def test_semantic_chunking_groups_similar_sentences(monkeypatch):
    pipeline = _pipeline()
    embeddings = [np.array([1.0, 0.0]), np.array([0.9, 0.1]), np.array([0.0, 1.0])]
    monkeypatch.setattr(pipeline, "_generate_embeddings", lambda texts: embeddings[: len(texts)])
    doc = Document(id="doc4", content="alpha beta. gamma delta. epsilon zeta.", metadata={})
    chunks = pipeline._chunk_semantic(doc)
    assert len(chunks) == 2
    assert "alpha beta" in chunks[0].content and "gamma delta" in chunks[0].content
    assert "epsilon zeta" in chunks[1].content


def test_assemble_context_respects_token_budget():
    pipeline = _pipeline()
    results = []
    for i in range(10):
        doc = Document(id=f"r{i}", content="word " * 200, metadata={"source": f"s{i}"})
        results.append(_RetrievalResult(doc, 0.9 - i / 100, i + 1))
    context = pipeline.assemble_context("query", results, max_tokens=200)
    assert len(context) < 200 * 4


def test_rerank_is_deterministic_and_orders_by_overlap():
    pipeline = _pipeline()
    results = {
        "ids": [["a", "b", "c"]],
        "documents": [["alpha beta", "beta delta", "gamma"]],
        "metadatas": [[{}, {}, {}]],
        "distances": [[0.1, 0.3, 0.2]],
    }
    ranked = pipeline._rerank("gamma", results, top_k=2)
    assert ranked["ids"][0] == ["c", "a"]
    assert ranked["documents"][0] == ["gamma", "alpha beta"]


class _RetrievalResult:
    def __init__(self, document, score, rank):
        self.document = document
        self.score = score
        self.rank = rank


class _FakeCollection:
    def __init__(self, docs):
        self._docs = docs
        self.added = None

    def query(self, query_embeddings, n_results, where=None):
        return {
            "ids": [[d[0] for d in self._docs]],
            "documents": [[d[1] for d in self._docs]],
            "metadatas": [[d[2] for d in self._docs]],
            "distances": [[d[3] for d in self._docs]],
        }

    def add(self, **kwargs):
        self.added = kwargs


class _FakeChroma:
    def __init__(self):
        self.collections = {}

    def get_or_create_collection(self, name, metadata=None):
        if name not in self.collections:
            self.collections[name] = _FakeCollection([])
        return self.collections[name]

    def get_collection(self, name):
        return self.collections[name]


@pytest.fixture
def fake_env(monkeypatch):
    chroma = _FakeChroma()
    chroma.collections["kb"] = _FakeCollection(
        [
            ("a", "alpha beta", {}, 0.1),
            ("b", "beta delta", {}, 0.3),
            ("c", "gamma", {}, 0.2),
        ]
    )
    monkeypatch.setattr(RAGPipeline, "chroma_client", chroma, raising=False)
    monkeypatch.setattr(
        RAGPipeline,
        "_generate_embeddings",
        lambda self, texts: [np.zeros(4) for _ in texts],
    )
    return chroma


def test_retrieve_truncates_when_rerank_disabled(fake_env):
    pipeline = _pipeline()
    results = pipeline.retrieve("gamma", collection_name="kb", top_k=2, rerank=False)
    assert [r.document.id for r in results] == ["a", "b"]


def test_retrieve_reranks_and_truncates(fake_env):
    pipeline = _pipeline()
    results = pipeline.retrieve("gamma", collection_name="kb", top_k=2, rerank=True)
    assert [r.document.id for r in results] == ["c", "a"]
    assert results[0].rank == 1


def test_ingest_adds_embeddings(fake_env):
    pipeline = _pipeline()
    doc = Document(id="doc5", content="word " * 100, metadata={})
    pipeline.ingest_documents([doc], collection_name="kb")
    added = fake_env.collections["kb"].added
    assert added is not None
    assert len(added["ids"]) == 1
    assert len(added["embeddings"]) == 1
