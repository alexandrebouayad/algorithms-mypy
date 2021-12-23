from linked_list._base import SingleLinkNode as Node


class Queue:
    """Implementation of a queue (FIFO) based on a singly linked list for
    storage."""

    def __init__(self):
        """Create an empty queue."""
        self._head = None  # head node of the linked list
        self._tail = None  # tail node of the linked list
        self._size = 0  # number of elements in the queue

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return without removing the element at the front of the queue.

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._head.element  # front corresponds to list's head

    def enqueue(self, element):
        """Add element to the back of the queue."""
        new_node = Node(element, None)  # node will be new tail node
        if self.is_empty():  # special case: queue was previously empty
            self._head = new_node
        else:
            self._tail.next = new_node
        self._tail = new_node  # Shift tail
        self._size += 1

    def dequeue(self):
        """Remove and return element from the front of the queue (i.e., FIFO).

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        element = self._head.element
        self._head = self._head.next  # Shift head
        self._size -= 1
        if self.is_empty():  # special case: queue becomes empty
            self._tail = None
        return element
