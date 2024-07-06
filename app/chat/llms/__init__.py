from functools import partial

from .openai import build_openai_llm


llm_map = {
    "gpt-4": partial(build_openai_llm, model_kwargs={"model_name": "gpt-4"}),
    "gpt-3.5-turbo": partial(build_openai_llm, model_kwargs={"model_name": "gpt-3.5-turbo"}),
}
