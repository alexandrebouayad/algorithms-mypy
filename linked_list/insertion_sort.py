from __future__ import annotations

import linked_list.positional as positional


def insertion_sort(lst: positional.PositionalList) -> None:
    """
    Sort positional list of comparable items in non-decreasing order.

    >>> lst = positional.PositionalList()
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
    while marker != lst.last_position():
        # position of next item to insert
        pivot = lst.position_after(marker)

        if marker.item <= pivot.item:
            # pivot item is already sorted
            marker = pivot
        else:
            # find left-most item greater than pivot item
            walker = marker
            while (
                walker != lst.first_position()
                and lst.position_before(walker).item > pivot.item
            ):
                # shift walker to the left
                walker = lst.position_before(walker)
            lst.insert_before(walker, pivot.item)
            lst.remove(pivot)
