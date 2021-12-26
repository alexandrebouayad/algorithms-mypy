from __future__ import annotations

from typing import Any


class Node:
    """Lightweight class for storing a double link node."""

    __slots__ = "data", "prev", "next"  # improve memory usage

    def __init__(
        self,
        data: Any,
        *,
        # linked nodes
        prev: Node | None = None,
        next: Node | None = None,
    ):
        """
        Create and initialize Node class instance.
        >>> Node("Hello, world!")
        Node(Hello, world!)
        >>> prev_node = Node(-1)
        >>> next_node = Node(1)
        >>> node = Node(0, prev=prev_node, next=next_node)
        >>> prev_node, node, next_node
        (Node(-1), Node(0), Node(1))
        """
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.data})"


class DoublyLinkedBase:
    """Implementation of a doubly linked list."""

    def __init__(self):
        """Create an empty list."""
        # initialise sentinel nodes
        self._header = Node()
        self._trailer = Node()

        # initialise empty list
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._size = 0  # number of elements in the list

    @property
    def _head(self):
        return self._header.next

    @property
    def _tail(self):
        return self._trailer.prev

    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if list is empty."""
        return self._size == 0

    def _insert_between(self, element, prev_node, next_node):
        """Add element between two existing nodes and return new node."""
        new_node = Node(element, prev_node, next_node)
        prev_node.next = new_node
        next_node.prev = new_node
        self._size += 1
        return new_node

    def _delete_node(self, node):
        """Delete non-sentinel node from the list and return its element.

        Raise IndexError if node is a sentinel node.
        """
        if node in (self._header, self._trailer):
            raise IndexError("Cannot delete a sentinel node.")
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self._size -= 1
        return node.element  # return element of the deleted node
