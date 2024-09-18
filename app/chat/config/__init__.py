import importlib
import os
from functools import (
    cached_property,
    partial,
)

import yaml  # type: ignore
from dotenv import (
    find_dotenv,
    load_dotenv,
)

from langchainX.embedding import Embedding


load_dotenv(find_dotenv(), override=True)


class ChatConfig:
    def __init__(self, config_file: str):
        with open(config_file) as f:
            self._yaml_data = yaml.safe_load(f)

    @cached_property
    def splitter_map(self):
        return self._build_map("text_splitter")

    @cached_property
    def llm_map(self):
        return self._build_map("llm")

    @cached_property
    def embedding_map(self):
        return self._build_embeddings()

    @cached_property
    def vector_store_map(self):
        return self._build_vector_store_map()

    @cached_property
    def vector_stores(self):
        return self._build_vector_store_list()

    @cached_property
    def retriever_map(self):
        return self._build_map("retriever")

    @cached_property
    def memory_map(self):
        return self._build_map("memory")

    @cached_property
    def condense_question_llm_kwargs(self):
        chain_config = self._yaml_data.get("chain", {})
        return chain_config.get("condense_question_llm", {})

    def _init_component(self, component: dict):
        env_variables = component.get("env", {})
        for key, value in env_variables.items():
            os.environ[key] = value
        shell_commands = component.get("shell", [])
        for command in shell_commands:
            os.system(command)

    def _build_map(self, component_type: str) -> dict:
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

    def _build_embeddings(self) -> dict:
        embedding_map = {}
        for embedding in self._yaml_data["embedding"]:
            self._init_component(embedding)
            embedding_name = embedding["name"]
            embedding_model = embedding["model"]
            embedding_kwargs = embedding.get("params", {})
            embedding_map[embedding_name] = Embedding(
                model=embedding_model, **embedding_kwargs
            )
        return embedding_map

    def _build_vector_store_map(self) -> dict:
        vector_store_map = {}
        for splitter_name in self.splitter_map.keys():
            store_map_level2 = {}
            for vector_store in self._yaml_data["vector_store"]:
                self._init_component(vector_store)
                vector_store_name = vector_store["name"]
                vector_store_module = importlib.import_module(vector_store["module"])
                vector_store_builder = getattr(
                    vector_store_module, vector_store["builder"]
                )
                store_map_level3 = {}
                for embedding_name, embedding in self.embedding_map.items():
                    store = vector_store_builder(
                        splitter_name, embedding_name, embedding
                    )
                    store_map_level3[embedding_name] = store
                store_map_level2[vector_store_name] = store_map_level3
            vector_store_map[splitter_name] = store_map_level2
        return vector_store_map

    def _build_vector_store_list(self) -> dict:
        used_vector_stores = {}
        for retriever in self._yaml_data["retriever"]:
            vector_store_name = retriever["module"].split(".")[-1]
            retriever_params = retriever.get("params", {})
            embedding_name = retriever_params["embedding_name"]
            splitter_name = retriever_params["splitter_name"]
            if splitter_name not in used_vector_stores:
                used_vector_stores[splitter_name] = []
            used_vector_stores[splitter_name].append(
                self.vector_store_map[splitter_name][vector_store_name][embedding_name]
            )
        return used_vector_stores


chat_config = ChatConfig("./app/chat/config.yaml")
