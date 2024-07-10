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

    print("*" * 50)
    print(f"Chat initiatied with components:")
    print(f"LLM: {llm_name}")
    print(f"Retriever: {retriever_name}")
    print(f"Memory: {memory_name}")
    print(f"Condense Question LLM: {chat_config.condense_question_llm_kwargs}")
    print("*" * 50)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        retriever=retriever,
        memory=memory,
    )
