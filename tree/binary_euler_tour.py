"""Binary Euler tour."""

from __future__ import annotations

from typing import Any, TypeVar

from tree.abc import Position
from tree.binary_abc import BinaryTree
from tree.euler_tour import EulerTour

_T = TypeVar("_T")
_P = TypeVar("_P", bound=Position[Any])
_R = TypeVar("_R")


class BinaryEulerTour(EulerTour[_T, _P, _R]):
    """Abstract base class for performing Euler tour of a binary tree.

    Include an additional _in_visit_hook that is called after the tour of the
    left subtree (if any), and before the tour of the right subtree (if any).

    Note: right child is indexed by 1 in paths, even if it has no left sibling.
    """

    tree: BinaryTree[_T, _P]

    def _tour(self, position: _P, depth: int, path: list[int]) -> _R:
        results = list[_R]()
        self._pre_visit_hook(position, depth, path)
        if (left_child := self.tree.left_child(position)) is not None:
            path.append(0)
            results[0] = self._tour(left_child, depth + 1, path)
            path.pop()
        self._in_visit_hook(position, depth, path)
        if (right_child := self.tree.right_child(position)) is not None:
            path.append(1)
            results[1] = self._tour(right_child, depth + 1, path)
            path.pop()
        return self._post_visit_hook(position, depth, path, results)

    def _in_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        """Visit position's node between the visits of its two children.

        position    position of current node being visited
        depth       depth of position' node in the tree
        path        list of children's indices from root to position' node
        """
        pass


class BinaryTreeLayout(BinaryEulerTour[_T, _P, int]):
    """Euler tour for computing planar coordinates of a binary tree's nodes."""

    def __init__(self, tree: BinaryTree[_T, _P]):
        """Initialise Euler tour."""
        super().__init__(tree)
        self._count = 0  # number of processed nodes
        self.coordinates = dict[_P, tuple[int, int]]()

    def _in_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        self.coordinates[position] = self._count, depth
        self._count += 1
