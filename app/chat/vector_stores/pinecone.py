import os
from typing import Optional

from app.chat.models import ChatArgs
from app.chat.config import chat_config
from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.pinecone_store import PineconeStore


def pinecone_vector_store_builder(embedding: Embedding) -> PineconeStore:
    return PineconeStore.connect(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        namespace=os.getenv("PINECONE_NAMESPACE"),
        embedding=embedding,
    )


def pinecone_retriever_builder(
    chat_args: ChatArgs, search_kwargs: Optional[dict] = None
) -> BaseRetriever:

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map["pinecone"]["openai"].as_retriever(
        search_kwargs=search_kwargs
    )
