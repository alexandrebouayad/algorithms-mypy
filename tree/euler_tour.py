"""Euler tour."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from tree.abc import Position, Tree

_T = TypeVar("_T", covariant=True)
_P = TypeVar("_P", bound=Position[Any])
_R = TypeVar("_R")


class EulerTour(Generic[_T, _P, _R]):
    """Abstract base class for performing Euler tour of a tree.

    _pre_visit_hook and _post_visit_hook may be overridden by subclasses.
    """

    def __init__(self, tree: Tree[_T, _P]):
        """Initialise Euler tour of tree."""
        self.tree = tree

    def execute(self) -> _R | None:
        """Perform Euler tour.

        Return result from root's post visit.
        """
        root = self.tree.root()
        if root is None:
            return None
        return self._tour(root, 0, [])  # start the recursion

    def _tour(self, position: _P, depth: int, path: list[int]) -> _R:
        """Perform Euler tour on subtree rooted at position.

        Return result from post visit of position's node.

        position    position of current node being visited
        depth       depth of position' node in the tree
        path        list of children's indices from root to position' node
        """
        self._pre_visit_hook(position, depth, path)
        results = list[_R]()
        path.append(0)  # add new index to end of path before recursion
        for child in self.tree.children(position):
            results.append(self._tour(child, depth + 1, path))
            path[-1] += 1  # increment path's last index
        path.pop()  # remove extraneous index
        return self._post_visit_hook(position, depth, path, results)

    def _pre_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        """Visit position's node before visiting its children.

        position    position of current node being visited
        depth       depth of position' node in the tree
        path        list of children's indices from root to position' node
        """
        pass

    def _post_visit_hook(
        self, position: _P, depth: int, path: list[int], results: list[_R]
    ) -> _R:
        """Visit position's node after visiting its children.

        position    position of current node being visited
        depth       depth of position' node in the tree
        path        list of children's indices from root to position' node
        """
        pass


class IndentedTreePrinter(EulerTour[_T, _P, None]):
    """Pre-order tree printer with level indentation."""

    def __init__(self, indent: int) -> None:
        """Initialise printer with indent spaces for indentation."""
        self.indent = indent

    def _pre_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        print(" " * self.indent * depth + str(position.element))


class LabelledTreePrinter(IndentedTreePrinter[_T, _P]):
    """Pre-order tree printer with level indentation and labelling."""

    def _pre_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        label = ".".join(str(j + 1) for j in path)  # labels are one-indexed
        print(" " * 2 * depth + label, position.element())


class ParentheticPrinter(EulerTour[_T, _P, None]):
    """Parenthetic tree printer."""

    def _pre_visit_hook(
        self, position: _P, depth: int, path: list[int]
    ) -> None:
        if path and path[-1] > 0:  # position's node follows a sibling
            print(", ", end="")
        print(position.element, end="")
        if not self.tree.is_leaf(position):  # if position's node has children
            print(" (", end="")

    def _post_visit_hook(
        self, position: _P, depth: int, path: list[int], results: list[_R]
    ) -> None:
        if not self.tree.is_leaf(position):  # if position's node has children
            print(")", end="")


_PN = TypeVar("_PN", bound=Position[int])


class TreeSum(EulerTour[int, _PN, int]):
    """Euler tour for summing elements of a tree."""

    def _post_visit_hook(
        self, position: _PN, depth: int, path: list[int], results: list[int]
    ) -> int:
        return position.element + sum(results)
