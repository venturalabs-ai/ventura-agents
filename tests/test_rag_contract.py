from ast import ClassDef, FunctionDef, parse
from pathlib import Path


def test_rag_pipeline_exposes_core_contract():
    source = Path("src/rag/pipeline.py").read_text(encoding="utf-8")
    module = parse(source)
    classes = {node.name: node for node in module.body if isinstance(node, ClassDef)}

    assert {"ChunkingStrategy", "Document", "RetrievalResult", "RAGPipeline"} <= classes.keys()
    methods = {
        node.name
        for node in classes["RAGPipeline"].body
        if isinstance(node, FunctionDef)
    }
    assert {"ingest_documents", "retrieve", "assemble_context"} <= methods
