from .buffer_memory import buffer_memory_builder
from .window_memory import window_buffer_memory_builder


memory_map = {
    "buffer_memory": buffer_memory_builder,
    "window_memory": window_buffer_memory_builder,
}
