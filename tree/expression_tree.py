"""Arithmetic expression tree."""

from __future__ import annotations

from typing import Union, overload

from tree.linked_binary_tree import LinkedBinaryTree, Position

OPERATORS = "+-x*"


class ExpressionTree(LinkedBinaryTree[Union[str, int]]):
    """Arithmetic expression tree."""

    @overload
    def __init__(self, token: int):
        """One-parameter form."""
        ...

    @overload
    def __init__(
        self, token: str, left_tree: ExpressionTree, right_tree: ExpressionTree
    ):
        """three-parameter form."""
        ...

    def __init__(
        self,
        token: str | int,
        left_tree: ExpressionTree | None = None,
        right_tree: ExpressionTree | None = None,
    ):
        """Initialise an expression tree.

        In one-parameter form, token is a leaf value (an integer); the tree
        will have that value at an isolated node.

        In three-parameter form, token is a binary operator (one of the
        characters '+-*/'), and left and right are the operand subtrees.

        Raise ValueError if invalid parameters.
        """
        super().__init__()
        no_subtree = left_tree is None and right_tree is None
        valid_left_tree = isinstance(left_tree, ExpressionTree)
        valid_right_tree = isinstance(right_tree, ExpressionTree)
        valid_subtrees = valid_left_tree and valid_right_tree
        valid_leaf_value = isinstance(token, int)
        valid_operator = isinstance(token, str) and token in OPERATORS
        valid_parameters = valid_leaf_value and no_subtree
        valid_parameters |= valid_operator and valid_subtrees
        if not valid_parameters:
            raise ValueError("invalid parameters")
        root = self._add_root(token)
        if left_tree is not None and right_tree is not None:
            self._attach(root, left_tree, right_tree)
        self._list = list[str]()  # representation string pieces to concatenate

    def _parenthesise(self, position: Position[Union[str, int]]) -> None:
        if isinstance(position.element, str):  # internal node
            left_child = self.left_child(position)
            right_child = self.right_child(position)
            assert left_child is not None
            assert right_child is not None
            self._list.append("(")
            self._parenthesise(left_child)
            self._list.append(position.element)  # operator character
            self._parenthesise(right_child)
            self._list.append(")")
        self._list.append(str(position.element))
        return

    def string(self) -> str:
        """Return the string representation of the expression tree."""
        root = self.root()
        if root is None:  # empty tree
            return ""
        self._parenthesise(root)
        return "".join(self._list)

    def _eval(self, position: Position[Union[str, int]]) -> float:
        if isinstance(position.element, str):  # internal node
            left_child = self.left_child(position)
            right_child = self.right_child(position)
            assert left_child is not None
            assert right_child is not None
            left_value = self._eval(left_child)
            right_value = self._eval(right_child)
            if position.element == "+":
                return left_value + right_value
            if position.element == "-":
                return left_value - right_value
            if position.element == "*":
                return left_value * right_value
            if position.element == "/":
                return left_value / right_value
        return float(position.element)

    def eval(self) -> float:
        """Return the numeric value of the expression."""
        root = self.root()
        assert root is not None
        return self._eval(root)


def _tokenize(raw: str) -> list[Union[str, int]]:
    symbols = OPERATORS + "()"
    mark = 0
    tokens = list[Union[str, int]]()
    n = len(raw)
    for j in range(n):
        if raw[j] in symbols:
            if mark != j:
                # complete preceding token
                integer = int(raw[mark:j])
                tokens.append(integer)
            tokens.append(raw[j])  # add symbol
            mark = j + 1
    if mark != n:
        # complete preceding token
        integer = int(raw[mark:n])
        tokens.append(integer)
    return tokens


def expression_tree(raw: str) -> ExpressionTree:
    """Build and return an expression tree from an expression string."""
    tokens = _tokenize(raw)
    stack = list[Union[str, ExpressionTree]]()
    for token in tokens:
        if isinstance(token, int):
            stack.append(ExpressionTree(token))
        elif token in OPERATORS:
            stack.append(token)
        elif token == ")":
            right_tree = stack.pop()
            operator = stack.pop()
            left_tree = stack.pop()
            assert isinstance(operator, str)
            assert isinstance(left_tree, ExpressionTree)
            assert isinstance(right_tree, ExpressionTree)
            stack.append(ExpressionTree(operator, left_tree, right_tree))
        # ignore left parenthesis
    tree = stack.pop()
    assert isinstance(tree, ExpressionTree)
    return tree
