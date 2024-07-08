import importlib
from functools import partial
from typing import Callable

import yaml  # type: ignore
from langchainX.embedding import Embedding


class ChatConfig:
    def __init__(self, config_file: str):
        with open(config_file) as f:
            self._yaml_data = yaml.safe_load(f)
            self._vector_stores = []
            self._vector_store_map = {}
            self._build_embeddings()

    @property
    def vector_stores(self):
        return self._vector_stores

    @property
    def vector_store_map(self):
        return self._vector_store_map

    def build_map(self, component_type: str) -> dict:
        component_map = {}
        for component in self._yaml_data[component_type]:
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

    def _build_embeddings(self):
        embedding_map = {}
        for embedding in self._yaml_data["embedding"]:
            embedding_name = embedding["name"]
            embedding_model = embedding["model"]
            embedding_kwargs = embedding.get("params", {})
            embedding_map[embedding_name] = Embedding(
                model=embedding_model, **embedding_kwargs
            )
        self._embedding_map = embedding_map

    def build_vector_stores(
        self, vector_store_name: str, vector_store_builder: Callable
    ) -> dict:
        stores = []
        store_map = {}
        for name, embedding in self._embedding_map.items():
            store = vector_store_builder(embedding)
            stores.append(store)
            store_map[name] = store
        self._vector_stores.extend(stores)
        self._vector_store_map[vector_store_name] = store_map
        return stores, store_map


chat_config = ChatConfig("./app/chat/config.yaml")
