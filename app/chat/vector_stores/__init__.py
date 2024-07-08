from pprint import pprint

from ..config import chat_config
from .pinecone import pinecone_vector_store_builder
from .singlestore import singlestore_vector_store_builder  # noqa: F401


retriever_map = chat_config.build_map("retriever")


chat_config.build_vector_stores("pinecone", pinecone_vector_store_builder)
# build_vector_stores("singlestore", singlestore_vector_store_builder)


print("-" * 50)
print("Available embeddings:")
pprint(chat_config._embedding_map)
print("-" * 50)
print("Available vector stores:")
print(chat_config.vector_stores)
print("-" * 50)
print("Available retrievers:")
pprint(retriever_map)
print("-" * 50)
