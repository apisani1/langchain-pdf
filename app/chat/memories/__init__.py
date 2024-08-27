from ..config import chat_config


memory_map = chat_config.build_map("memory")

from pprint import pprint
import os

if os.getenv("APP_ENV") == "development":
    print("-" * 50)
    print("Available chat memories:")
    pprint(memory_map)
    print("-" * 50)
