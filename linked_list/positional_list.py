from linked_list import Position
from linked_list.doubly_linked import DoublyLinkedBase


class PositionalList(DoublyLinkedBase):
    """Implementation of a positional list based on a doubly linked list."""

    def _validate(self, position):
        """Return position's node, or raise appropriate error if invalid."""
        if not isinstance(position, Position):
            raise TypeError(f"{position} is not of type Position")
        if position == Position():
            # position has been deprecated
            raise ValueError("invalid position")
        if position._list is not self:
            raise ValueError(f"{position} does not refer to {self}")
        return position._node

    def _make_position(self, node):
        """Build and return a position for node, or None if sentinel node."""
        if node is self._header or node is self._trailer:
            return None
        else:
            return Position(self, node)

    def first(self):
        """Return the first position in the list, or None if the list is empty."""
        return self._make_position(self._header.next)

    def last(self):
        """Return the last Position in the list or None if the list is empty."""
        return self._make_position(self._trailer.prev)

    def before(self, position):
        """Return the position just before given position, or None if given
        position is first."""
        node = self._validate(position)
        return self._make_position(node.prev)

    def after(self, position):
        """Return the position just after given position, or None if given
        position is last."""
        node = self._validate(position)
        return self._make_position(node.next)

    def __iter__(self):
        """Generate iterator for traversing the list."""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element
            cursor = self.after(cursor)

    # override method of DoublyLinkedBase; return a position rather than a node
    def _insert_between(self, element, prev, next):
        """Add element between existing nodes and return new position."""
        node = super()._insert_between(element, prev, next)
        return self._make_position(node)

    def add_first(self, element):
        """Insert element at the front of the list and return new position."""
        return self._insert_between(element, self._header, self._header.next)

    def add_last(self, element):
        """Insert element at the back of the list and return new position."""
        return self._insert_between(element, self._trailer.prev, self._trailer)

    def add_before(self, position, element):
        """Insert element before given position and return new position."""
        node = self._validate(position)
        return self._insert_between(element, node.prev, node)

    def add_after(self, position, element):
        """Insert element after given position and return new position."""
        node = self._validate(position)
        return self._insert_between(element, node, node.next)

    def delete(self, position):
        """Remove and return element at given position."""
        node = self._validate(position)
        position._list = position._node = None  # deprecate position
        return self._delete_node(node)  # use method of DoublyLinkedBase

    def replace(self, position, element):
        """Replace the element at given position with given element, and return
        the replaced element.
        """
        node = self._validate(position)
        replaced_element = node.element
        node.element = element
        return replaced_element
