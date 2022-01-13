"""Linked structure for binary tree."""

from __future__ import annotations

from typing import Generic, TypeVar

from tree.binary_abc import BinaryTree

_T = TypeVar("_T")


class _Node(Generic[_T]):
    """Binary node."""

    __slots__ = "element", "parent", "left", "right", "deprecated"

    def __init__(
        self,
        element: _T,
        *,
        parent: _Node[_T] | None = None,
        left: _Node[_T] | None = None,
        right: _Node[_T] | None = None
    ):
        """Initialise node."""
        self.element = element
        self.parent = parent
        self.left = left
        self.right = right
        self.deprecated = False


class Position(Generic[_T]):
    """
    Location of an element in a tree.

    Two positions may represent the same inherent location in the tree. Use
    'p == q' rather than 'p is q' when testing equivalence of positions.
    """

    __slots__ = "_tree", "_node"

    def __init__(self, tree: LinkedBinaryTree[_T], node: _Node[_T]) -> None:
        """Initialise position."""
        self._tree = tree
        self._node = node

    @property
    def element(self) -> _T:
        """Return the element stored at this position."""
        return self._node.element

    def __eq__(self, other: object) -> bool:
        """Return True if the two positions represent the same location."""
        if not isinstance(other, Position):
            return False
        return (self._tree, self._node) is (other._tree, other._node)


class LinkedBinaryTree(BinaryTree[_T, Position[_T]]):
    """Linked representation of a binary tree structure."""

    def __init__(self) -> None:
        """Initialise empty tree."""
        self._root: _Node[_T] | None = None
        self._size = 0

    def __len__(self) -> int:
        """Return the number of elements in the tree."""
        return self._size

    def _validate(self, p: Position[_T]) -> _Node[_T]:
        """
        Return p's node.

        Raise ValueError if the position is invalid.
        """
        if p._tree != self or p._node.deprecated:
            raise ValueError("invalid position")
        return p._node

    def _make_position(self, node: _Node[_T]) -> Position[_T]:
        """Return node's position, or None if node is None."""
        return None if node is None else Position(self, node)

    def root(self) -> Position[_T] | None:
        """Return the root's position, or None if the tree is empty."""
        if self._root is None:  # tree is empty
            return None
        return self._make_position(self._root)

    def parent(self, p: Position[_T]) -> Position[_T] | None:
        """Return the position of p's parent, or None if p is the root."""
        node = self._validate(p)
        if node.parent is None:
            return None
        return self._make_position(node.parent)

    def left_child(self, p: Position[_T]) -> Position[_T] | None:
        """Return the position of p's left child, or None if absent."""
        node = self._validate(p)
        if node.left is None:
            return None
        return self._make_position(node.left)

    def right_child(self, p: Position[_T]) -> Position[_T] | None:
        """Return the position of p's right child, or None if absent."""
        node = self._validate(p)
        if node.right is None:
            return None
        return self._make_position(node.right)

    def n_children(self, p: Position[_T]) -> int:
        """Return the number of p's children."""
        node = self._validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def _add_root(self, element: _T) -> Position[_T]:
        """Add element at the root of an empty tree.

        Return the root's position.
        Raise ValueError if the tree is not empty.
        """
        if not self.is_empty():
            raise ValueError("non-empty tree")
        self._root = _Node[_T](element)
        self._size = 1
        return self._make_position(self._root)

    def _add_left(self, p: Position[_T], element: _T) -> Position[_T]:
        """
        Add a left child to p's node and store element on the new node.

        Return the position of the new node.
        Raise ValueError if p is invalid or if p already has a left child.
        """
        node = self._validate(p)
        if node.left is not None:
            raise ValueError("left child exists")
        node.left = _Node[_T](element, parent=node)
        self._size += 1
        return self._make_position(node.left)

    def _add_right(self, p: Position[_T], element: _T) -> Position[_T]:
        """
        Add a right child to p's node and store element on the new node.

        Return the position of the new node.
        Raise ValueError if p is invalid or if p already has a left child.
        """
        node = self._validate(p)
        if node.right is not None:
            raise ValueError("right child exists")
        node.right = _Node[_T](element, parent=node)
        self._size += 1
        return self._make_position(node.right)

    def _replace(self, p: Position[_T], element: _T) -> _T:
        """Place element at p, and return the replaced element."""
        node = self._validate(p)
        old_element = node.element
        node.element = element
        return old_element

    def _delete(self, p: Position[_T]) -> _T:
        """
        Delete p's node, and replace it with its unique child, if any.

        Return deleted element.
        Raise ValueError if p is invalid or if p has two children.
        """
        node = self._validate(p)
        if self.n_children(p) == 2:
            raise ValueError("delete node with two children")
        child = node.left or node.right
        if node.parent is None:  # node is root
            self._root = child
        elif child is None:
            if node is node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
        else:
            child.parent = node.parent  # child's grandparent becomes parent
        node.deprecated = True
        self._size -= 1
        return node.element

    def _attach(
        self,
        p: Position[_T],
        tree_1: LinkedBinaryTree[_T],
        tree_2: LinkedBinaryTree[_T],
    ) -> None:
        """
        Attach tree_1 and tree_2 to the left and right of p, respectively.

        As a side effect, set tree_1 and tree_2 empty.
        Raise ValueError if p is internal.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError("attach to internal node")

        # attach tree_1 and tree_2
        if tree_1._root is not None:  # tree_1 is not empty
            tree_1._root.parent = node
            node.left = tree_1._root
        if tree_2._root is not None:  # tree_2 is not empty
            tree_2._root.parent = node
            node.right = tree_2._root
        self._size += len(tree_1) + len(tree_2)

        # set tree_1 and tree_2 empty
        tree_1._root = tree_2._root = None
        tree_1._size = tree_2._size = 0
