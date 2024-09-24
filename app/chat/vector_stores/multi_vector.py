import os
from typing import (
    Any,
    Optional,
)

from langchain.schema import BaseRetriever
from langchainX.embedding import Embedding
from langchainX.store.multi_vectorstore import (
    LocalMultiVectorStore,
    MultiVectorStore,
)


from langchainX.model import get_chat
from app.chat.models import ChatArgs


def _process_params(kwargs: dict) -> dict:
    if "functor" in kwargs and isinstance(kwargs["functor"], list):
        functor_list = []
        for functor in kwargs["functor"]:
            if isinstance(functor, list):
                functor_list.append((functor[0], functor[1]))
            else:
                functor_list.append(functor)
        kwargs["functor"] = functor_list
    if "llm" in kwargs:
        llm = get_chat(**kwargs["llm"])
        kwargs["llm"] = llm
    return kwargs


def multi_vector_store_builder(
    splitter_name, embedding_name: str, embedding: Embedding, **kwargs: Any
) -> MultiVectorStore:
    return LocalMultiVectorStore(
        data_folder=os.getenv("MULTI_VECTOR_INDEX_NAME", "embeddings/multi_vector")
        + "-"
        + splitter_name
        + "-"
        + embedding_name,
        vectorstore_kwargs={"embedding": embedding},
        **_process_params(kwargs),
    )


def multi_vector_retriever_builder(
    chat_args: ChatArgs,
    splitter_name: str,
    embedding_name: str,
    search_type: str = "similarity",
    search_kwargs: Optional[dict] = None,
) -> BaseRetriever:
    from app.chat.config import chat_config

    search_kwargs = search_kwargs or {}
    search_kwargs.update({"filter": {"doc_id": chat_args.pdf_id}})
    return chat_config.vector_store_map[splitter_name]["multi_vector"][
        embedding_name
    ].as_retriever(search_type=search_type, search_kwargs=search_kwargs)
