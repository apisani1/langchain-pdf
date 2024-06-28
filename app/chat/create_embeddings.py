# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from app.chat.vector_stores.pinecone import vector_store
#
#
# def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#   loader = PyPDFLoader(pdf_path)
#   docs = loader.load_and_split(text_splitter)
#   vector_store.add_documents(docs)

from app.chat.vector_stores.pinecone import vector_store
from langchainX.document import load_document


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
    """
    docs = load_document(
        pdf_path, chunk_it=True, chunk_size=500, chunk_overlap=100,
    )

    vector_store.add_documents(docs)
