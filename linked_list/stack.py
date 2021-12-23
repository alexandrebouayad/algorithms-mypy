from linked_list._base import SingleLinkNode as Node


class Stack:
    """Implementation of a stack (LIFO) based on a singly linked list for
    storage."""

    def __init__(self):
        """Create an empty stack."""
        self._head = None  # head node of the linked list
        self._size = 0  # number of elements in the stack

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def push(self, element):
        """Add element to the top of the stack."""
        self._head = Node(element, self._head)  # create and link a new node
        self._size += 1

    def top(self):
        """Return without removing the element at the top of the stack.

        Raise IndexError if the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._head.element  # top corresponds to list's head

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise IndexError if the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        element = self._head.element
        self._head = self._head.next  # shift head of the linked list
        self._size -= 1
        return element
