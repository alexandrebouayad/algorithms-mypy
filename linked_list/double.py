from __future__ import annotations

from typing import Any, Iterator


class Node:
    """
    Lightweight class for storing double link node.

    >>> Node('Hello, world!')
    Node('Hello, world!')
    >>> prev_node = Node(-1)
    >>> next_node = Node(1)
    >>> node = Node(0, prev=prev_node, next=next_node)
    >>> prev_node, node, next_node
    (Node(-1), Node(0), Node(1))
    """

    __slots__ = "data", "prev", "next"  # improve memory usage

    def __init__(
        self,
        data: Any,
        *,
        # linked nodes
        prev: Node | None = None,
        next: Node | None = None,
    ):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        item_str = repr(self.data)
        return f"Node({item_str})"


class DoublyLinkedBase:
    """
    Doubly linked list.

    >>> lst = DoublyLinkedBase()
    >>> lst.is_empty()
    True
    >>> lst._insert(5, lst._header, lst._trailer)
    Node(5)
    >>> lst._insert('Python', lst._head, lst._trailer)
    Node('Python')
    >>> node = lst._insert(9, lst._head, lst._tail)
    >>> lst.is_empty()
    False
    >>> len(lst)
    3
    >>> lst
    DoublyLinkedBase(5 <-> 9 <-> 'Python')
    >>> lst._head
    Node(5)
    >>> len(lst)
    3
    >>> lst._tail
    Node('Python')
    >>> len(lst)
    3
    >>> lst._remove(node)
    9
    >>> lst._insert('algorithms', lst._tail, lst._trailer)
    Node('algorithms')
    >>> lst
    DoublyLinkedBase(5 <-> 'Python' <-> 'algorithms')
    >>> lst._remove(lst._head)
    5
    >>> lst._remove(lst._header)
    Traceback (most recent call last):
    ...
    IndexError: remove sentinel node
    >>> lst._remove(lst._head)
    'Python'
    >>> lst._remove(lst._head)
    'algorithms'
    >>> lst.is_empty()
    True
    """

    def __init__(self):
        """Create an empty list."""
        # initialise sentinel nodes
        self._header = Node(None)
        self._trailer = Node(None)

        # initialise empty list
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._size = 0  # number of items in the list

    @property
    def _head(self) -> Node:  # head node
        return self._header.next

    @property
    def _tail(self) -> Node:  # tail node
        return self._trailer.prev

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_head":
            self._header.next = value
            return
        if name == "_tail":
            self._trailer.prev = value
            return
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        list_str = " <-> ".join([repr(item) for item in self])
        return f"{class_name}({list_str})"

    def __iter__(self) -> Iterator:
        """
        Generate iterator for traversing this list.

        >>> lst = DoublyLinkedBase()
        >>> lst._insert(0, lst._header, lst._trailer)
        Node(0)
        >>> lst._insert(2, lst._head, lst._trailer)
        Node(2)
        >>> lst._insert(1, lst._head, lst._tail)
        Node(1)
        >>> for item in lst:
        ...     print(item)
        0
        1
        2
        >>> lst.clear()
        >>> for item in lst:
        ...     print(item)
        """
        node = self._header.next
        while node is not self._trailer:
            yield node.data
            node = node.next

    def __len__(self) -> int:
        """
        Return the number of items in this list.

        >>> lst = DoublyLinkedBase()
        >>> len(lst)
        0
        >>> lst._insert(0, lst._header, lst._trailer)
        Node(0)
        >>> lst._insert(2, lst._head, lst._trailer)
        Node(2)
        >>> lst._insert(1, lst._head, lst._tail)
        Node(1)
        >>> len(lst)
        3
        >>> lst._remove(lst._head)
        0
        >>> lst._remove(lst._tail)
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
        >>> lst._insert(0, lst._header, lst._trailer)
        Node(0)
        >>> lst._insert(1, lst._head, lst._trailer)
        Node(1)
        >>> lst.is_empty()
        False
        """
        return self._size == 0

    def _insert(self, item: Any, prev_node: Node, next_node: Node) -> Node:
        """
        Insert item between prev_node and next_node, and return new node.

        >>> lst = DoublyLinkedBase()
        >>> lst._insert('Python', lst._header, lst._trailer)
        Node('Python')
        >>> lst._insert('C', lst._head, lst._trailer)
        Node('C')
        >>> lst._insert('Java', lst._head, lst._tail)
        Node('Java')
        >>> lst
        DoublyLinkedBase('Python' <-> 'Java' <-> 'C')
        """
        new_node = Node(item, prev=prev_node, next=next_node)
        prev_node.next = new_node
        next_node.prev = new_node
        self._size += 1
        return new_node

    def _remove(self, node: Node) -> Any:
        """
        Delete node from this list and return node's item.

        Raise IndexError if node is a sentinel node.

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
        >>> lst._insert(0, lst._header, lst._trailer)
        Node(0)
        >>> lst._insert(2, lst._head, lst._trailer)
        Node(2)
        >>> node = lst._insert(1, lst._head, lst._tail)
        >>> lst._remove(node)
        1
        >>> node.prev
        >>> node.next
        >>> lst._remove(lst._head)
        0
        """
        if node in (self._header, self._trailer):
            raise IndexError("remove sentinel node")
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None  # deprecate node
        self._size -= 1
        return node.data  # return item of the removed node

    def clear(self) -> None:
        """
        Clear this list.

        >>> lst = DoublyLinkedBase()
        >>> lst._insert(0, lst._header, lst._trailer)
        Node(0)
        >>> lst._insert(2, lst._head, lst._trailer)
        Node(2)
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


class Position:
    """
    Abstraction representing the location of a single item.

    Note that two positions may represent the same inherent location in the
    list. Use 'p == q' rather than 'p is q' when testing equivalence of
    positions.

    >>> lst = DoublyLinkedBase()
    >>> lst._insert(0, lst._header, lst._trailer)
    Node(0)
    >>> lst._insert(1, lst._head, lst._trailer)
    Node(1)
    >>> lst._insert(0, lst._tail, lst._trailer)
    Node(0)
    >>> position = Position(lst._head, list=lst)
    >>> position
    Position(0)
    >>> position_2 = Position(lst._tail, list=lst)
    >>> position == position_2
    False
    >>> position_2 = Position(lst._head, list=lst)
    >>> position == position_2
    True
    >>> lst_2 = DoublyLinkedBase()
    >>> lst_2._insert(0, lst._header, lst._trailer)
    Node(0)
    >>> position_2 = Position(lst._head, list=lst_2)
    >>> position == position_2
    False
    """

    __slots__ = "_node", "_list"  # improve memory usage

    def __init__(self, node: Node, *, list: DoublyLinkedBase | None = None):
        self._node = node
        self._list = list

    @property
    def item(self) -> Any:
        """Return the item stored at this position."""
        return self._node.data

    def __repr__(self) -> str:
        item_repr = repr(self.item)
        return f"Position({item_repr})"

    def __eq__(self, other: Position) -> bool:
        """Return True if the two positions represent the same location."""
        if not isinstance(other, Position):
            return False
        return self._list == other._list and self._node == other._node
