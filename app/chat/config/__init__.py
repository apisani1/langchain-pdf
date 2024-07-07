import importlib
from functools import partial

import yaml  # type: ignore


class ChatConfig:
    def __init__(self, config_file: str):
        with open(config_file) as f:
            self.yaml_data = yaml.safe_load(f)

    def build_map(self, component_type: str) -> dict:
        component_map = {}
        for component in self.yaml_data[component_type]:
            component_name = component["name"]
            component_module = importlib.import_module(component["module"])
            component_builder = getattr(component_module, component["builder"])
            component_kwargs = component.get("params", {})
            if component_kwargs:
                component_map[component_name] = partial(component_builder, **component_kwargs)
            else:
                component_map[component_name] = component_builder
        return component_map


chat_config = ChatConfig("./app/chat/config.yaml")
