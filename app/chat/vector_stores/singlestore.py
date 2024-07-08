import os   # noqa: F401
from typing import Optional

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.store.singlestore import SingleStore  # noqa: F401


# singlestore_vector_stores = [SingleStore.connect(
#     index_name=os.getenv("SINGLESTOREDB_TABLE"),
#     host=os.getenv("SINGLESTOREDB_HOST"),
#     database=os.getenv("SINGLESTOREDB_DATABASE"),
#     id_key="chunk_id",
# )]

singlestore_vector_stores = None


def singlestore_retriever_builder(
    chat_args: ChatArgs, search_kwargs: Optional[dict] = None
) -> BaseRetriever:
    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return singlestore_vector_stores[0].as_retriever(search_kwargs=search_kwargs)
