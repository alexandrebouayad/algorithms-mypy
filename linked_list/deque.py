from linked_list._base import DoublyLinkedBase


class LinkedDeque(DoublyLinkedBase):
    """Implementation of a double-ended queue based on a doubly linked list."""

    def first(self):
        """Return without removing the element at the front of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._header.next.element  # element of the head of the list

    def last(self):
        """Return without removing the element at the back of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._trailer.prev.element  # element of tail of the list

    def insert_first(self, element):
        """Add element to the front of the deque."""
        self._insert_between(element, self._header, self._header.next)

    def insert_last(self, element):
        """Add element to the back of the deque."""
        self._insert_between(element, self._trailer.prev, self._trailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._delete_node(self._header.next)  # remove head

    def delete_last(self):
        """Remove and return the element from the back of the deque.

        Raise IndexError if the deque is empty.
        """
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._delete_node(self._trailer.prev)  # remove tail
