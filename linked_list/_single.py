from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Single link node."""

    __slots__ = "data", "next"  # improve memory usage

    def __init__(self, data: T, *, next: Node[T] | None = None):
        self.data = data
        self.next = next
