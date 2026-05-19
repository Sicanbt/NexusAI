from typing import Optional
from nexus.core.config import NexusConfig


class MemoryStore:
    """
    Persistent memory using ChromaDB (vector) for semantic search
    across sessions. Falls back to in-memory if ChromaDB unavailable.
    """

    def __init__(self, config: NexusConfig):
        self.config = config
        self._client = None
        self._collection = None
        self._fallback = {}
        self._init()

    def _init(self):
        try:
            import chromadb
            self._client = chromadb.PersistentClient(path=self.config.chroma_persist_dir)
            self._collection = self._client.get_or_create_collection("nexus_memory")
        except Exception:
            pass  # fallback to in-memory dict

    async def store(self, task: str, result) -> None:
        import hashlib, datetime
        doc_id = hashlib.md5(task.encode()).hexdigest()
        doc = f"Task: {task}\nResult: {result.report}"
        meta = {"task": task[:200], "confidence": result.confidence, "timestamp": datetime.datetime.utcnow().isoformat()}

        if self._collection:
            self._collection.upsert(ids=[doc_id], documents=[doc], metadatas=[meta])
        else:
            self._fallback[doc_id] = {"doc": doc, "meta": meta}

    async def search(self, query: str, n: int = 3) -> list:
        if self._collection:
            results = self._collection.query(query_texts=[query], n_results=n)
            return results.get("documents", [[]])[0]
        return []
