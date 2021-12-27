from __future__ import annotations

from typing import Any

import linked_list.double as double


class PositionalList(double.DoublyLinkedBase):
    """
    Positional list based on doubly linked list.

    >>> lst = PositionalList()
    >>> lst.is_empty()
    True
    >>> position_5 = lst.insert_first(5)
    >>> position_5
    Position(5)
    >>> position_9 = lst.insert_last(9)
    >>> position_python = lst.insert_after(position_5, 'Python')
    >>> lst.is_empty()
    False
    >>> len(lst)
    3
    >>> lst
    PositionalList(5 <-> 'Python' <-> 9)
    >>> lst.first_position()
    Position(5)
    >>> lst.last_position()
    Position(9)
    >>> lst.position_before(position_9)
    Position('Python')
    >>> lst.position_before(position_5)
    >>> lst.position_after(position_python)
    Position(9)
    >>> lst.position_after(position_9)
    >>> len(lst)
    3
    >>> lst.remove(position_python)
    'Python'
    >>> lst.remove(position_python)
    Traceback (most recent call last):
        ...
    IndexError: invalid position
    >>> lst_2 = PositionalList()
    >>> lst_2.insert_before(position_9, 'algorithms')
    Traceback (most recent call last):
        ...
    IndexError: invalid position
    >>> position_algo = lst.insert_before(position_9, 'algorithms')
    >>> lst
    PositionalList(5 <-> 'algorithms' <-> 9)
    >>> lst.replace(position_5, 6)
    5
    >>> lst.remove(position_5)
    6
    >>> lst.remove(position_algo)
    'algorithms'
    >>> lst.remove(position_9)
    9
    >>> lst.is_empty()
    True
    """

    def _validate(self, position: double.Position) -> double.Node:
        """Return node at position or raise IndexError if position is invalid."""
        if position._list is not self:
            # position does not refer to this list
            raise IndexError("invalid position")
        if position._node.prev is None or position._node.next is None:
            # node had been deprecated
            raise IndexError("invalid position")
        return position._node

    def _make_position(self, node: double.Node) -> double.Position:
        """Return a position for node or None if sentinel node."""
        if node in (self._header, self._trailer):
            return None
        return double.Position(node, list=self)

    # override method of DoublyLinkedBase; return a position rather than a node
    def _insert(
        self,
        item: Any,
        prev_node: double.Node,
        next_node: double.Node,
    ) -> double.Position:
        """Insert item between prev_node and next_node, and return new position."""
        node = super()._insert(item, prev_node, next_node)
        return self._make_position(node)

    def insert_first(self, item: Any) -> double.Position:
        """Insert item at the front of this list and return new position."""
        return self._insert(item, self._header, self._header.next)

    def insert_last(self, item: Any) -> double.Position:
        """Insert item at the back of this list and return new position."""
        return self._insert(item, self._trailer.prev, self._trailer)

    def insert_before(
        self, position: double.Position, item: Any
    ) -> double.Position:
        """Insert item before given position and return new position."""
        node = self._validate(position)
        return self._insert(item, node.prev, node)

    def insert_after(
        self, position: double.Position, item: Any
    ) -> double.Position:
        """Insert item after given position and return new position."""
        node = self._validate(position)
        return self._insert(item, node, node.next)

    def remove(self, position: double.Position) -> Any:
        """Remove and return item at position."""
        node = self._validate(position)
        return self._remove(node)

    def replace(self, position: double.Position, item: Any) -> Any:
        """Place item at position and return old item."""
        node = self._validate(position)
        old_item = position.item
        node.data = item
        return old_item

    def first_position(self) -> double.Position:
        """Return the first position in this list or None if the list is empty."""
        return self._make_position(self._header.next)

    def last_position(self) -> double.Position:
        """Return the last Position in this list or None if the list is empty."""
        return self._make_position(self._trailer.prev)

    def position_before(self, position: double.Position) -> double.Position:
        """Return the position just before given position, or None if given
        position is first."""
        node = self._validate(position)
        return self._make_position(node.prev)

    def position_after(self, position: double.Position) -> double.Position:
        """Return the position just after given position, or None if given
        position is last."""
        node = self._validate(position)
        return self._make_position(node.next)
