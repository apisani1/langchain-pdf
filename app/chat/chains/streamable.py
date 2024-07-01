from queue import Queue
from threading import Thread

from app.chat.callbacks.stream import StreamingHandler
from flask import current_app


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()  # push Flask app context to use in the new thread
            self.invoke(input, config={"callbacks": [handler]})

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
