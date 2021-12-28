from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from linked_list._single import Node as _Node

_T = TypeVar("_T")


class CircularQueue(Generic[_T]):
    """
    Circular queue (FIFO) based on singly linked list.

    >>> queue = CircularQueue()
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
    CircularQueue(5 <- 9 <- 'Python')
    >>> queue.peek()
    5
    >>> len(queue)
    3
    >>> queue.dequeue()
    5
    >>> queue.enqueue('algorithms')
    >>> queue.rotate()
    >>> queue
    CircularQueue('Python' <- 'algorithms' <- 9)
    >>> queue.dequeue()
    'Python'
    >>> queue.dequeue()
    'algorithms'
    >>> queue.dequeue()
    9
    >>> queue.is_empty()
    True
    >>> queue.dequeue()
    Traceback (most recent call last):
        ...
    IndexError: dequeue from empty queue
    """

    def __init__(self) -> None:
        """Initialise empty queue."""
        self._tail: _Node[_T] | None = None  # tail node of the underlying list
        self._size: int = 0  # number of items in the queue

    def __repr__(self) -> str:
        list_str = " <- ".join([repr(item) for item in self])
        return f"CircularQueue({list_str})"

    def __iter__(self) -> Iterator[_T]:
        """
        Generate iterator for traversing this queue.

        >>> queue = CircularQueue()
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
        if self._tail is None:
            # list is empty
            return
        node = self._tail.next  # head node
        while node is not self._tail:
            assert node is not None  # helper for static type checking
            yield node.data
            node = node.next
        yield node.data

    def __len__(self) -> int:
        """
        Return the number of items in this queue.

        >>> queue = CircularQueue()
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

        >>> queue = CircularQueue()
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

        >>> queue = CircularQueue()
        >>> queue.enqueue("Python")
        >>> queue.enqueue("Java")
        >>> queue.enqueue("C")
        >>> queue
        CircularQueue('Python' <- 'Java' <- 'C')
        """
        new_node = _Node(item)
        if self._tail is None:
            # list is empty
            new_node.next = new_node  # set circularity
        else:
            new_node.next = self._tail.next  # link new node to head
            self._tail.next = new_node
        self._tail = new_node
        self._size += 1

    def dequeue(self) -> _T:
        """Remove and return item from the front of this queue.

        Raise IndexError if the queue is empty.

        >>> queue = CircularQueue()
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
        if self._tail is None:
            raise IndexError("dequeue from empty queue")
        head = self._tail.next
        assert head is not None  # helper for static type checking
        item = head.data  # item to return
        self._tail.next = head.next  # shift head
        self._size -= 1
        if self.is_empty():
            # queue becomes empty
            self._tail = None
        return item

    def rotate(self) -> None:
        """
        Move item from the front to the back of this queue.

        >>> queue = CircularQueue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue
        CircularQueue(0 <- 1 <- 2)
        >>> queue.rotate()
        >>> queue
        CircularQueue(1 <- 2 <- 0)
        >>> queue.rotate()
        >>> queue
        CircularQueue(2 <- 0 <- 1)
        >>> queue.rotate()
        >>> queue
        CircularQueue(0 <- 1 <- 2)
        """
        if self._tail is None:
            # if list is empty, do nothing
            return
        self._tail = self._tail.next  # former head becomes new tail

    def peek(self) -> _T:
        """
        Return without removing the item at the front of this queue.

        Raise IndexError if the queue is empty.

        >>> queue = CircularQueue()
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
        if self._tail is None:
            raise IndexError("peek from empty queue")
        head = self._tail.next
        assert head is not None  # helper for static type checking
        return head.data

    def clear(self) -> None:
        """
        Clear this queue.

        >>> queue = CircularQueue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.is_empty()
        False
        >>> queue.clear()
        >>> queue.is_empty()
        True
        >>> queue
        CircularQueue()
        """
        self._tail = None
        self._size = 0
