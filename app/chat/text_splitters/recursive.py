from typing import Optional, Callable

from langchain.text_splitter import RecursiveCharacterTextSplitter


def recursive_character_text_splitter_builder(
    chunk_size: int = 4000,
    chunk_overlap: int = 200,
    separators: Optional[list[str]] = None,
    length_function: Callable = len,
    keep_separator: bool = True,
    is_separator_regex: bool = False,
    add_start_index: bool = False,
    strip_whitespace: bool = True,
):
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=length_function,
        keep_separator=keep_separator,
        is_separator_regex=is_separator_regex,
        add_start_index=add_start_index,
        strip_whitespace=strip_whitespace,
    )
