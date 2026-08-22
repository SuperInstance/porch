"""
porch — A CLI for 3 a.m. thoughts. The small gods, as a tool.

The porch holds. The porch remembers. The porch does not sort.
"""
from .core import Porch, Thought
from .cli import main

__all__ = ["Porch", "Thought", "main"]
__version__ = "0.1.0"
