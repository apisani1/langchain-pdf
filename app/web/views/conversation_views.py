from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from langchain.callbacks.base import BaseCallbackHandler

from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs
from app.chat.config import chat_config
from app.chat.logger import logger

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")


def _answer_with_page_numbers(answer, source_documents):
    source_pages = []
    for doc in source_documents:
        if doc.metadata.get("page") not in source_pages:
            source_pages.append(doc.metadata.get("page"))
    answer += "\n" + "~" * 34 + "\n"
    answer += "Source pages:"
    for page in source_pages:
        answer += f"\n{page}"
    return answer


class SourcePageHandler(BaseCallbackHandler):
    def on_chain_end(self, outputs, **kwargs):
        # logger.info(f">>>>>>on_chain_end: {outputs}")
        pass


@bp.route("/", methods=["GET"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]


@bp.route("/", methods=["POST"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    chat_input = request.json.get("input")
    streaming = request.args.get("stream", False)

    pdf = conversation.pdf

    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "user_id": g.user.id,
            "pdf_id": pdf.id,
        },
    )

    chat = build_chat(chat_args)

    if not chat:
        return "Chat not yet implemented!"

    try:

        if streaming:
            config = {
                "callbacks": [SourcePageHandler()],
            }
            return Response(
                stream_with_context(
                    chat.stream(chat_input, config=config)
                ),
                mimetype="text/event-stream",
            )
        else:
            response = chat.invoke(input={"question": chat_input})
            answer = response["answer"]
            if chat_config.return_page_numbers:
                answer = _answer_with_page_numbers(answer, response.get("source_documents", []))
            return jsonify(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
