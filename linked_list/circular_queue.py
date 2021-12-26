from linked_list import SingleLinkNode as Node


class CircularQueue:
    """Implementation of a queue based on a circularly linked list for storage."""

    def __init__(self):
        """Create an empty queue."""
        self._tail = None  # tail node of the linked list
        self._size = 0  # number of elements in the queue

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    @property
    def _head(self):
        # tail is linked to head (circularity)
        return None if self.is_empty() else self._tail.next

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return without removing the element at the front of the queue.

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._head.element

    def enqueue(self, element):
        """Add element to the back of the queue."""
        new_node = Node(element, None)
        if self.is_empty():  # special case: queue was previously empty
            new_node.next = new_node  # initialise circularity
        else:
            new_node.next = self._head  # link new node to head
            self._tail.next = new_node  # link former head to new node
            self._tail = new_node  # shift tail
            self._size += 1

    def dequeue(self):
        """Remove and return the element at the front of the queue (i.e., FIFO).

        Raise IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        element = self._head.element
        self._tail.next = self._head.next  # shift head
        self._size -= 1
        if self.is_empty():  # special case: queue becomes empty
            self._tail = None
        return element

    def rotate(self):
        """Move element from the front to the back of the queue."""
        self._tail = self._head  # former head becomes tail
