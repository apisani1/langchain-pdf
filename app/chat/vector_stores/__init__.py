from ..config import chat_config

retriever_map = chat_config.retriever_map

import os
from pprint import pformat
from ..logger import logger

if os.getenv("APP_ENV") == "development":
    logger.info(">" * 50)
    logger.info("Available splitters:\n" + pformat(chat_config.splitter_map))
    logger.info("-" * 50)
    logger.info("Available embeddings:\n" + pformat(chat_config.embedding_map))
    logger.info("-" * 50)
    logger.info("Available vector stores:\n" + pformat(chat_config.vector_stores))
    logger.info("-" * 50)
    logger.info("Available retrievers: \n" + pformat(retriever_map))
    logger.info("<" * 50)
