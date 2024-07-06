from app.web.api import (
    add_message_to_conversation,
    get_messages_by_conversation_id,
)
from app.web.db.models import Message
from langchain.pydantic_v1 import BaseModel
from langchain.schema import BaseChatMessageHistory
from langchain.schema.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)


class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    @property
    def messages(self) -> list[AIMessage | HumanMessage | SystemMessage]:
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message) -> Message:
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )

    def clear(self):
        pass
