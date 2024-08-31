FROM python:3.11-slim
WORKDIR '/chat_pdf'
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chmod 1777 /tmp
COPY . .
ENV FLASK_APP=wsgi.py
ENV PYTHONPATH="/chat_pdf:/chat_pdf/langchainX:${PYTHONPATH}"
