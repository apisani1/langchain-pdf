from ..config import chat_config


llm_map = chat_config.build_map("llm")

import os
from pprint import pformat
from ..logger import logger

if os.getenv("APP_ENV") == "development":
    logger.info(">" * 50)
    logger.info("Available chat models:\n" + pformat(llm_map))
    logger.info("<" * 50)
