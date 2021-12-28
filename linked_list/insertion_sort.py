from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, TypeVar

from linked_list.positional import PositionalList


class _Comparable(Protocol):
    @abstractmethod
    def __lt__(self: _T, other: _T) -> bool:
        pass

    def __le__(self: _T, other: _T) -> bool:
        return self < other or self == other


_T = TypeVar("_T", bound=_Comparable)


def insertion_sort(lst: PositionalList[_T]) -> None:
    """
    Sort positional list of comparable items in non-decreasing order.

    >>> lst = PositionalList()
    >>> lst.insert_last(2)
    Position(2)
    >>> lst.insert_last(6)
    Position(6)
    >>> lst.insert_last(1)
    Position(1)
    >>> lst.insert_last(8)
    Position(8)
    >>> lst.insert_last(-10)
    Position(-10)
    >>> insertion_sort(lst)
    >>> lst
    PositionalList(-10 <-> 1 <-> 2 <-> 6 <-> 8)
    """

    marker = lst.first_position()
    if marker is None:
        # empty list
        return

    while (pivot := lst.position_after(marker)) is not None:
        if marker.item <= pivot.item:
            # pivot item is already sorted
            marker = pivot
        else:
            # find left-most item greater than pivot item
            walker = marker
            while (
                before_walker := lst.position_before(walker)
            ) is not None and before_walker.item > pivot.item:
                # shift walker to the left
                walker = before_walker
            lst.insert_before(walker, pivot.item)
            lst.remove(pivot)
