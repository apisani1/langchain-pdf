from pprint import pprint
from typing import Callable

from ..config import chat_config
from .pinecone import pinecone_vector_store_builder


embedding_map = chat_config.build_embeddings()
retriever_map = chat_config.build_map("retriever")
vector_stores = []
vector_store_map = {}


def build_vector_stores(vector_store_name: str, vector_store_builder: Callable) -> dict:
    stores = []
    store_map = {}
    for name, embedding in embedding_map.items():
        store = vector_store_builder(embedding)
        stores.append(store)
        store_map[name] = store
    vector_stores.extend(stores)
    vector_store_map[vector_store_name] = store_map


build_vector_stores("pinecone", pinecone_vector_store_builder)

print("-" * 50)
print("Available embeddings:")
pprint(embedding_map)
print("-" * 50)
print("Available vector stores:")
print(vector_stores)
print("-" * 50)
print("Available retrievers:")
pprint(retriever_map)
print("-" * 50)
