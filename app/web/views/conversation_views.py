import time

from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from langchain.callbacks.base import BaseCallbackHandler

from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat import build_chat, ChatArgs
from app.chat.config import chat_config
from app.chat.logger import logger

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")


class _CaptureResponseHandler(BaseCallbackHandler):
    def __init__(self):
        self.source_documents = []

    def on_chain_end(self, outputs, **kwargs):
        if "source_documents" in outputs:
            self.source_documents = outputs["source_documents"]


def _answer_with_page_numbers(answer, source_documents):
    if source_documents:
        source_pages = []
        for doc in source_documents:
            page_number = doc.metadata.get("page")
            if page_number and page_number not in source_pages:
                source_pages.append(page_number)
        if source_pages:
            answer += "\n" + "~" * 34 + "\n"
            answer += "Source pages:"
            for page_number in source_pages:
                answer += f"\n{page_number}"
    return answer


def _stream_with_page_numbers(chain, chat_input, timeout=5):
    response_handler = _CaptureResponseHandler()
    config = {
        "callbacks": [response_handler],
    }
    for token in chain.stream(chat_input, config=config):
        yield token
    start_time = time.time()
    while not response_handler.source_documents:
        if time.time() - start_time > timeout:
            logger.warning(
                f"Timeout reached after {timeout} seconds while waiting for source documents"
            )
            break

        import os

        if os.getenv("APP_ENV") == "development":
            logger.info("waiting for source documents")

        time.sleep(0.1)
    yield _answer_with_page_numbers("", response_handler.source_documents)


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
    try:
        if streaming:
            return Response(
                stream_with_context(
                    _stream_with_page_numbers(chat, chat_input)
                    if chat_config.return_page_numbers
                    else chat.stream(chat_input)
                ),
                mimetype="text/event-stream",
            )
        response = chat.invoke(input={"question": chat_input})
        answer = response["answer"]
        if chat_config.return_page_numbers:
            answer = _answer_with_page_numbers(
                answer, response.get("source_documents", [])
            )
        return jsonify(
            {
                "role": "assistant",
                "content": answer,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
