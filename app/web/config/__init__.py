import os

from dotenv import (
    find_dotenv,
    load_dotenv,
)


load_dotenv(find_dotenv(), override=True)


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or os.environ["DATABASE_URL"]
    UPLOAD_URL = os.environ["UPLOAD_URL"]
    DOWNLOAD_URL = os.environ["DOWNLOAD_URL"]
    CELERY = {
        "broker_url": os.environ.get("REDIS_URI", False),
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
    }
