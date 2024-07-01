from langchain.chat_models.base import BaseChatModel
from langchainX.model import get_chat

from app.chat.models import ChatArgs


def build_llm(chat_args: ChatArgs, **kwargs) -> BaseChatModel:
    if hasattr(chat_args, 'chat_model'):
        chat_name = chat_args.chat_model
    else:
        chat_name = "OpenAI"
    if hasattr(chat_args, 'model_kwargs'):
        model_kwargs = chat_args.model_kwargs
    else:
        model_kwargs = {}
    if "streaming" in kwargs:
        streaming = kwargs['streaming']
    else:
        streaming = chat_args.streaming
    return get_chat(chat_name=chat_name, streaming=streaming, **model_kwargs)
