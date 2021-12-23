from turtle import pos

from .positional_list import PositionalList


class _Item:
    __slots__ = "_value", "_count"  # improve memory usage

    def __init__(self, value):
        self.value = value  # value of the item
        self.count = 0  # access count initially set to zero


class FavoritesList:
    """List of elements sorted by access frequencies in non-increasing order."""

    def __init__(self):
        """Create an empty list of favorites."""
        self._data = PositionalList()  # will be list of _Item instances

    def __str__(self):
        # positional lists support iteration
        return str([(item.value, item.count) for item in self])

    def __len__(self):
        """Return number of entries in the favorites list."""
        return len(self._data)

    def _find_position(self, element):
        """Search for given element and return its position, or None if not found."""
        walk = self._data.first()
        while walk is not None and walk.element.value != element:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, position):
        """Move up the item located at given position based on access counts."""
        if position == self._data.first():
            # if already at the front, do nothing
            return
        walker = position
        count = position.element.count
        while (
            walker != self._data.first()
            and self._data.before(walker).element.count < count
        ):
            walker = self._data.before(walker)
        node = self._data.delete(position)  # delete
        self._data.add_before(walker, node)  # reinsert

    def is_empty(self):
        """Return True if list is empty."""
        return len(self._data) == 0

    def access(self, element):
        """Access element given element, and increase its access count."""
        position = self._find_position(element)
        if position is None:
            # if new element, insert at the back of the list
            position = self._data.add_last(_Item(element))
        position.element.count += 1  # increment access count
        self._move_up(position)

    def remove(self, element):
        """Remove given element."""
        position = self._find_position(element)
        if position is not None:
            # delete element if present
            self._data.delete(position)

    def top(self, k):
        """Generate iterator for top k elements with respect to access counts."""
        if k > len(self):
            raise ValueError(f"{k} exceeds list length")
        walker = self._data.first()
        for _ in range(k):
            yield walker.element.value
            walker = self._data.after(walker)


class FavoritesListMTF(FavoritesList):
    """List of elements sorted using move-to-front heuristic."""

    # override: use move-to-front heuristic
    def _move_up(self, position):
        """Move the item located at given position to the front of the list."""
        if position == self._data.first():
            # if already at the front, do nothing
            return
        node = self._data.delete(position)  # delete
        self._data.add_first(node)  # reinsert

    # override: traverse k times the list to find k top elements
    def top(self, k):
        """Generate iterator for top k elements with respect to access counts."""
        if k > len(self):
            raise ValueError(f"{k} exceeds list length")

        # copy original list
        temp_list = PositionalList()
        for item in self._data:  # positional lists support iteration
            temp_list.add_last(item)

        for _ in range(k):
            # traverse temp list and find element with largest access count
            highest = walker = temp_list.first()
            while walker != temp_list.last():
                walker = temp_list.after(walker)
                if walker.element.count > highest.element.count:
                    highest = walker

            yield highest.element.value  # yield element
            temp_list.delete(highest)  # remove element from temp list
