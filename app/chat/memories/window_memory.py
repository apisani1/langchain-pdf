from app.chat.memories.histories.sql_history import SqlMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from app.chat.models import ChatArgs


def window_buffer_memory_builder(chat_args: ChatArgs) -> ConversationBufferWindowMemory:
    return ConversationBufferWindowMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
        k=2,
    )
