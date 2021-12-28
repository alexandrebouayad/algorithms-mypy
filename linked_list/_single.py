from __future__ import annotations

from typing import Generic, TypeVar

_T = TypeVar("_T")


class Node(Generic[_T]):
    """Single link node."""

    __slots__ = "data", "next"  # improve memory usage

    def __init__(self, data: _T, *, next: Node[_T] | None = None):
        self.data = data
        self.next = next
