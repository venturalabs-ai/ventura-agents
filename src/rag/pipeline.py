"""Core RAG pipeline: deterministic chunking, dense retrieval (ChromaDB) and lexical re-ranking.

The pipeline is provider-agnostic by default: OpenAI and ChromaDB clients are
initialized lazily so the module can be imported and pure-logic methods tested
without network access or heavy dependencies.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import numpy as np


class ChunkingStrategy(StrEnum):
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    DOCUMENT_STRUCTURE = "document_structure"


@dataclass
class Document:
    id: str
    content: str
    metadata: dict[str, Any]
    embedding: np.ndarray | None = None


@dataclass
class RetrievalResult:
    document: Document
    score: float
    rank: int


class RAGPipeline:
    """RAG pipeline with deterministic chunking, dense retrieval and re-ranking."""

    def __init__(
        self,
        vector_db_path: str = "./chroma_db",
        embedding_model: str = "text-embedding-3-small",
        chunking_strategy: ChunkingStrategy = ChunkingStrategy.SEMANTIC,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self._vector_db_path = vector_db_path
        self.embedding_model = embedding_model
        self.chunking_strategy = chunking_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._openai_client: Any | None = None
        self._chroma_client: Any | None = None

    @property
    def openai_client(self) -> Any:
        if self._openai_client is None:
            from openai import OpenAI

            self._openai_client = OpenAI()
        return self._openai_client

    @property
    def chroma_client(self) -> Any:
        if self._chroma_client is None:
            import chromadb
            from chromadb.config import Settings

            self._chroma_client = chromadb.PersistentClient(
                path=self._vector_db_path,
                settings=Settings(anonymized_telemetry=False),
            )
        return self._chroma_client

    def ingest_documents(
        self,
        documents: list[Document],
        collection_name: str = "knowledge_base",
    ) -> None:
        """Chunk and store documents in the vector database."""
        collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Enterprise knowledge base"},
        )

        for doc in documents:
            chunks = self._chunk_document(doc)
            embeddings = self._generate_embeddings([c.content for c in chunks])
            collection.add(
                ids=[c.id for c in chunks],
                documents=[c.content for c in chunks],
                embeddings=embeddings,
                metadatas=[c.metadata for c in chunks],
            )

    def retrieve(
        self,
        query: str,
        collection_name: str = "knowledge_base",
        top_k: int = 10,
        rerank: bool = True,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        """Retrieve documents with dense search and optional lexical re-ranking."""
        collection = self.chroma_client.get_collection(collection_name)

        query_embedding = self._generate_embeddings([query])[0]
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2,
            where=filters,
        )

        if rerank:
            results = self._rerank(query, results, top_k)
        else:
            results = {key: [row[:top_k] for row in value] for key, value in results.items()}

        retrieval_results: list[RetrievalResult] = []
        for idx, (doc_id, doc_content, doc_metadata, distance) in enumerate(
            zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
                strict=True,
            )
        ):
            retrieval_results.append(
                RetrievalResult(
                    document=Document(id=doc_id, content=doc_content, metadata=doc_metadata),
                    score=1 - distance,
                    rank=idx + 1,
                )
            )

        return retrieval_results

    def assemble_context(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
        max_tokens: int = 4000,
        include_metadata: bool = True,
    ) -> str:
        """Assemble a context string bounded by a token budget."""
        context_parts = [f"# Context for Query: {query}\n\n"]
        current_tokens = self._estimate_tokens(context_parts[0])

        for result in retrieval_results:
            doc_text = f"## Source {result.rank} (Score: {result.score:.3f})\n\n"

            if include_metadata:
                doc_text += f"**Source:** {result.document.metadata.get('source', 'Unknown')}\n"
                doc_text += f"**Date:** {result.document.metadata.get('date', 'Unknown')}\n\n"

            doc_text += f"{result.document.content}\n\n---\n\n"

            doc_tokens = self._estimate_tokens(doc_text)
            if current_tokens + doc_tokens > max_tokens:
                break

            context_parts.append(doc_text)
            current_tokens += doc_tokens

        return "".join(context_parts)

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    def _chunk_document(self, document: Document) -> list[Document]:
        strategy = self.chunking_strategy
        if strategy == ChunkingStrategy.FIXED_SIZE:
            return self._chunk_fixed_size(document)
        if strategy == ChunkingStrategy.SEMANTIC:
            return self._chunk_semantic(document)
        if strategy == ChunkingStrategy.RECURSIVE:
            return self._chunk_recursive(document)
        return self._chunk_by_structure(document)

    def _make_chunk(self, document: Document, content: str, index: int) -> Document:
        return Document(
            id=f"{document.id}_chunk_{index}",
            content=content,
            metadata={
                **document.metadata,
                "chunk_index": index,
                "parent_doc_id": document.id,
            },
        )

    def _chunk_fixed_size(self, document: Document) -> list[Document]:
        """Fixed-size sliding window with overlap."""
        content = document.content
        step = self.chunk_size - self.chunk_overlap
        chunks: list[Document] = []
        for i in range(0, len(content), step):
            chunk_content = content[i : i + self.chunk_size]
            if len(chunk_content) < 50:
                continue
            chunks.append(self._make_chunk(document, chunk_content, len(chunks)))
        return chunks

    def _chunk_recursive(self, document: Document) -> list[Document]:
        """Recursive splitting by separator priority, respecting size and overlap."""
        separators = ["\n\n", "\n", ". ", " "]
        content = document.content
        chunks: list[Document] = []
        start = 0
        while start < len(content):
            if len(content) - start <= self.chunk_size:
                end = len(content)
            else:
                window = content[start : start + self.chunk_size]
                end = start
                for sep in separators:
                    candidate = window.rfind(sep)
                    if candidate > end:
                        end = start + candidate + len(sep)
                if end == start:
                    end = start + self.chunk_size

            chunk_content = content[start:end].strip()
            if len(chunk_content) >= 50:
                chunks.append(self._make_chunk(document, chunk_content, len(chunks)))

            next_start = end - self.chunk_overlap
            start = next_start if next_start > start else start + 1

        return chunks

    def _chunk_by_structure(self, document: Document) -> list[Document]:
        """Split on markdown heading boundaries; large sections fall back to recursive splitting."""
        lines = document.content.splitlines()
        sections: list[str] = []
        current: list[str] = []
        for line in lines:
            if re.match(r"^#{1,6}\s", line):
                if current:
                    sections.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append("\n".join(current))

        chunks: list[Document] = []
        for section in sections:
            if len(section) <= self.chunk_size and len(section.strip()) >= 50:
                chunks.append(self._make_chunk(document, section.strip(), len(chunks)))
            else:
                section_doc = Document(id=document.id, content=section, metadata=document.metadata)
                chunks.extend(self._chunk_recursive(section_doc))

        renumbered = [
            self._make_chunk(document, chunk.content, i) for i, chunk in enumerate(chunks)
        ]
        return renumbered

    def _chunk_semantic(self, document: Document) -> list[Document]:
        """Semantic chunking using sentence boundaries and embedding similarity."""
        sentences = self._split_sentences(document.content)
        if not sentences:
            return []

        sentence_embeddings = self._generate_embeddings(sentences)

        chunks: list[Document] = []
        current_chunk: list[str] = []
        current_embedding: np.ndarray | None = None

        for sentence, embedding in zip(sentences, sentence_embeddings, strict=True):
            if current_embedding is None:
                current_chunk.append(sentence)
                current_embedding = embedding
            else:
                similarity = float(
                    np.dot(current_embedding, embedding)
                    / (np.linalg.norm(current_embedding) * np.linalg.norm(embedding))
                )
                if similarity > 0.8 and len(" ".join(current_chunk)) < self.chunk_size:
                    current_chunk.append(sentence)
                    current_embedding = (current_embedding + embedding) / 2
                else:
                    chunks.append(self._make_chunk(document, " ".join(current_chunk), len(chunks)))
                    current_chunk = [sentence]
                    current_embedding = embedding

        if current_chunk:
            chunks.append(self._make_chunk(document, " ".join(current_chunk), len(chunks)))

        return chunks

    # ------------------------------------------------------------------
    # Embeddings / re-ranking
    # ------------------------------------------------------------------

    def _generate_embeddings(self, texts: list[str]) -> list[np.ndarray]:
        response = self.openai_client.embeddings.create(
            model=self.embedding_model, input=texts
        )
        return [np.array(data.embedding) for data in response.data]

    def _rerank(self, query: str, results: dict[str, Any], top_k: int) -> dict[str, Any]:
        """Re-ranking determinístico: overlap léxico com a query; empates por distância."""
        ids = (results.get("ids") or [[]])[0]
        documents = (results.get("documents") or [[]])[0]
        metadatas = (results.get("metadatas") or [[]])[0]
        distances = (results.get("distances") or [[]])[0]

        query_tokens = self._tokens(query)
        scored = []
        for doc_id, doc, meta, distance in zip(
            ids, documents, metadatas, distances, strict=True
        ):
            overlap = len(self._tokens(doc) & query_tokens)
            scored.append((overlap, distance, doc_id, doc, meta))

        scored.sort(key=lambda item: (-item[0], item[1]))
        picked = scored[:top_k]

        return {
            "ids": [[item[2] for item in picked]],
            "documents": [[item[3] for item in picked]],
            "metadatas": [[item[4] for item in picked]],
            "distances": [[item[1] for item in picked]],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4

    def _split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9_]+", text.lower()))
