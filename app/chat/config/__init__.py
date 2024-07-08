import importlib
import os
from functools import partial

import yaml  # type: ignore
from langchainX.embedding import Embedding


class ChatConfig:
    def __init__(self, config_file: str):
        with open(config_file) as f:
            self._yaml_data = yaml.safe_load(f)

    @property
    def vector_stores(self):
        return self._vector_stores

    @property
    def vector_store_map(self):
        return self._vector_store_map

    def _init_component(self, component: dict):
        env_variables = component.get("env", {})
        for key, value in env_variables.items():
            os.environ[key] = value
        shell_commands = component.get("shell", [])
        for command in shell_commands:
            os.system(command)

    def _build_embeddings(self):
        embedding_map = {}
        for embedding in self._yaml_data["embedding"]:
            self._init_component(embedding)
            embedding_name = embedding["name"]
            embedding_model = embedding["model"]
            embedding_kwargs = embedding.get("params", {})
            embedding_map[embedding_name] = Embedding(
                model=embedding_model, **embedding_kwargs
            )
        self._embedding_map = embedding_map

    def build_vector_stores(self):
        self._build_embeddings()
        self._vector_stores = []
        self._vector_store_map = {}

        for vector_store in self._yaml_data["vector_store"]:
            self._init_component(vector_store)
            vector_store_name = vector_store["name"]
            vector_store_module = importlib.import_module(vector_store["module"])
            vector_store_builder = getattr(vector_store_module, vector_store["builder"])

            stores = []
            store_map = {}
            for name, embedding in self._embedding_map.items():
                store = vector_store_builder(embedding)
                stores.append(store)
                store_map[name] = store

            self._vector_stores.extend(stores)
            self._vector_store_map[vector_store_name] = store_map

    def build_map(self, component_type: str) -> dict:
        component_map = {}
        for component in self._yaml_data[component_type]:
            self._init_component(component)
            component_name = component["name"]
            component_module = importlib.import_module(component["module"])
            component_builder = getattr(component_module, component["builder"])
            component_kwargs = component.get("params", {})
            if component_kwargs:
                component_map[component_name] = partial(
                    component_builder, **component_kwargs
                )
            else:
                component_map[component_name] = component_builder
        return component_map


chat_config = ChatConfig("./app/chat/config.yaml")
