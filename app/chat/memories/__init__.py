from ..config import chat_config


memory_map = chat_config.build_map("memory")

import os
from pprint import pformat
from ..logger import logger

if os.getenv("APP_ENV") == "development":
    logger.info(">" * 50)
    logger.info("Available chat memories: \n" + pformat(memory_map))
    logger.info("<" * 50)
