import os
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.store.singlestore import SingleStore


singlestore_vector_store = SingleStore.connect(
    index_name=os.getenv("SINGLESTOREDB_TABLE"),
    id_key="chunk_id",
)


def singlestore_retriever_builder(
    chat_args: ChatArgs, search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return singlestore_vector_store.as_retriever(search_kwargs=search_kwargs)
