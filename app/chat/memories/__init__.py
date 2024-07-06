from functools import partial

from .buffer_memory import buffer_memory_builder
from .window_memory import window_buffer_memory_builder
from .summary_memory import summary_buffer_memory_builder


memory_map = {
    "buffer_memory": buffer_memory_builder,
    "window_memory_3": partial(window_buffer_memory_builder, k=3),
    "window_memory_5": partial(window_buffer_memory_builder, k=5),
    "window_memory_7": partial(window_buffer_memory_builder, k=7),
    "summary_memory_1000": partial(summary_buffer_memory_builder, max_token_limit=1000),
    "summary_memory_2000": partial(summary_buffer_memory_builder, max_token_limit=2000),
    "summary_memory_3000": partial(summary_buffer_memory_builder, max_token_limit=3000),
}
