from linked_list.doubly_linked import DoublyLinkedBase


class LinkedDeque(DoublyLinkedBase):
    """Implementation of a double-ended queue based on a doubly linked list."""

    def first(self):
        """Return without removing the element at the front of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._head.element

    def last(self):
        """Return without removing the element at the back of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._tail.element

    def insert_first(self, element):
        """Add element to the front of the deque."""
        self._insert_between(element, self._header, self._head)

    def insert_last(self, element):
        """Add element to the back of the deque."""
        self._insert_between(element, self._tail, self._trailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._delete_node(self._head)  # remove head

    def delete_last(self):
        """Remove and return the element from the back of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._delete_node(self._tail)  # remove tail
