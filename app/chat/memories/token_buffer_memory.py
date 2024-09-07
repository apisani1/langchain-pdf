from app.chat.llms.chat_model import build_llm
from app.chat.memories.histories.sql_history import SqlMessageHistory
from app.chat.models import ChatArgs
from langchain.memory import ConversationTokenBufferMemory
from typing import Optional


def token_buffer_memory_builder(
    chat_args: ChatArgs,
    model_kwargs: Optional[dict] = None,
    max_token_limit: int = 2000,
) -> ConversationTokenBufferMemory:
    model_kwargs = model_kwargs or {}
    token_llm = build_llm(
        chat_args=chat_args,
        streaming=False,
        **model_kwargs,
    )
    return ConversationTokenBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
        llm=token_llm,
        max_token_limit=max_token_limit,
    )
