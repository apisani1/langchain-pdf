import os

from dotenv import (
    find_dotenv,
    load_dotenv,
)


load_dotenv(find_dotenv(), override=True)

print(">>>> Tracing: ", os.environ["LANGCHAIN_TRACING_V2"])
print(">>>> API KEY: ", os.environ["LANGCHAIN_API_KEY"])
print(">>>> Endpoint: ", os.environ["LANGCHAIN_ENDPOINT"])
print(">>>> Project: ", os.environ["LANGCHAIN_PROJECT"])


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    UPLOAD_URL = os.environ["UPLOAD_URL"]
    CELERY = {
        "broker_url": os.environ.get("REDIS_URI", False),
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
    }
