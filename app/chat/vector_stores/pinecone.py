import os
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.pinecone_store import PineconeStore


def pinecone_vector_store_builder(
    splitter_name: str, embedding_name: str, embedding: Embedding
) -> PineconeStore:
    return PineconeStore.connect(
        index_name=os.getenv("PINECONE_INDEX_NAME")
        + "-"
        + splitter_name
        + "-"
        + embedding_name,
        namespace=os.getenv("PINECONE_NAMESPACE"),
        embedding=embedding,
    )


def pinecone_retriever_builder(
    chat_args: ChatArgs,
    splitter_name: str,
    embedding_name: str,
    search_kwargs: Optional[dict] = None,
) -> BaseRetriever:
    from app.chat.config import chat_config

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map[splitter_name]["pinecone"][embedding_name].as_retriever(
        search_kwargs=search_kwargs
    )
