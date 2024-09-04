from typing import Optional

from langchain_experimental.text_splitter import (
    BreakpointThresholdType,
    SemanticChunker,
)

from ..config import chat_config


def semantic_chunker_builder(
    embeddings_name: str,
    buffer_size: int = 1,
    add_start_index: bool = False,
    breakpoint_threshold_type: BreakpointThresholdType = "percentile",
    breakpoint_threshold_amount: Optional[float] = None,
    number_of_chunks: Optional[int] = None,
    sentence_split_regex: str = r"(?<=[.?!])\s+",
):
    return SemanticChunker(
        embeddings=chat_config.embedding_map[embeddings_name],
        buffer_size=buffer_size,
        add_start_index=add_start_index,
        breakpoint_threshold_type=breakpoint_threshold_type,
        breakpoint_threshold_amount=breakpoint_threshold_amount,
        number_of_chunks=number_of_chunks,
        sentence_split_regex=sentence_split_regex,
    )
