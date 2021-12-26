from __future__ import annotations

from typing import Any, Iterator

from linked_list.singly_linked import Node


class LinkedStack:
    """
    Stack (LIFO) based on singly linked list.

    >>> stack = LinkedStack()
    >>> stack.is_empty()
    True
    >>> stack.push(5)
    >>> stack.push(9)
    >>> stack.push('python')
    >>> stack.is_empty()
    False
    >>> len(stack)
    3
    >>> stack
    LinkedStack('python' -> 9 -> 5)
    >>> stack.pop()
    'python'
    >>> stack.push('algorithms')
    >>> stack.pop()
    'algorithms'
    >>> stack.pop()
    9
    >>> stack.pop()
    5
    >>> stack.is_empty()
    True
    >>> stack.pop()
    Traceback (most recent call last):
        ...
    IndexError: pop from empty stack
    """

    def __init__(self):
        """Create an empty stack."""
        self._head = None  # head node of the underlying list
        self._size = 0  # number of elements in the stack

    def __repr__(self) -> str:
        list_str = " -> ".join([repr(item) for item in self])
        return f"LinkedStack({list_str})"

    def __iter__(self) -> Iterator:
        """
        Generate iterator for traversing this stack

        >>> stack = LinkedStack()
        >>> stack.push(0)
        >>> stack.push(1)
        >>> stack.push(2)
        >>> for item in stack:
        ...     print(item)
        2
        1
        0
        """
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __len__(self) -> int:
        """
        Return the number of elements in this stack.

        >>> stack = LinkedStack()
        >>> len(stack) == 0
        True
        >>> stack.push(0)
        >>> stack.push(1)
        >>> stack.push(2)
        >>> len(stack)
        3
        >>> stack.pop()
        2
        >>> stack.pop()
        1
        >>> len(stack)
        1
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Return True if this stack is empty.

        >>> stack = LinkedStack()
        >>> stack.is_empty()
        True
        >>> stack.push(0)
        >>> stack.push(1)
        >>> stack.is_empty()
        False
        """
        return self._size == 0

    def push(self, item: Any) -> None:
        """
        Add item to the top of this stack.

        >>> stack = LinkedStack()
        >>> stack.push("Python")
        >>> stack.push("Java")
        >>> stack.push("C")
        >>> stack
        LinkedStack('C' -> 'Java' -> 'Python')
        """
        self._head = Node(item, next=self._head)
        self._size += 1

    def pop(self) -> Any:
        """
        Remove and return the item from the top of this stack.

        Raise IndexError if the stack is empty.

        >>> stack = LinkedStack()
        >>> stack.pop()
        Traceback (most recent call last):
        ...
        IndexError: pop from empty stack
        >>> stack.push(0)
        >>> stack.push(1)
        >>> stack.pop()
        1
        >>> stack.pop()
        0
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        top_item = self._head.data
        self._head = self._head.next  # shift head
        self._size -= 1
        return top_item

    def peek(self) -> Any:
        """
        Return without removing the element at the top of this stack.

        Raise IndexError if the stack is empty.

        >>> stack = LinkedStack()
        >>> stack.peek()
        Traceback (most recent call last):
        ...
        IndexError: peek from empty stack
        >>> stack.push("Java")
        >>> stack.push("C")
        >>> stack.push("Python")
        >>> stack.peek()
        'Python'
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.data

    def clear(self) -> None:
        """
        Clear the stack.

        >>> stack = LinkedStack()
        >>> stack.push(0)
        >>> stack.push(1)
        >>> stack.is_empty()
        False
        >>> stack.clear()
        >>> stack.is_empty()
        True
        >>> stack
        LinkedStack()
        """
        self._head = None
        self._size = 0
