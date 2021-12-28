from __future__ import annotations

from typing import Iterator, TypeVar

from linked_list.favourites import FavouritesList, _Item
from linked_list.positional import Position, PositionalList

_T = TypeVar("_T")


class FavouritesListMTF(FavouritesList[_T]):
    """
    List of items with access counts sorted using move-to-front heuristic.

    >>> lst = FavouritesListMTF()
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
    [(5, 2), ('Python', 3)]
    >>> for item, count in lst:
    ...     print(item, count)
    5 2
    Python 3
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
    [(9, 1), ('Python', 3)]
    >>> for item in lst.top(3):
    ...     pass
    Traceback (most recent call last):
        ...
    IndexError: list has less than 3 items
    >>> lst.remove(5)
    >>> lst
    [(9, 1), ('Python', 3)]
    >>> lst.remove('Python')
    >>> lst.remove(9)
    >>> len(lst)
    0
    >>> lst.is_empty()
    True
    """

    # override: use move-to-front heuristic
    def _move_up(self, position: Position[_Item[_T]]) -> None:
        """Move the item located at position to the front of this list."""
        self._list.insert_first(position.item)
        self._list.remove(position)

    # override: traverse k times the list to find k top items
    def top(self, k: int) -> Iterator[_T]:
        """
        Generate iterator over top k items with respect to access counts.

        Raise IndexError if list has less than k items.
        """
        # clone original list
        self_clone: PositionalList[_Item[_T]] = PositionalList()
        for item in self._list:
            self_clone.insert_last(item)

        for _ in range(k):
            # traverse cloned list, find and remove item with largest access count
            highest = self_clone.first_position()
            if highest is None:
                raise IndexError(f"list has less than {k} items")
            walker = self_clone.position_after(highest)
            while walker is not None:
                if walker.item.count > highest.item.count:
                    highest = walker
                walker = self_clone.position_after(walker)
            yield highest.item.value
            self_clone.remove(highest)
