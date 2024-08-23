import os
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.chroma_store import ChromaStore


def chroma_vector_store_builder(
    embedding_name: str, embedding: Embedding
) -> ChromaStore:
    return ChromaStore.connect(
        index_name=os.getenv("CHROMA_INDEX_NAME") + "-" + embedding_name,
        embedding=embedding,
    )


def chroma_retriever_builder(
    chat_args: ChatArgs, embedding_name: str, search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    from app.chat.config import chat_config

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map["chroma"][embedding_name].as_retriever(
        search_kwargs=search_kwargs
    )
