# import os
# import pinecone
# from langchain.vectorstores.pinecone import Pinecone
# from app.chat.embeddings.openai import embeddings

# pinecone.Pinecone(
#     api_key=os.getenv("PINECONE_API_KEY"),
#     environment=os.getenv("PINECONE_ENV_NAME")
# )

# vector_store = Pinecone.from_existing_index(
#     os.getenv("PINECONE_INDEX_NAME"), embeddings
# )

# def build_retriever(chat_args):
#     search_kwargs = {"filter": { "pdf_id": chat_args.pdf_id }}
#     return vector_store.as_retriever(
#         search_kwargs=search_kwargs
#     )

import os

from app.chat.models import ChatArgs
from langchain.schema import BaseRetriever
from langchainX.store.pinecone_store import PineconeStore


vector_store = PineconeStore.connect(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    namespace=os.getenv("PINECONE_NAMESPACE"),
)


def build_retriever(chat_args: ChatArgs) -> BaseRetriever:
    search_kwargs = {"filter": {"doc_id": chat_args.doc_id}}
    return vector_store.as_retriever(search_kwargs=search_kwargs)
