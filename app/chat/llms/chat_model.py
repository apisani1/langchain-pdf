from langchain.chat_models.base import BaseChatModel
from langchainX.model import get_chat

from app.chat.models import ChatArgs


def build_llm(
    chat_args: ChatArgs,
    chat_name: str = "OpenAI",
    **kwargs
) -> BaseChatModel:
    if "streaming" in kwargs:
        streaming = kwargs.pop("streaming")
    else:
        streaming = chat_args.streaming
    return get_chat(chat_name=chat_name, streaming=streaming, **kwargs)
