from langchain.chat_models.base import BaseChatModel
from langchainX.model import get_chat

from app.chat.models import ChatArgs


def build_llm(chat_args: ChatArgs) -> BaseChatModel:
    if hasattr(chat_args, 'chat_model'):
        chat_name = chat_args.chat_model
    else:
        chat_name = "OpenAI"
    if hasattr(chat_args, 'model_kwargs'):
        model_kwargs = chat_args.model_kwargs
    else:
        model_kwargs = {}
    return get_chat(chat_name=chat_name, streaming=chat_args.streaming, **model_kwargs)
