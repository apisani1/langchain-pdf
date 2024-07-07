from pprint import pprint

from ..config import chat_config
from .pinecone import pinecone_vector_store
from .singlestore import singlestore_vector_store  # noqa: F401


vector_stores = [
    pinecone_vector_store,
    # singlestore_vector_store
]


retriever_map = chat_config.build_map("retriever")

pprint(retriever_map)
