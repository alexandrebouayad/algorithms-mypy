from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Header(Generic[T]):
    __slots__ = "next"  # improve memory usage

    def __init__(self) -> None:
        self.next: Node[T] | Trailer[T]


class Trailer(Generic[T]):
    __slots__ = "prev"  # improve memory usage

    def __init__(self) -> None:
        self.prev: Node[T] | Header[T]


class Node(Generic[T]):
    """Double link node."""

    __slots__ = "data", "prev", "next", "deprecated"  # improve memory usage

    def __init__(
        self, data: T, prev: Node[T] | Header[T], next: Node[T] | Trailer[T]
    ):
        self.data = data
        self.prev = prev
        self.next = next
        self.deprecated = False


class DoublyLinkedBase(Generic[T]):
    """
    Doubly linked list.

    >>> lst = DoublyLinkedBase()
    >>> lst.is_empty()
    True
    >>> node_5 = lst._insert(5, lst._header, lst._trailer)
    >>> node_python = lst._insert('Python', node_5, lst._trailer)
    >>> node_9 = lst._insert(9, node_5, node_python)
    >>> lst.is_empty()
    False
    >>> len(lst)
    3
    >>> lst
    DoublyLinkedBase(5 <-> 9 <-> 'Python')
    >>> len(lst)
    3
    >>> len(lst)
    3
    >>> lst._remove(node_9)
    9
    >>> node_algorithms = lst._insert('algorithms', node_python, lst._trailer)
    >>> lst
    DoublyLinkedBase(5 <-> 'Python' <-> 'algorithms')
    >>> lst._remove(node_5)
    5
    >>> lst._remove(lst._header)
    Traceback (most recent call last):
    ...
    IndexError: remove sentinel node
    >>> lst._remove(node_python)
    'Python'
    >>> lst._remove(node_algorithms)
    'algorithms'
    >>> lst.is_empty()
    True
    """

    def __init__(self) -> None:
        """Initialise empty list."""
        # set sentinel nodes
        self._header: Header[T] = Header()
        self._trailer: Trailer[T] = Trailer()
        self._header.next = self._trailer
        self._trailer.prev = self._header

        self._size = 0  # number of items in the list

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        list_str = " <-> ".join([repr(item) for item in self])
        return f"{class_name}({list_str})"

    def __iter__(self) -> Iterator[T]:
        """
        Generate iterator for traversing this list.

        >>> lst = DoublyLinkedBase()
        >>> node_0 = lst._insert(0, lst._header, lst._trailer)
        >>> node_2 = lst._insert(2, node_0, lst._trailer)
        >>> node_1 = lst._insert(1, node_0, node_2)
        >>> list(lst)
        [0, 1, 2]
        >>> lst.clear()
        >>> for item in lst:
        ...     print(item)
        """
        node = self._header.next  # head node or trailer
        while not isinstance(node, Trailer):
            yield node.data
            node = node.next

    def __len__(self) -> int:
        """
        Return the number of items in this list.

        >>> lst = DoublyLinkedBase()
        >>> len(lst)
        0
        >>> node_0 = lst._insert(0, lst._header, lst._trailer)
        >>> node_2 = lst._insert(2, node_0, lst._trailer)
        >>> node_1 = lst._insert(1, node_0, node_2)
        >>> len(lst)
        3
        >>> lst._remove(node_0)
        0
        >>> lst._remove(node_2)
        2
        >>> len(lst)
        1
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Return True if this list is empty.

        >>> lst = DoublyLinkedBase()
        >>> lst.is_empty()
        True
        >>> node_0 = lst._insert(0, lst._header, lst._trailer)
        >>> node_1 = lst._insert(1, node_0, lst._trailer)
        >>> lst.is_empty()
        False
        """
        return self._size == 0

    def _insert(
        self,
        item: T,
        prev_node: Node[T] | Header[T],
        next_node: Node[T] | Trailer[T],
    ) -> Node[T]:
        """
        Insert item between prev_node and next_node, and return new node.

        >>> lst = DoublyLinkedBase()
        >>> node_python = lst._insert('Python', lst._header, lst._trailer)
        >>> node_c = lst._insert('C', node_python, lst._trailer)
        >>> node_java = lst._insert('Java', node_python, node_c)
        >>> lst
        DoublyLinkedBase('Python' <-> 'Java' <-> 'C')
        """
        new_node = Node(item, prev_node, next_node)
        prev_node.next = new_node
        next_node.prev = new_node
        self._size += 1
        return new_node

    def _remove(self, node: Node[T]) -> T:
        """
        Delete node from this list and return node's item.

        Raise IndexError if sentinel node.

        >>> lst = DoublyLinkedBase()
        >>> lst._remove(lst._header)
        Traceback (most recent call last):
        ...
        IndexError: remove sentinel node
        >>> lst = DoublyLinkedBase()
        >>> lst._remove(lst._trailer)
        Traceback (most recent call last):
        ...
        IndexError: remove sentinel node
        >>> node_0 = lst._insert(0, lst._header, lst._trailer)
        >>> node_2 = lst._insert(2, node_0, lst._trailer)
        >>> node_1 = lst._insert(1, node_0, node_2)
        >>> lst._remove(node_1)
        1
        >>> lst._remove(node_0)
        0
        """
        if node in (self._header, self._trailer):
            raise IndexError("remove sentinel node")
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node.data

    def clear(self) -> None:
        """
        Clear this list.

        >>> lst = DoublyLinkedBase()
        >>> node_0 = lst._insert(0, lst._header, lst._trailer)
        >>> node_1 = lst._insert(2, node_0, lst._trailer)
        >>> lst.is_empty()
        False
        >>> lst.clear()
        >>> lst.is_empty()
        True
        >>> lst
        DoublyLinkedBase()
        """
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._size = 0
