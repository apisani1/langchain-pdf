import importlib
import os
from functools import partial

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
        self._condense_question_llm_kwargs = None
        self._splitter_map = None
        self._llm_map = None
        self._embedding_map = None
        self._vector_stores = None
        self._vector_store_map = None
        self._retriever_map = None
        self._memory_map = None

    @property
    def document_splitters(self):
        if self._splitter_map is None:
            self._splitter_map = self._build_map("text_splitter")
        return self._splitter_map

    @property
    def llm_map(self):
        if self._llm_map is None:
            self._llm_map = self._build_map("llm")
        return self._llm_map

    @property
    def embedding_map(self):
        if self._embedding_map is None:
            self._embedding_map = self._build_embeddings()
        return self._embedding_map

    @property
    def vector_stores(self):
        if self._vector_stores is None:
            self._vector_stores = self._build_vector_store_list()
        return self._vector_stores

    @property
    def vector_store_map(self):
        if self._vector_store_map is None:
            self._vector_store_map = self._build_vector_store_map()
        return self._vector_store_map

    @property
    def retriever_map(self):
        if self._retriever_map is None:
            self._retriever_map = self._build_map("retriever")
        return self._retriever_map

    @property
    def memory_map(self):
        if self._memory_map is None:
            self._memory_map = self._build_map("memory")
        return self._memory_map

    @property
    def condense_question_llm_kwargs(self):
        if self._condense_question_llm_kwargs is None:
            chain_config = self._yaml_data.get("chain", {})
            self._condense_question_llm_kwargs = chain_config.get(
                "condense_question_llm", {}
            )
        return self._condense_question_llm_kwargs

    def _init_component(self, component: dict):
        env_variables = component.get("env", {})
        for key, value in env_variables.items():
            os.environ[key] = value
        shell_commands = component.get("shell", [])
        for command in shell_commands:
            os.system(command)

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
        for splitter_name in self.document_splitters.keys():

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


chat_config = ChatConfig("./app/chat/config.yaml")
