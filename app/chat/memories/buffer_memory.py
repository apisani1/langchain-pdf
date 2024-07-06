from app.chat.memories.histories.sql_history import SqlMessageHistory
from app.chat.models import ChatArgs
from langchain.memory import ConversationBufferMemory


def buffer_memory_builder(chat_args: ChatArgs) -> ConversationBufferMemory:
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
    )
