from __future__ import annotations

from typing import Any, Iterator

from linked_list.singly_linked import Node


class LinkedQueue:
    """
    Queue (FIFO) based on singly linked list.

    >>> queue = LinkedQueue()
    >>> queue.is_empty()
    True
    >>> queue.enqueue(5)
    >>> queue.enqueue(9)
    >>> queue.enqueue('python')
    >>> queue.is_empty()
    False
    >>> len(queue)
    3
    >>> queue
    LinkedQueue(5 <- 9 <- 'python')
    >>> queue.dequeue()
    5
    >>> queue.enqueue('algorithms')
    >>> queue.dequeue()
    9
    >>> queue.dequeue()
    'python'
    >>> queue.dequeue()
    'algorithms'
    >>> queue.is_empty()
    True
    >>> queue.dequeue()
    Traceback (most recent call last):
        ...
    IndexError: dequeue from empty queue
    """

    def __init__(self):
        """Create an empty queue."""
        self._header = Node(None)  # sentinel node of the underlying list
        self._tail = self._header  # queue is initialised empty
        self._size = 0  # number of elements in the queue

    @property
    def _head(self) -> Node | None:  # head node of the underlying list
        return self._header.next

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_head":
            self._header.next = value
            return
        super().__setattr__(name, value)

    def __repr__(self) -> str:
        list_str = " <- ".join([repr(item) for item in self])
        return f"LinkedQueue({list_str})"

    def __iter__(self) -> Iterator:
        """
        Generate iterator for traversing this queue

        >>> queue = LinkedQueue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> for item in queue:
        ...     print(item)
        0
        1
        2
        """
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __len__(self) -> int:
        """
        Return the number of elements in this queue.

        >>> queue = LinkedQueue()
        >>> len(queue) == 0
        True
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

        >>> queue = LinkedQueue()
        >>> queue.is_empty()
        True
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.is_empty()
        False
        """
        return self._size == 0

    def enqueue(self, item: Any) -> None:
        """
        Add item to the back of this queue.

        >>> queue = LinkedQueue()
        >>> queue.enqueue("Python")
        >>> queue.enqueue("Java")
        >>> queue.enqueue("C")
        >>> queue
        LinkedQueue('Python' <- 'Java' <- 'C')
        """
        # create new tail node
        new_node = Node(item)
        self._tail.next = new_node
        self._tail = new_node

        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return item from the front of this queue.

        Raise IndexError if the queue is empty.

        >>> queue = LinkedQueue()
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
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._head.data  # item to return
        self._head = self._head.next  # shift head
        self._size -= 1
        if self.is_empty():
            # special case: queue becomes empty
            self._tail = self._header
        return item

    def clear(self) -> None:
        """
        Clear the queue.

        >>> queue = LinkedQueue()
        >>> queue.enqueue(0)
        >>> queue.enqueue(1)
        >>> queue.is_empty()
        False
        >>> queue.clear()
        >>> queue.is_empty()
        True
        >>> queue
        LinkedQueue()
        """
        self._head = None
        self._tail = self._header
        self._size = 0
