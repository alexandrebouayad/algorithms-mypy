def insertion_sort(lst):
    """Sort positional list of comparable elements in non-decreasing order."""

    marker = lst.first()
    while marker != lst.last():
        pivot = lst.after(marker)  # position of next element to insert
        if marker.element <= pivot.element:  # pivot element is already sorted
            marker = pivot  # pivot becomes new marker
        else:  # find leftmost element greater than pivot element
            walker = marker
            while (
                walker != lst.first()
                and lst.before(walker).element > pivot.element
            ):
                walker = lst.before(walker)  # shift walker to the left
            lst.delete(pivot)  # remove pivot element from the list
            lst.add_before(walker, pivot.element)  # reinsert before walker
