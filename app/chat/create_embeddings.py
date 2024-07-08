from app.chat.config import chat_config
from langchainX.document import load_document


def create_embeddings_for_pdf(doc_id: str, file_path: str, doc_name: str = ""):
    """
    Generate and store embeddings for the given document.

    1. Extract text from the specified document.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param doc_id: The unique identifier for the document.
    :param file_path: The file path to the document.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
    """
    docs = load_document(
        file_path,
        mode="paged",
        strategy="fast",
        chunk_it=True,
        chunk_size=500,
        chunk_overlap=100,
    )

    if not docs:
        raise ValueError("No chunk of text found in the document.")

    for doc in docs:
        doc.metadata = {
            "page": doc.metadata["page_number"],
            "doc_id": doc_id,
            "source": doc_name,
        }

    for vector_store in chat_config.vector_stores:
        vector_store.add_documents(docs, id_key="chunk_id")
