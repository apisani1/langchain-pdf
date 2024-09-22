import os
from typing import (
    Any,
    Optional,
)

from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.chroma_store import ChromaStore

from app.chat.models import ChatArgs


def chroma_vector_store_builder(
    splitter_name,
    embedding_name: str,
    embedding: Embedding,
    **kwargs: Any,
) -> ChromaStore:
    return ChromaStore.connect(
        index_name=os.getenv("CHROMA_INDEX_NAME", "embeddings/chroma")
        + "-"
        + splitter_name
        + "-"
        + embedding_name,
        embedding=embedding,
        **kwargs,
    )


def chroma_retriever_builder(
    chat_args: ChatArgs,
    splitter_name: str,
    embedding_name: str,
    search_kwargs: Optional[dict] = None,
) -> BaseRetriever:
    from app.chat.config import chat_config

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map[splitter_name]["chroma"][
        embedding_name
    ].as_retriever(search_kwargs=search_kwargs)
