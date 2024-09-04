import os  # noqa: F401
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.singlestore import SingleStore


def singlestore_vector_store_builder(
    splitter_name: str, embedding_name: str, embedding: Embedding
) -> SingleStore:
    return SingleStore.connect(
        index_name=os.getenv("SINGLESTOREDB_TABLE")
        + "_"
        + splitter_name
        + "-"
        + embedding_name,
        host=os.getenv("SINGLESTOREDB_HOST"),
        database=os.getenv("SINGLESTOREDB_DATABASE"),
        embedding=embedding,
        id_key="chunk_id",
    )


def singlestore_retriever_builder(
    chat_args: ChatArgs, splitter_name: str, embedding_name: str, search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    from app.chat.config import chat_config

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map[splitter_name]["singlestore"][embedding_name].as_retriever(
        search_kwargs=search_kwargs
    )
