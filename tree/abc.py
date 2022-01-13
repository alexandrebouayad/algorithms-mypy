"""Abstract class for tree structure."""

from __future__ import annotations

from typing import Any, Generic, Iterator, Protocol, TypeVar

from linked_list.queue import Queue

_T = TypeVar("_T", covariant=True)
_P = TypeVar("_P", bound="Position[Any]")


class Position(Protocol[_T]):
    """
    Abstract base class for representing the location of an element in a tree.

    Two positions may represent the same inherent location in the tree. Use
    '==' rather than 'is' when testing equivalence of positions.
    """

    @property
    def element(self) -> _T:
        """Return the element stored at this position."""
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Return True if the two positions represent the same location."""
        raise NotImplementedError


class Tree(Generic[_T, _P]):
    """Abstract class of a tree structure."""

    def __len__(self) -> int:
        """Return the number of elements in the tree."""
        raise NotImplementedError

    def root(self) -> _P | None:
        """Return the root's position, or None if the tree is empty."""
        raise NotImplementedError

    def parent(self, p: _P) -> _P | None:
        """Return the position of p's parent, or None if p is the root."""
        raise NotImplementedError

    def n_children(self, p: _P) -> int:
        """Return the number of p's children."""
        raise NotImplementedError

    def children(self, p: _P) -> Iterator[_P]:
        """Return iterator over the positions of p's children."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[_T]:
        """Return pre-order iterator over the tree's elements."""
        for p in self.positions():
            yield p.element

    def positions(self) -> Iterator[_P]:
        """Return pre-order iterator over the tree's positions."""
        return self.pre_order()

    def is_empty(self) -> int:
        """Return True if the tree is empty."""
        return len(self) == 0

    def is_root(self, p: _P) -> bool:
        """Return True if p is the root."""
        return self.root() == p

    def is_leaf(self, p: _P) -> bool:
        """Return True if p has no children."""
        return self.n_children(p) == 0

    def depth(self, p: _P) -> int:
        """Return the number of levels separating p from the root."""
        parent = self.parent(p)
        if parent is None:  # p is root
            return 0
        return 1 + self.depth(parent)

    def height(self, p: _P | None = None) -> int:
        """
        Return the height of the subtree rooted at p.

        Return the height of the tree if p is None (-1 if the tree is empty).
        """
        p = p or self.root()
        if p is None:  # empty tree
            return -1
        return self._height_2(p)

    def _height_1(self) -> int:
        """
        Return the height of the tree.

        Worst-case time is quadratic in the size of the tree.
        """
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

    def _height_2(self, p: _P) -> int:
        """
        Return the height of the subtree rooted at p.

        Worst-case time is linear in the size of the subtree.
        """
        if self.is_leaf(p):
            return 0
        return 1 + max(self._height_2(c) for c in self.children(p))

    def _preorder(self, p: _P) -> Iterator[_P]:
        """Return pre-order iterator over positions in subtree rooted at p."""
        yield p  # visit p before its subtrees
        for c in self.children(p):
            yield from self._preorder(c)

    def pre_order(self) -> Iterator[_P]:
        """Return a pre-order iterator over the positions in the tree."""
        root = self.root()
        if root is None:  # empty Tree
            return
        yield from self._preorder(root)

    def _post_order(self, p: _P) -> Iterator[_P]:
        """Return post-order iterator over positions in subtree rooted at p."""
        for c in self.children(p):
            yield from self._post_order(c)
        yield p  # visit p after its subtrees

    def post_order(self) -> Iterator[_P]:
        """Return a post-order iterator over the positions in the tree."""
        root = self.root()
        if root is None:  # empty Tree
            return
        yield from self._post_order(root)

    def breadth_first(self) -> Iterator[_P]:
        """Return breadth-first iterator over the tree's positions."""
        root = self.root()
        if root is None:  # empty Tree
            return
        fringe = Queue[_P]()
        fringe.enqueue(root)
        while not fringe.is_empty():
            p = fringe.dequeue()
            yield p
            for child in self.children(p):
                fringe.enqueue(child)
