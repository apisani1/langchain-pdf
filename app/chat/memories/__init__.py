from pprint import pprint

from ..config import chat_config


memory_map = chat_config.build_map("memory")

print("-" * 50)
print("Available chat memories:")
pprint(memory_map)
print("-" * 50)
