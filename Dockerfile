FROM python:3.11-slim
WORKDIR '/chat_pdf'
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
RUN chmod 1777 /tmp
COPY . .
ENV PYTHONPATH="/chat_pdf:/chat_pdf/langchainX:${PYTHONPATH}"
