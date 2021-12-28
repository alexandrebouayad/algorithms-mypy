from __future__ import annotations

from typing import TypeVar

from linked_list._double import DoublyLinkedBase as _DoublyLinkedBase
from linked_list._double import Header as _Header
from linked_list._double import Trailer as _Trailer

T = TypeVar("T")


class Deque(_DoublyLinkedBase[T]):
    """
    Deque (double-ended queue) based on doubly linked list.

    >>> deque = Deque()
    >>> deque.is_empty()
    True
    >>> deque.insert_first(5)
    >>> deque.insert_last(9)
    >>> deque.insert_first('Python')
    >>> deque.is_empty()
    False
    >>> len(deque)
    3
    >>> deque
    Deque('Python' <-> 5 <-> 9)
    >>> deque.peek_first()
    'Python'
    >>> len(deque)
    3
    >>> deque.remove_last()
    9
    >>> deque.insert_last('algorithms')
    >>> deque
    Deque('Python' <-> 5 <-> 'algorithms')
    >>> deque.remove_first()
    'Python'
    >>> deque.remove_last()
    'algorithms'
    >>> deque.remove_first()
    5
    >>> deque.is_empty()
    True
    >>> deque.remove_first()
    Traceback (most recent call last):
        ...
    IndexError: remove from empty deque
    """

    def insert_first(self, item: T) -> None:
        """
        Add item to the front of this deque.

        >>> deque = Deque()
        >>> deque.insert_first("Python")
        >>> deque.insert_first("Java")
        >>> deque.insert_first("C")
        >>> deque
        Deque('C' <-> 'Java' <-> 'Python')
        """
        self._insert(item, self._header, self._header.next)

    def insert_last(self, item: T) -> None:
        """
        Add item to the front of this deque.

        >>> deque = Deque()
        >>> deque.insert_last("Python")
        >>> deque.insert_last("Java")
        >>> deque.insert_last("C")
        >>> deque
        Deque('Python' <-> 'Java' <-> 'C')
        """
        self._insert(item, self._trailer.prev, self._trailer)

    def remove_first(self) -> T:
        """
        Remove and return the item from the front of this deque.

        Raise IndexError if the deque is empty.

        >>> deque = Deque()
        >>> deque.remove_first()
        Traceback (most recent call last):
        ...
        IndexError: remove from empty deque
        >>> deque.insert_first(0)
        >>> deque.insert_last(1)
        >>> deque.remove_first()
        0
        >>> deque.remove_first()
        1
        """
        head = self._header.next  # head node or trailer
        if isinstance(head, _Trailer):
            raise IndexError("remove from empty deque")
        return self._remove(head)

    def remove_last(self) -> T:
        """Remove and return the item from the back of this deque.

        Raise IndexError if the deque is empty.
        >>> deque = Deque()
        >>> deque.remove_last()
        Traceback (most recent call last):
        ...
        IndexError: remove from empty deque
        >>> deque.insert_first(0)
        >>> deque.insert_last(1)
        >>> deque.remove_last()
        1
        >>> deque.remove_last()
        0
        """
        tail = self._trailer.prev  # tail node or header
        if isinstance(tail, _Header):
            raise IndexError("remove from empty deque")
        return self._remove(tail)

    def peek_first(self) -> T:
        """Return without removing the item at the front of this deque.

        Raise IndexError if the deque is empty.
        >>> deque = Deque()
        >>> deque.peek_first()
        Traceback (most recent call last):
        ...
        IndexError: peek from empty deque
        >>> deque.insert_first("Java")
        >>> deque.insert_last("C")
        >>> deque.insert_first("Python")
        >>> deque.peek_first()
        'Python'
        """
        head = self._header.next  # head node or trailer
        if isinstance(head, _Trailer):
            raise IndexError("peek from empty deque")
        return head.data

    def peek_last(self) -> T:
        """Return without removing the item at the back of this deque.

        Raise IndexError if the deque is empty.
        >>> deque = Deque()
        >>> deque.peek_last()
        Traceback (most recent call last):
        ...
        IndexError: peek from empty deque
        >>> deque.insert_first("Java")
        >>> deque.insert_last("C")
        >>> deque.insert_last("Python")
        >>> deque.peek_last()
        'Python'
        """
        tail = self._trailer.prev  # tail node or header
        if isinstance(tail, _Header):
            raise IndexError("peek from empty deque")
        return tail.data
