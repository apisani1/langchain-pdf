import os
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.store.pinecone_store import PineconeStore


pinecone_vector_store = PineconeStore.connect(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    namespace=os.getenv("PINECONE_NAMESPACE"),
)


def pinecone_retriever_builder(
    chat_args: ChatArgs, search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return pinecone_vector_store.as_retriever(search_kwargs=search_kwargs)
