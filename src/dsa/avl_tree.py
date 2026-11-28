"""
D2: AVL Tree (self-balancing binary search tree).
Used for sorted listings and range queries.

insert, delete: O(log n)
in_order_traversal: O(n)
range_query: O(log n + k), k = number of results
rotations: O(1)
space: O(n)
"""

from typing import Any, Callable, List, Optional


class AVLNode:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.values = [value]  # same keys share one node
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self, key_func: Optional[Callable] = None) -> None:
        """Create an empty tree. O(1)."""
        self.root = None
        self.key_func = key_func or (lambda value: value)

    def _height(self, node):
        return node.height if node else 0

    def _balance(self, node):
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def rotate_right(self, node: AVLNode) -> AVLNode:
        """Rotate right and return the new top node. O(1)."""
        pivot = node.left
        node.left = pivot.right
        pivot.right = node
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    def rotate_left(self, node: AVLNode) -> AVLNode:
        """Rotate left and return the new top node. O(1)."""
        pivot = node.right
        node.right = pivot.left
        pivot.left = node
        self._update_height(node)
        self._update_height(pivot)
        return pivot

    def _rebalance(self, node):
        self._update_height(node)
        if self._balance(node) > 1:  # left heavy
            if self._balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if self._balance(node) < -1:  # right heavy
            if self._balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert(self, value: Any, key: Any = None) -> None:
        """Add a value to the tree. O(log n)."""
        if key is None:
            key = self.key_func(value)
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.values.append(value)
        return self._rebalance(node)

    def delete(self, key: Any) -> None:
        """Remove a key and all its values. O(log n)."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # two children: copy the next bigger node, then delete it
            next_node = node.right
            while next_node.left:
                next_node = next_node.left
            node.key = next_node.key
            node.values = next_node.values
            node.right = self._delete(node.right, next_node.key)
        return self._rebalance(node)

    def in_order_traversal(self) -> List[Any]:
        """Return all values in key order. O(n)."""
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node, result):
        if node:
            self._traverse(node.left, result)
            result.extend(node.values)
            self._traverse(node.right, result)

    def range_query(self, min_key: Any, max_key: Any) -> List[Any]:
        """Return values from min_key to max_key. O(log n + k)."""
        if min_key > max_key:
            raise ValueError("Minimum key cannot be greater than maximum key.")
        result = []
        self._range(self.root, min_key, max_key, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.key:
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.extend(node.values)
        if node.key < high:
            self._range(node.right, low, high, result)