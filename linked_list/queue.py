from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from linked_list._single import Node as _Node

_T = TypeVar("_T")


class Queue(Generic[_T]):
    """
    Queue (FIFO) based on singly linked list.

    >>> queue = Queue()
    >>> queue.is_empty()
    True
    >>> queue.enqueue(5)
    >>> queue.enqueue(9)
    >>> queue.enqueue('Python')
    >>> queue.is_empty()
    False
    >>> len(queue)
    3
    >>> queue
    Queue(5 <- 9 <- 'Python')
    >>> queue.peek()
    5
    >>> len(queue)
    3
    >>> queue.dequeue()
    5
    >>> queue.enqueue('algorithms')
    >>> queue.dequeue()
    9
    >>> queue.dequeue()
    'Python'
    >>> queue.dequeue()
    'algorithms'
    >>> queue.is_empty()
    True
    >>> queue.dequeue()
    Traceback (most recent call last):
        ...
    IndexError: dequeue from empty queue
    """

    def __init__(self) -> None:
        """Initialise empty queue."""
        self._head: _Node[_T] | None = None  # head node of the underlying list
        self._tail: _Node[_T] | None = None  # tail node of the underlying list
        self._size = 0  # number of items in the queue

    def __repr__(self) -> str:
        list_str = " <- ".join([repr(item) for item in self])
        return f"Queue({list_str})"

    def __iter__(self) -> Iterator[_T]:
        """
        Generate iterator for traversing this queue.

        >>> queue = Queue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> for item in queue:
        ...     print(item)
        0
        1
        2
        >>> queue.clear()
        >>> for item in queue:
        ...     print(item)
        """
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __len__(self) -> int:
        """
        Return the number of items in this queue.

        >>> queue = Queue()
        >>> len(queue)
        0
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> len(queue)
        3
        >>> queue.dequeue()
        0
        >>> queue.dequeue()
        1
        >>> len(queue)
        1
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Return True if this queue is empty.

        >>> queue = Queue()
        >>> queue.is_empty()
        True
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.is_empty()
        False
        """
        return self._size == 0

    def enqueue(self, item: _T) -> None:
        """
        Add item to the back of this queue.

        >>> queue = Queue()
        >>> queue.enqueue("Python")
        >>> queue.enqueue("Java")
        >>> queue.enqueue("C")
        >>> queue
        Queue('Python' <- 'Java' <- 'C')
        """
        new_node = _Node(item)
        if self._tail is None:
            # list is empty
            self._head = new_node
        else:
            self._tail.next = new_node
        self._tail = new_node
        self._size += 1

    def dequeue(self) -> _T:
        """Remove and return item from the front of this queue.

        Raise IndexError if the queue is empty.

        >>> queue = Queue()
        >>> queue.dequeue()
        Traceback (most recent call last):
        ...
        IndexError: dequeue from empty queue
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.dequeue()
        0
        >>> queue.dequeue()
        1
        """
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        item = self._head.data  # item to return
        self._head = self._head.next  # shift head
        self._size -= 1
        if self.is_empty():
            # special case: queue becomes empty
            self._tail = None
        return item

    def peek(self) -> _T:
        """
        Return without removing the item at the front of this queue.

        Raise IndexError if the queue is empty.

        >>> queue = Queue()
        >>> queue.peek()
        Traceback (most recent call last):
        ...
        IndexError: peek from empty queue
        >>> queue.enqueue("Java")
        >>> queue.enqueue("C")
        >>> queue.enqueue("Python")
        >>> queue.peek()
        'Java'
        """
        if self._head is None:
            raise IndexError("peek from empty queue")
        return self._head.data

    def clear(self) -> None:
        """
        Clear this queue.

        >>> queue = Queue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.is_empty()
        False
        >>> queue.clear()
        >>> queue.is_empty()
        True
        >>> queue
        Queue()
        """
        self._head = self._tail = None
        self._size = 0
