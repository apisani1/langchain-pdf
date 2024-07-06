from functools import partial

from .pinecone import (  # noqa: F401
    pinecone_retriever_builder,
    pinecone_vector_store,
)
from .singlestore import (  # noqa: F401
    singlestore_retriever_builder,
    singlestore_vector_store,
)


vector_stores = [pinecone_vector_store, singlestore_vector_store]

retriever_map = {
    "pinecone_1": partial(pinecone_retriever_builder, search_kwargs={"k": 1}),
    "pinecone_2": partial(pinecone_retriever_builder, search_kwargs={"k": 2}),
    "pinecone_3": partial(pinecone_retriever_builder, search_kwargs={"k": 3}),
    # "singlestore_1": partial(singlestore_retriever_builder, search_kwargs={"k": 1}),
    # "singlestore_2": partial(singlestore_retriever_builder, search_kwargs={"k": 2}),
    # "singlestore_3": partial(singlestore_retriever_builder, search_kwargs={"k": 3}),
}
