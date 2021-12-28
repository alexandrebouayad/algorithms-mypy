from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from linked_list.positional import Position, PositionalList

_T = TypeVar("_T")


class _Item(Generic[_T]):
    __slots__ = "value", "count"  # improve memory usage

    def __init__(self, value: _T) -> None:
        self.value = value  # value of the item
        self.count = 0  # access count


class FavouritesList(Generic[_T]):
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
    >>> list(lst.top(2))
    [5, 'Python']
    >>> lst.remove(5)
    >>> lst
    [('Python', 3), (9, 1)]
    >>> list(lst.top(3))
    ['Python', 9]
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

    def __init__(self) -> None:
        """Create an empty list of favourites."""
        self._list: PositionalList[_Item[_T]] = PositionalList()

    def __repr__(self) -> str:
        return repr(list(self))

    def __iter__(self) -> Iterator[tuple[_T, int]]:
        """Return iterator over items with access counts."""
        return ((item.value, item.count) for item in self._list)

    def __len__(self) -> int:
        """Return the number of items in this favourites list."""
        return len(self._list)

    def _find_position(self, item: _T) -> Position[_Item[_T]] | None:
        """Search for item and return its position, or None if not found."""
        position = self._list.first_position()
        while position is not None and position.item.value != item:
            position = self._list.position_after(position)
        return position

    def _move_up(self, position: Position[_Item[_T]]) -> None:
        """Move up the item located at position based on access counts."""
        walker = position
        while (
            before_walker := self._list.position_before(walker)
        ) is not None and before_walker.item.count < position.item.count:
            walker = before_walker
        self._list.insert_before(walker, position.item)
        self._list.remove(position)

    def is_empty(self) -> bool:
        """Return True if this list is empty."""
        return self._list.is_empty()

    def access(self, item: _T) -> None:
        """Access item and increase its access count."""
        position = self._find_position(item)
        if position is None:
            # if new item, insert at the back of the list
            position = self._list.insert_last(_Item(item))
        position.item.count += 1
        self._move_up(position)

    def remove(self, item: _T) -> None:
        """Remove item from this list."""
        position = self._find_position(item)
        if position is not None:
            # remove item if present
            self._list.remove(position)

    def top(self, k: int) -> Iterator[_T]:
        """
        Generate iterator over the top k items with respect to access counts.

        If list has less than k items, iteration stops when list is exhausted.
        """
        position = self._list.first_position()
        for _ in range(k):
            if position is None:
                break
            yield position.item.value
            position = self._list.position_after(position)
