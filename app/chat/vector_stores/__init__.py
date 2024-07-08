from pprint import pprint

from ..config import chat_config


chat_config.build_embeddings()
chat_config.build_vector_stores()
retriever_map = chat_config.build_map("retriever")


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
