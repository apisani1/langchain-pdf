from queue import Queue
from threading import Thread
from typing import (
    Any,
    Optional,
)

from flask import current_app
from langchain_core.runnables.config import RunnableConfig

from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
    def stream(
        self,
        input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ):
        config = config or RunnableConfig()
        queue = Queue()
        handler = StreamingHandler(queue)
        if "callbacks" in config:
            config["callbacks"].append(handler)
        else:
            config["callbacks"] = [handler]

        def task(app_context):
            app_context.push()  # push Flask app context to use in the new thread
            self.invoke(input, config=config)

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
