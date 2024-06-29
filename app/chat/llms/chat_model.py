from langchain.chat_models.base import BaseChatModel
from langchainX.model import get_chat

from app.chat.models import ChatArgs


def build_llm(chat_args: ChatArgs) -> BaseChatModel:
    return get_chat()
