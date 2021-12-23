  class SingleLinkNode:
    """Lightweight class for storing a singly linked node."""
    __slots__ = 'element', 'next'  # improve memory usage

    def __init__(self, element, next):
      self.element = element  # element of the node
      self.next = next  # next linked node


class DoubleLinkNode:
  """Lightweight class for storing a doubly linked node."""
  __slots__ = '_element', '_prev', '_next'  # improve memory usage

  def __init__(self, element, prev, next):
    self.element = element  # element of the node
    self.prev = prev  # previous linked node
    self.next = next  # next linked node


class DoublyLinkedBase:
    """Implementation of a doubly linked list."""

    def __init__(self):
        """Create an empty list."""
        self._header = DoubleLinkNode(None, None, None)
        self._trailer = DoubleLinkNode(None, None, None)
        self._header.next = self._trailer  # trailer is after header
        self._trailer.prev = self._header  # header is before trailer
        self._size = 0  # number of elements in the list

    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if list is empty."""
        return self._size == 0

    def _insert_between(self, element, prev_node, next_node):
        """Add element between two existing nodes and return new node."""
        new_node = DoubleLinkNode(element, prev_node, next_node)
        prev_node.next = new_node
        next_node.prev = new_node
        self._size += 1
        return new_node

    def _delete_node(self, node):
        """Delete non-sentinel node from the list and return its element."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self._size -= 1
        return node.element  # return element of the deleted node


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
