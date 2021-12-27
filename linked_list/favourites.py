from __future__ import annotations

from typing import Any, Iterator

import linked_list.double as double
import linked_list.positional as positional


class _Item:
    __slots__ = "value", "count"  # improve memory usage

    def __init__(self, value):
        self.value = value  # value of the item
        self.count = 0  # access count


class FavouritesList:
    """
    List of items sorted by access frequencies in non-increasing order.

    >>> lst = FavouritesList()
    >>> len(lst)
    0
    >>> lst.is_empty()
    True
    >>> lst.access('Python')
    >>> lst.access(5)
    >>> lst.access('Python')
    >>> lst.access('Python')
    >>> len(lst)
    2
    >>> lst.is_empty()
    False
    >>> lst
    [('Python', 3), (5, 1)]
    >>> lst.access(5)
    >>> lst
    [('Python', 3), (5, 2)]
    >>> for item, count in lst:
    ...     print(item, count)
    Python 3
    5 2
    >>> lst.access(5)
    >>> lst.access(5)
    >>> lst
    [(5, 4), ('Python', 3)]
    >>> lst.access(9)
    >>> for item in lst.top(2):
    ...     print(item)
    5
    Python
    >>> lst.remove(5)
    >>> lst
    [('Python', 3), (9, 1)]
    >>> for item in lst.top(3):
    ...     break
    Traceback (most recent call last):
        ...
    IndexError: list has less than 3 items
    >>> lst.remove(5)
    >>> lst
    [('Python', 3), (9, 1)]
    >>> lst.remove('Python')
    >>> lst.remove(9)
    >>> len(lst)
    0
    >>> lst.is_empty()
    True
    """

    def __init__(self):
        """Create an empty list of favourites."""
        self._list = (
            positional.PositionalList()
        )  # will contain _Item instances

    def __repr__(self) -> str:
        return repr(list(self))

    def __iter__(self) -> Iterator:
        """Return iterator over items with access counts."""
        return ((item.value, item.count) for item in self._list)

    def __len__(self) -> int:
        """Return the number of items in this favourites list."""
        return len(self._list)

    def _find_position(self, item: _Item) -> double.Position:
        """Search for item and return its position or None if not found."""
        position = self._list.first_position()
        while position is not None and position.item.value != item:
            position = self._list.position_after(position)
        return position

    def _move_up(self, position: double.Position) -> None:
        """Move up the item located at position based on access counts."""
        walker = position
        count = position.item.count
        while (
            walker != self._list.first_position()
            and self._list.position_before(walker).item.count < count
        ):
            walker = self._list.position_before(walker)
        self._list.insert_before(walker, position.item)
        self._list.remove(position)

    def is_empty(self) -> bool:
        """Return True if this list is empty."""
        return self._list.is_empty()

    def access(self, item: Any) -> None:
        """Access item and increase its access count."""
        position = self._find_position(item)
        if position is None:
            # if new item, insert at the back of the list
            position = self._list.insert_last(_Item(item))
        position.item.count += 1
        self._move_up(position)

    def remove(self, item: Any) -> None:
        """Remove item from this list."""
        position = self._find_position(item)
        if position is not None:
            # remove item if present
            self._list.remove(position)

    def top(self, k: int) -> Iterator:
        """
        Generate iterator over top k items with respect to access counts.

        Raise IndexError if list has less than k items.
        """
        if k > len(self):
            raise IndexError(f"list has less than {k} items")
        position = self._list.first_position()
        for _ in range(k):
            yield position.item.value
            position = self._list.position_after(position)
