"""Abstract for binary tree structure."""

from __future__ import annotations

from typing import Any, Iterator, TypeVar

from tree.abc import Position, Tree

_T = TypeVar("_T")
_P = TypeVar("_P", bound=Position[Any])


class BinaryTree(Tree[_T, _P]):
    """Abstract base class for a binary tree structure."""

    def left_child(self, p: _P) -> _P | None:
        """Return the position of p's left child, or None if absent."""
        raise NotImplementedError

    def right_child(self, p: _P) -> _P | None:
        """Return the position of p's right child, or None if absent."""
        raise NotImplementedError

    def sibling(self, p: _P) -> _P | None:
        """Return the position of p's sibling, or None if absent."""
        parent = self.parent(p)
        if parent is None:  # p is root
            return None
        if p == self.left_child(parent):
            return self.right_child(parent)  # possibly None
        else:
            return self.left_child(parent)  # possibly None

    def children(self, p: _P) -> Iterator[_P]:
        """Return ordered iterator over the positions of p's children."""
        if (left_child := self.left_child(p)) is not None:
            yield left_child
        if (right_child := self.right_child(p)) is not None:
            yield right_child

    # override Tree' method: use in-order traversal
    def positions(self) -> Iterator[_P]:
        """Return in-order iterator over the tree's positions."""
        return self.in_order()

    def _in_order(self, p: _P) -> Iterator[_P]:
        """Return in-order iterator over positions in subtree rooted at p."""
        if (left_child := self.left_child(p)) is not None:
            yield from self._in_order(left_child)
        yield p
        if (right_child := self.right_child(p)) is not None:
            yield from self._in_order(right_child)

    def in_order(self) -> Iterator[_P]:
        """Return in-order iterator over the tree's positions."""
        root = self.root()
        if root is None:  # empty Tree
            return
        yield from self._in_order(root)
