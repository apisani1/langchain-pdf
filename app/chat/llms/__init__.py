from functools import partial

from .chat_model import build_llm


# To use VertexAI models you need to authenticate with your Google Cloud account.
# run 'gcloud auth login' in your terminal

llm_map = {
    # "gpt-4": partial(
    #     build_llm, chat_name="OpenAI", model_kwargs={"model_name": "gpt-4"}
    # ),
    "gpt-3.5-turbo": partial(
        build_llm, chat_name="OpenAI", model_kwargs={"model_name": "gpt-3.5-turbo"}
    ),
    # "chat-bison": partial(
    #     build_llm, chat_name="VertexAI", model_kwargs={"model_name": "chat-bison"}
    # )
}
