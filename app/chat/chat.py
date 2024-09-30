from langchain.retrievers.multi_query import MultiQueryRetriever

from app.chat.config import chat_config
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.chat.llms import llm_map
from app.chat.llms.chat_model import build_llm
from app.chat.memories import memory_map
from app.chat.models import ChatArgs
from app.chat.score import random_component_by_score
from app.chat.vector_stores import retriever_map
from app.web.api import (
    get_conversation_components,
    set_conversation_components,
)


def select_component(component_type: str, component_map: dict, chat_args: ChatArgs):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component and previous_component in component_map:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name,
    )

    condense_question_llm = build_llm(
        chat_args, **chat_config.condense_question_llm_kwargs, streaming=False
    )

    if chat_config.multi_query:
        retriever = MultiQueryRetriever.from_llm(
            llm=condense_question_llm,
            retriever=retriever,
            include_original=True
        )

    import os
    from .logger import logger

    if os.getenv("APP_ENV") == "development":
        logger.info(">" * 50)
        logger.info(f"Chat initiatied with components:")
        logger.info(f"LLM: {llm_name}")
        logger.info(f"Chat Type: {chat_config.chain_type}")
        logger.info(f"Max Tokens Limit: {chat_config.max_tokens_limit}")
        logger.info(f"Return Page Numbers: {chat_config.return_page_numbers}")
        logger.info(f"Streaming: {chat_args.streaming}")
        logger.info(f"Retriever: {retriever_name}")
        logger.info(f"Multi Query: {chat_config.multi_query}")
        logger.info(f"Memory: {memory_name}")
        logger.info(
            f"Condense Question LLM: {chat_config.condense_question_llm_kwargs}"
        )
        logger.info("<" * 50)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        retriever=retriever,
        memory=memory,
        chain_type=chat_config.chain_type,
        max_tokens_limit=chat_config.max_tokens_limit,
        return_source_documents=chat_config.return_page_numbers,
    ).with_config(
        {
            "run_id": chat_args.conversation_id,
            "tags": [
                f"llm: {llm_name}",
                f"memory: {memory_name}",
                f"retriever: {retriever_name}",
            ],
            "metadata": {
                "user_id": chat_args.metadata.user_id,
                "pdf_id": chat_args.pdf_id,
                "streaming": chat_args.streaming,
            },
        }
    )
