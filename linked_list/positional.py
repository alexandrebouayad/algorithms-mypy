from __future__ import annotations

from typing import Generic, TypeVar

from linked_list._double import DoublyLinkedBase as _DoublyLinkedBase
from linked_list._double import Header as _Header
from linked_list._double import Node as _Node
from linked_list._double import Trailer as _Trailer

_T = TypeVar("_T")


class Position(Generic[_T]):
    """
    Abstraction representing the location of a single item.

    Two positions may represent the same inherent location in the list. Use
    'p == q' rather than 'p is q' when testing equivalence of positions.

    >>> lst = _DoublyLinkedBase()
    >>> node_0 = lst._insert(0, lst._header, lst._trailer)
    >>> node_1 = lst._insert(1, node_0, lst._trailer)
    >>> node_2 = lst._insert(0, node_1, lst._trailer)
    >>> position_0 = Position(node_0, lst)
    >>> position_0
    Position(0)
    >>> position_2 = Position(node_2, lst)
    >>> position_0 == position_2
    False
    >>> new_position_0 = Position(node_0, lst)
    >>> position_0 == new_position_0
    True
    >>> new_lst = _DoublyLinkedBase()
    >>> new_node_0 = new_lst._insert(0, lst._header, lst._trailer)
    >>> new_position_0 = Position(node_0, new_lst)
    >>> position_0 == new_position_0
    False
    """

    __slots__ = "_node", "_list"  # improve memory usage

    def __init__(self, node: _Node[_T], list: _DoublyLinkedBase[_T]) -> None:
        self._node = node
        self._list = list

    @property
    def item(self) -> _T:
        """Return the item stored at this position."""
        return self._node.data

    def __repr__(self) -> str:
        item_repr = repr(self.item)
        return f"Position({item_repr})"

    def __eq__(self, other: object) -> bool:
        """Return True if the two positions represent the same location."""
        if not isinstance(other, Position):
            return False
        return self._list == other._list and self._node == other._node


class PositionalList(_DoublyLinkedBase[_T]):
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
    ValueError: invalid position
    >>> lst_2 = PositionalList()
    >>> lst_2.insert_before(position_9, 'algorithms')
    Traceback (most recent call last):
        ...
    ValueError: invalid position
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

    def _validate(self, position: Position[_T]) -> _Node[_T]:
        """Return node at position or raise ValueError if position is invalid."""
        if position._list is not self:
            # position does not refer to this list
            raise ValueError("invalid position")
        if position._node.deprecated:
            raise ValueError("invalid position")
        return position._node

    def _make_position(self, node: _Node[_T]) -> Position[_T]:
        """Return a position for node."""
        return Position(node, self)

    # override method of DoublyLinkedBase; return a position rather than a node
    def _positional_insert(
        self,
        item: _T,
        prev_node: _Node[_T] | _Header[_T],
        next_node: _Node[_T] | _Trailer[_T],
    ) -> Position[_T]:
        """Insert item between prev_node and next_node, and return new position."""
        node = super()._insert(item, prev_node, next_node)
        return self._make_position(node)

    def insert_first(self, item: _T) -> Position[_T]:
        """Insert item at the front of this list and return new position."""
        return self._positional_insert(item, self._header, self._header.next)

    def insert_last(self, item: _T) -> Position[_T]:
        """Insert item at the back of this list and return new position."""
        return self._positional_insert(item, self._trailer.prev, self._trailer)

    def insert_before(self, position: Position[_T], item: _T) -> Position[_T]:
        """Insert item before given position and return new position."""
        node = self._validate(position)
        return self._positional_insert(item, node.prev, node)

    def insert_after(self, position: Position[_T], item: _T) -> Position[_T]:
        """Insert item after given position and return new position."""
        node = self._validate(position)
        return self._positional_insert(item, node, node.next)

    def remove(self, position: Position[_T]) -> _T:
        """Remove and return item at position."""
        node = self._validate(position)
        node.deprecated = True
        return self._remove(node)

    def replace(self, position: Position[_T], item: _T) -> _T:
        """Place item at position and return old item."""
        node = self._validate(position)
        old_item = position.item
        node.data = item
        return old_item

    def first_position(self) -> Position[_T] | None:
        """Return the first position in this list, or None if the list is empty."""
        head = self._header.next  # head node or trailer
        if isinstance(head, _Trailer):
            return None
        return self._make_position(head)

    def last_position(self) -> Position[_T] | None:
        """Return the last position in this list, or None if the list is empty."""
        tail = self._trailer.prev  # tail node or header
        if isinstance(tail, _Header):
            return None
        return self._make_position(tail)

    def position_before(self, position: Position[_T]) -> Position[_T] | None:
        """Return the position just before given position, or None if given
        position is first."""
        node = self._validate(position)
        if isinstance(node.prev, _Header):
            return None
        return self._make_position(node.prev)

    def position_after(self, position: Position[_T]) -> Position[_T] | None:
        """Return the position just after given position, or None if given
        position is last."""
        node = self._validate(position)
        if isinstance(node.next, _Trailer):
            return None
        return self._make_position(node.next)
