from typing import List, Optional


class Node:
    """
    A node in the AVL tree.

    Attributes:
        value (int): The value stored in the node
        left (Optional[Node]): Reference to the left child node
        right (Optional[Node]): Reference to the right child node
        height (int): The height of the node in the tree
    """

    def __init__(self, value: int) -> None:
        """
        Initialize a new node with the given value.

        Args:
            value (int): The value to store in the node
        """
        self.value: int = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height: int = 1


class AVLTree:
    """
    A self-balancing binary search tree (AVL Tree) implementation.

    An AVL tree maintains balance by ensuring that for any node, the height
    difference between its left and right subtrees is at most 1.

    Attributes:
        root (Optional[Node]): The root node of the tree
    """

    def __init__(self) -> None:
        """Initialize an empty AVL tree."""
        self.root: Optional[Node] = None

    def insert(self, value: int) -> None:
        """
        Insert a value into the AVL tree.

        Duplicates are not allowed in the AVL tree.

        Args:
            value (int): The value to insert into the tree

        Raises:
            ValueError: If the value already exists in the tree
        """
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[Node], value: int) -> Node:
        """
        Recursively insert a value into the subtree rooted at node.

        Args:
            node (Optional[Node]): The root of the subtree to insert into
            value (int): The value to insert

        Returns:
            Node: The new root of the subtree after insertion and balancing
        """
        if not node:
            return Node(value)
        elif value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            raise ValueError("Duplicate values are not allowed in AVL Tree")

        # Update height and rebalance
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, value: int) -> None:
        """
        Delete a value from the AVL tree.

        Args:
            value (int): The value to delete from the tree

        Raises:
            ValueError: If the value is not found in the tree
        """
        self.root = self._delete(self.root, value)

    def _delete(self, node: Optional[Node], value: int) -> Optional[Node]:
        """
        Recursively delete a value from the subtree rooted at node.

        Args:
            node (Optional[Node]): The root of the subtree to delete from
            value (int): The value to delete

        Returns:
            Optional[Node]: The new root of the subtree after deletion and balancing

        Raises:
            ValueError: If the value is not found in the tree
        """

        if not node:
            # Value not found - raise an exception
            raise ValueError(f"Value {value} not found in the tree")
        elif value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node has two children: get inorder successor
            temp = self.get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        # Update height and rebalance
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Left Right Case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Right Left Case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def left_rotate(self, z: Node) -> Node:
        """
        Perform a left rotation on the given node.

        Args:
            z (Node): The node to rotate around

        Returns:
            Node: The new root of the subtree after rotation
        """
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z: Node) -> Node:
        """
        Perform a right rotation on the given node.

        Args:
            z (Node): The node to rotate around

        Returns:
            Node: The new root of the subtree after rotation
        """
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, node: Optional[Node]) -> int:
        """
        Get the height of a node.

        Args:
            node (Optional[Node]): The node to get the height of

        Returns:
            int: The height of the node (0 if node is None)
        """
        return node.height if node else 0

    def get_balance(self, node: Optional[Node]) -> int:
        """
        Get the balance factor of a node.

        The balance factor is calculated as: height(left_subtree) - height(right_subtree)
        A balanced node has a balance factor of -1, 0, or 1.

        Args:
            node (Optional[Node]): The node to get the balance factor of

        Returns:
            int: The balance factor of the node (0 if node is None)
        """
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def get_min_value_node(self, node: Node) -> Node:
        """
        Find the node with the minimum value in the subtree.

        Args:
            node (Node): The root of the subtree to search

        Returns:
            Node: The node with the minimum value
        """
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, value: int) -> Optional[Node]:
        """
        Search for a value in the AVL tree.

        Args:
            value (int): The value to search for

        Returns:
            Optional[Node]: The node containing the value, or None if not found
        """
        return self._search(self.root, value)

    def _search(self, node: Optional[Node], value: int) -> Optional[Node]:
        """
        Recursively search for a value in the subtree rooted at node.

        Args:
            node (Optional[Node]): The root of the subtree to search
            value (int): The value to search for

        Returns:
            Optional[Node]: The node containing the value, or None if not found
        """
        if not node or node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def _is_balanced(self, node: Optional[Node]) -> bool:
        """
        Check if the subtree rooted at node is balanced.

        Args:
            node (Optional[Node]): The root of the subtree to check

        Returns:
            bool: True if the subtree is balanced, False otherwise
        """
        if not node:
            return True

        balance = self.get_balance(node)
        return (
            abs(balance) <= 1
            and self._is_balanced(node.left)
            and self._is_balanced(node.right)
        )

    def preorder_traversal(self) -> List[int]:
        """
        Perform preorder traversal of the tree.

        Returns nodes in root -> left -> right order.

        Returns:
            List[int]: List of values in preorder traversal order
        """
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def inorder_traversal(self) -> List[int]:
        """
        Perform inorder traversal of the tree.

        Returns nodes in left -> root -> right order (sorted order for BST).

        Returns:
            List[int]: List of values in inorder traversal order (sorted)
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def postorder_traversal(self) -> List[int]:
        """
        Perform postorder traversal of the tree.

        Returns nodes in left -> right -> root order.

        Returns:
            List[int]: List of values in postorder traversal order
        """
        result = []
        self._postorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, node: Optional[Node], result: List[int]) -> None:
        """
        Helper method for preorder traversal: root -> left -> right.

        Args:
            node (Optional[Node]): Current node being visited
            result (List[int]): List to store traversal results
        """
        if node:
            result.append(node.value)
            self._preorder_traversal(node.left, result)
            self._preorder_traversal(node.right, result)

    def _inorder_traversal(self, node: Optional[Node], result: List[int]) -> None:
        """
        Helper method for inorder traversal: left -> root -> right.

        Args:
            node (Optional[Node]): Current node being visited
            result (List[int]): List to store traversal results
        """
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)

    def _postorder_traversal(self, node: Optional[Node], result: List[int]) -> None:
        """
        Helper method for postorder traversal: left -> right -> root.

        Args:
            node (Optional[Node]): Current node being visited
            result (List[int]): List to store traversal results
        """
        if node:
            self._postorder_traversal(node.left, result)
            self._postorder_traversal(node.right, result)
            result.append(node.value)
