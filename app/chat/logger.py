import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


# def setup_logger():
#     os.makedirs("logs", exist_ok=True)
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#         filename="logs/langchain-pdf.log",
#         filemode="a",
#     )
#     return logging.getLogger(__name__)


# def setup_logger():
#     os.makedirs("logs", exist_ok=True)

#     # Create a root logger
#     root_logger = logging.getLogger()
#     root_logger.setLevel(logging.INFO)

#     # Create formatter
#     formatter = logging.Formatter(
#         "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#     )

#     # Handler for your app's logs
#     app_handler = logging.FileHandler("logs/langchain-pdf.log")
#     app_handler.setFormatter(formatter)
#     app_handler.addFilter(lambda record: record.name.startswith(__name__))

#     # Handler for third-party logs
#     third_party_handler = logging.FileHandler("logs/third-party.log")
#     third_party_handler.setFormatter(formatter)
#     third_party_handler.addFilter(lambda record: not record.name.startswith(__name__))

#     # Add handlers to the root logger
#     root_logger.addHandler(app_handler)
#     root_logger.addHandler(third_party_handler)

#     # Create and return a logger for your application
#     app_logger = logging.getLogger(__name__)
#     return app_logger


def setup_logger():
    os.makedirs("logs", exist_ok=True)

    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler for your app's logs
    app_handler = TimedRotatingFileHandler(
        filename="logs/langchain-pdf.log",
        when="midnight",
        interval=1,
        backupCount=30,  # Keep logs for 30 days
    )
    app_handler.setFormatter(formatter)
    app_handler.addFilter(lambda record: record.name.startswith(__name__))
    app_handler.namer = (
        lambda name: name.replace(".log", "")
        + "."
        + datetime.now().strftime("%Y-%m-%d")
        + ".log"
    )

    # Handler for third-party logs
    third_party_handler = TimedRotatingFileHandler(
        filename="logs/third-party.log",
        when="midnight",
        interval=1,
        backupCount=30,  # Keep logs for 30 days
    )
    third_party_handler.setFormatter(formatter)
    third_party_handler.addFilter(lambda record: not record.name.startswith(__name__))
    third_party_handler.namer = (
        lambda name: name.replace(".log", "")
        + "."
        + datetime.now().strftime("%Y-%m-%d")
        + ".log"
    )

    # Add handlers to the root logger
    root_logger.addHandler(app_handler)
    root_logger.addHandler(third_party_handler)

    # Create and return a logger for your application
    app_logger = logging.getLogger(__name__)
    return app_logger


logger = setup_logger()
