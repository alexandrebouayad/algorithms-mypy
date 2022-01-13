import ctypes
from typing import Any


class DynamicArray:
    """Dynamic array akin to a simplified Python list."""

    def __init__(self) -> None:
        """Create an empty array."""
        self._n = 0  # number of actual elements
        self._capacity = 1  # array capacity
        self._array = self._make_array(self._capacity)  # low-level array

    def __len__(self) -> int:
        """Return the number of elements stored in this array."""
        return self._n

    def __getitem__(self, k: int) -> Any:
        """
        Return element at index k.

        Raise an error if invalid index.
        """
        if not isinstance(k, int):
            raise TypeError("index must be an integer")
        if not 0 <= k < self._n:
            raise IndexError("index out of range")
        return self._array[k]  # retrieve from internal array

    def _resize(self, c: int) -> None:
        """Resize internal array to capacity c."""
        new_array = self._make_array(c)

        # copy elements to new array
        for k in range(self._n):
            new_array[k] = self._array[k]

        self._array = new_array
        self._capacity = c

    def _make_array(self, c: int) -> ctypes.Array[Any]:
        """Create and return low-level array with capacity c."""
        return (c * ctypes.py_object)()

    def insert(self, k: int, element: object) -> None:
        """
        Insert element at index k and shift subsequent elements rightward.

        Raise an error if invalid index.
        """
        if not isinstance(k, int):
            raise TypeError("index must be an integer")
        if not 0 <= k <= self._n:
            raise IndexError("index out of range")
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # double capacity

        # shift elements
        for j in range(k, self._n):
            self._array[j + 1] = self._array[j]

        self._array[k] = element
        self._n += 1

    def append(self, element: object) -> None:
        """Add element to the end of this array."""
        self.insert(self._n, element)

    def remove(self, element: object) -> None:
        """
        Remove first occurrence of element.

        Raise ValueError if element is not found.
        """
        for k in range(self._n):
            if self._array[k] == element:
                for j in range(k, self._n - 1):  # shift to fill gap
                    self._array[j] = self._array[j + 1]
                self._array[self._n - 1] = None  # help garbage collection
                self._n -= 1
                return  # exit immediately
        raise ValueError("element not found")  # only reached if no match
