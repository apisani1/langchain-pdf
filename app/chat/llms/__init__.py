

from ..config import chat_config


llm_map = chat_config.build_map("llm")

from pprint import pprint
import os

if os.getenv("APP_ENV") == "development":
    print("-" * 50)
    print("Available chat models:")
    pprint(llm_map)
    print("-" * 50)
