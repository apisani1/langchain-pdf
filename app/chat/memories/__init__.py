from pprint import pprint

from ..config import chat_config


memory_map = chat_config.build_map("memory")

pprint(memory_map)
