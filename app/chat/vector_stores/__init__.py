from functools import partial

from .pinecone import (
    pinecone_retriever_builder,
    pinecone_vector_store,
)

vector_stores = [pinecone_vector_store]

retriever_map = {
    "pinecone_1": partial(pinecone_retriever_builder, search_kwargs={"k": 1}),
    "pinecone_2": partial(pinecone_retriever_builder, search_kwargs={"k": 2}),
    "pinecone_3": partial(pinecone_retriever_builder, search_kwargs={"k": 3}),
}
