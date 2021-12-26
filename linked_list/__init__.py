class Position:
    """Abstraction representing the location of a single element.

    Note that two positions may represent the same inherent location in the
    list. Use 'p == q' rather than 'p is q' when testing equivalence of
    positions.
    """

    def __init__(self, list=None, node=None):
        self._list = list
        self._node = node

    @property
    def element(self):
        """Return the element stored at this position."""
        return self._node.element

    def __eq__(self, other):
        """Return True if the two positions represent the same location."""
        if not isinstance(other, Position):
            return False
        return self._list == other._list and self._node == other._node
