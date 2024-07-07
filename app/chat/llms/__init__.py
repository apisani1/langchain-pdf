from pprint import pprint

from ..config import chat_config


llm_map = chat_config.build_map("llm")

pprint(llm_map)
