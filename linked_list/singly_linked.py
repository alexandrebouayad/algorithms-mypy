from __future__ import annotations

from typing import Any


class Node:
    """
    Lightweight class for storing a single link node.

    >>> Node("Hello, world!")
    Node(Hello, world!)
    >>> next_node = Node(1)
    >>> node = Node(0, next=next_node)
    >>> node, node.next
    (Node(0), Node(1))
    """

    __slots__ = "data", "next"  # improve memory usage

    def __init__(
        self,
        data: Any,
        *,
        next: Node | None = None,  # linked node
    ):
        self.data = data
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.data})"
