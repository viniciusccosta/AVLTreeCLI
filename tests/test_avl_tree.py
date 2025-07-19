"""
Comprehensive tests for the AVL Tree implementation.

Tests cover all core functionality including:
- Node creation and initialization
- Tree insertion with automatic balancing
- Tree deletion with rebalancing
- Search operations
- Tree rotations (left and right)
- Balance factor calculations
- Height calculations
- Edge cases and error conditions
"""

from typing import List, Optional

import pytest

from avltreecli.avl_tree import AVLTree, Node


class TestNode:
    """Test cases for the Node class."""

    def test_node_creation(self) -> None:
        """Test that a node is created correctly with default values."""
        node = Node(10)
        assert node.value == 10
        assert node.left is None
        assert node.right is None
        assert node.height == 1

    def test_node_with_negative_value(self) -> None:
        """Test node creation with negative values."""
        node = Node(-5)
        assert node.value == -5
        assert node.height == 1

    def test_node_with_zero(self) -> None:
        """Test node creation with zero value."""
        node = Node(0)
        assert node.value == 0
        assert node.height == 1

    def test_node_without_value(self) -> None:
        """Test node creation without a value."""
        with pytest.raises(TypeError):
            Node()

    def test_node_with_left_parameter(self) -> None:
        """Test node creation with left and right children."""
        left_child = Node(5)

        with pytest.raises(TypeError):
            Node(10, left=left_child)

    def test_node_with_right_parameter(self) -> None:
        """Test node creation with right and left children."""
        right_child = Node(15)

        with pytest.raises(TypeError):
            Node(10, right=right_child)

    def test_node_with_both_children(self) -> None:
        """Test node creation with both left and right children."""
        left_child = Node(5)
        right_child = Node(15)

        with pytest.raises(TypeError):
            Node(10, left=left_child, right=right_child)

    def test_node_height_update(self) -> None:
        """Test that the height of a node is updated correctly."""
        node = Node(10)
        assert node.height == 1

        # Simulate left child
        node.left = Node(5)
        node.height = (
            max(node.left.height + 1, node.right.height + 1)
            if node.right
            else node.left.height + 1
        )
        assert node.height == 2

        # Simulate right child
        node.right = Node(15)
        node.height = max(node.left.height + 1, node.right.height + 1)
        assert node.height == 2


class TestAVLTree:
    """Test cases for the AVL Tree implementation."""

    def setup_method(self) -> None:
        """Set up a fresh AVL tree for each test."""
        self.tree = AVLTree()

    def test_empty_tree_creation(self) -> None:
        """Test that an empty tree is created correctly."""
        assert self.tree.root is None

    def test_single_insertion(self) -> None:
        """Test inserting a single value into an empty tree."""
        self.tree.insert(10)
        assert self.tree.root is not None
        assert self.tree.root.value == 10
        assert self.tree.root.height == 1
        assert self.tree.root.left is None
        assert self.tree.root.right is None

    def test_multiple_insertions_no_rotation(self) -> None:
        """Test inserting multiple values that don't require rotation."""
        values = [10, 5, 15]
        for value in values:
            self.tree.insert(value)

        # Check tree structure
        assert self.tree.root.value == 10
        assert self.tree.root.left.value == 5
        assert self.tree.root.right.value == 15
        assert self.tree.root.height == 2

    def test_left_rotation(self) -> None:
        """Test that left rotation occurs when needed (Right-Right case)."""
        # Insert values that cause right-heavy imbalance
        self.tree.insert(10)
        self.tree.insert(20)
        self.tree.insert(30)  # This should trigger left rotation

        # After rotation, 20 should be root
        assert self.tree.root.value == 20
        assert self.tree.root.left.value == 10
        assert self.tree.root.right.value == 30

    def test_right_rotation(self) -> None:
        """Test that right rotation occurs when needed (Left-Left case)."""
        # Insert values that cause left-heavy imbalance
        self.tree.insert(30)
        self.tree.insert(20)
        self.tree.insert(10)  # This should trigger right rotation

        # After rotation, 20 should be root
        assert self.tree.root.value == 20
        assert self.tree.root.left.value == 10
        assert self.tree.root.right.value == 30

    def test_left_right_rotation(self) -> None:
        """Test Left-Right case rotation."""
        self.tree.insert(30)
        self.tree.insert(10)
        self.tree.insert(20)  # This should trigger left-right rotation

        # After rotation, 20 should be root
        assert self.tree.root.value == 20
        assert self.tree.root.left.value == 10
        assert self.tree.root.right.value == 30

    def test_right_left_rotation(self) -> None:
        """Test Right-Left case rotation."""
        self.tree.insert(10)
        self.tree.insert(30)
        self.tree.insert(20)  # This should trigger right-left rotation

        # After rotation, 20 should be root
        assert self.tree.root.value == 20
        assert self.tree.root.left.value == 10
        assert self.tree.root.right.value == 30

    def test_complex_insertions(self) -> None:
        """Test a complex sequence of insertions that require multiple rotations."""
        values = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35]
        for value in values:
            self.tree.insert(value)

        # Verify the tree is still balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify all values are present
        for value in values:
            assert self.tree.search(value) is not None

    def test_duplicate_insertion(self) -> None:
        """Test inserting duplicate values."""
        self.tree.insert(10)

        with pytest.raises(ValueError) as exc_info:
            self.tree.insert(10)
        assert str(exc_info.value) == "Duplicate values are not allowed in AVL Tree"

    def test_search_existing_value(self) -> None:
        """Test searching for values that exist in the tree."""
        values = [10, 5, 15, 3, 7, 12, 17]
        for value in values:
            self.tree.insert(value)

        for value in values:
            result = self.tree.search(value)
            assert result is not None
            assert result.value == value

    def test_search_non_existing_value(self) -> None:
        """Test searching for values that don't exist in the tree."""
        values = [10, 5, 15]
        for value in values:
            self.tree.insert(value)

        # Search for values not in tree
        assert self.tree.search(1) is None
        assert self.tree.search(100) is None
        assert self.tree.search(8) is None

    def test_search_empty_tree(self) -> None:
        """Test searching in an empty tree."""
        assert self.tree.search(10) is None

    def test_delete_leaf_node(self) -> None:
        """Test deleting a leaf node."""
        values = [10, 5, 15]
        for value in values:
            self.tree.insert(value)

        self.tree.delete(5)  # Delete leaf node

        assert self.tree.search(5) is None
        assert self.tree.search(10) is not None
        assert self.tree.search(15) is not None
        # assert self._is_balanced(self.tree.root)

    def test_delete_node_with_one_child(self) -> None:
        """Test deleting a node with one child."""
        values = [10, 5, 15, 3]
        for value in values:
            self.tree.insert(value)

        self.tree.delete(5)  # Delete node with one child

        assert self.tree.search(5) is None
        assert self.tree.search(3) is not None
        assert self.tree.search(10) is not None
        assert self.tree.search(15) is not None
        # assert self._is_balanced(self.tree.root)

    def test_delete_node_with_two_children(self) -> None:
        """Test deleting a node with two children."""
        values = [10, 5, 15, 3, 7, 12, 17]
        for value in values:
            self.tree.insert(value)

        self.tree.delete(10)  # Delete root node with two children

        assert self.tree.search(10) is None
        for value in [5, 15, 3, 7, 12, 17]:
            assert self.tree.search(value) is not None
        # assert self._is_balanced(self.tree.root)

    def test_delete_root_single_node(self) -> None:
        """Test deleting the root when it's the only node."""
        self.tree.insert(10)
        self.tree.delete(10)

        assert self.tree.root is None

    def test_delete_non_existing_value(self) -> None:
        """Test deleting a value that doesn't exist."""
        values = [10, 5, 15]
        for value in values:
            self.tree.insert(value)

        with pytest.raises(ValueError) as exc_info:
            self.tree.delete(100)  # Delete non-existing value
        assert str(exc_info.value) == "Value 100 not found in the tree"

    def test_delete_from_empty_tree(self) -> None:
        """Test deleting from an empty tree."""
        with pytest.raises(ValueError) as exc_info:
            self.tree.delete(10)

        # TODO: Seria interessante ter um erro diferente aqui
        assert str(exc_info.value) == "Value 10 not found in the tree"

    def test_delete_with_rebalancing(self) -> None:
        """Test that deletion triggers rebalancing when needed."""
        # Create a tree that will need rebalancing after deletion
        values = [20, 10, 30, 5, 15, 25, 35, 1, 7, 12, 17]
        for value in values:
            self.tree.insert(value)

        # Delete nodes that should trigger rebalancing
        self.tree.delete(1)
        self.tree.delete(5)

        # Verify tree is still balanced
        assert self.tree._is_balanced(self.tree.root)

    def test_height_calculation(self) -> None:
        """Test height calculation for various tree configurations."""
        # Empty tree
        assert self.tree.get_height(None) == 0

        # Single node
        self.tree.insert(10)
        assert self.tree.get_height(self.tree.root) == 1

        # Two levels
        self.tree.insert(5)
        assert self.tree.get_height(self.tree.root) == 2

        # Three levels
        self.tree.insert(15)
        self.tree.insert(3)
        assert self.tree.get_height(self.tree.root) >= 2

    def test_balance_factor_calculation(self) -> None:
        """Test balance factor calculations."""
        # Empty tree
        assert self.tree.get_balance(None) == 0

        # Single node
        self.tree.insert(10)
        assert self.tree.get_balance(self.tree.root) == 0

        # Left-heavy
        self.tree.insert(5)
        assert self.tree.get_balance(self.tree.root) == 1

        # Balanced
        self.tree.insert(15)
        assert self.tree.get_balance(self.tree.root) == 0

    def test_min_value_node(self) -> None:
        """Test finding the minimum value node in a subtree."""
        values = [20, 10, 30, 5, 15, 25, 35]
        for value in values:
            self.tree.insert(value)

        min_node = self.tree.get_min_value_node(self.tree.root)
        assert min_node.value == 5

        # Test min in right subtree
        min_right = self.tree.get_min_value_node(self.tree.root.right)
        assert min_right.value == 25

    def test_large_dataset(self) -> None:
        """Test with a large dataset to ensure performance and correctness."""
        import random

        # Insert 100 random values
        values = list(range(1, 101))
        random.shuffle(values)

        for value in values:
            self.tree.insert(value)

        # Verify all values are present
        for value in values:
            assert self.tree.search(value) is not None

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Delete half the values
        to_delete = values[:50]
        for value in to_delete:
            self.tree.delete(value)

        # Verify deleted values are gone
        for value in to_delete:
            assert self.tree.search(value) is None

        # Verify remaining values are still present
        for value in values[50:]:
            assert self.tree.search(value) is not None

        # Verify tree is still balanced
        assert self.tree._is_balanced(self.tree.root)

    def test_negative_values(self) -> None:
        """Test tree operations with negative values."""
        values = [-10, -5, -15, -3, -7, -12, -17]
        for value in values:
            self.tree.insert(value)

        # Verify all values are present
        for value in values:
            assert self.tree.search(value) is not None

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Test deletion
        self.tree.delete(-10)
        assert self.tree.search(-10) is None
        assert self.tree._is_balanced(self.tree.root)

    def test_mixed_positive_negative_values(self) -> None:
        """Test tree operations with mixed positive and negative values."""
        values = [-20, -10, 10, 20, -5, 5, -15, 15]
        for value in values:
            self.tree.insert(value)

        # Verify all values are present
        for value in values:
            assert self.tree.search(value) is not None

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

    def test_preorder_traversal(self) -> None:
        """Test preorder traversal functionality."""
        values = [10, 5, 15, 3, 7, 12, 17]
        for value in values:
            self.tree.insert(value)

        preorder_result = self.tree.preorder_traversal()

        # All values should be present
        assert set(preorder_result) == set(values)

        # Length should match
        assert len(preorder_result) == len(values)

        # Check the order of traversal
        assert preorder_result[0] == 10  # Root first
        assert preorder_result[1] == 5  # Left child second
        assert preorder_result[2] == 3  # Left-left grandchild third
        assert preorder_result[3] == 7  # Left-right grandchild fourth
        assert preorder_result[4] == 15  # Right child fifth
        assert preorder_result[5] == 12  # Right-left grandchild sixth
        assert preorder_result[6] == 17  # Right-right grandchild seventh

    def test_inorder_traversal_sorted(self) -> None:
        """Test that inorder traversal returns values in sorted order."""
        values = [20, 10, 30, 5, 15, 25, 35, 12, 17, 22, 27]
        for value in values:
            self.tree.insert(value)

        inorder_result = self.tree.inorder_traversal()
        assert inorder_result == sorted(values)

    def test_postorder_traversal(self) -> None:
        """Test postorder traversal functionality."""
        values = [10, 5, 15, 3, 7, 12, 17]
        for value in values:
            self.tree.insert(value)

        postorder_result = self.tree.postorder_traversal()

        # All values should be present
        assert set(postorder_result) == set(values)

        # Length should match
        assert len(postorder_result) == len(values)

        # Check the order of traversal
        assert postorder_result[-1] == 10  # Root last
        assert postorder_result[0] == 3  # Leftmost leaf first
        assert postorder_result[1] == 7  # Left-right grandchild second
        assert postorder_result[2] == 5  # Left child third
        assert postorder_result[3] == 12  # Right-left grandchild fourth
        assert postorder_result[4] == 17  # Right-right grandchild fifth
        assert postorder_result[5] == 15  # Right child sixth

    def test_traversal_empty_tree(self) -> None:
        """Test traversals on empty tree."""
        assert self.tree.preorder_traversal() == []
        assert self.tree.inorder_traversal() == []
        assert self.tree.postorder_traversal() == []

    def test_traversal_single_node(self) -> None:
        """Test traversals with single node."""
        self.tree.insert(42)

        assert self.tree.preorder_traversal() == [42]
        assert self.tree.inorder_traversal() == [42]
        assert self.tree.postorder_traversal() == [42]

    def test_traversal_with_negative_values(self) -> None:
        """Test traversals with negative values."""
        values = [-10, -5, -15, -3, -7]
        for value in values:
            self.tree.insert(value)

        preorder_result = self.tree.preorder_traversal()
        inorder_result = self.tree.inorder_traversal()
        postorder_result = self.tree.postorder_traversal()

        # All values should be present
        assert set(preorder_result) == set(values)
        assert set(inorder_result) == set(values)
        assert set(postorder_result) == set(values)

        # Length should match
        assert len(preorder_result) == len(values)
        assert len(inorder_result) == len(values)
        assert len(postorder_result) == len(values)

    def test_traversal_with_mixed_values(self) -> None:
        """Test traversals with mixed positive and negative values."""
        values = [-20, -10, 10, 20, -5, 5, -15, 15]
        for value in values:
            self.tree.insert(value)

        preorder_result = self.tree.preorder_traversal()
        inorder_result = self.tree.inorder_traversal()
        postorder_result = self.tree.postorder_traversal()

        # All values should be present
        assert set(preorder_result) == set(values)
        assert set(inorder_result) == set(values)
        assert set(postorder_result) == set(values)

        # Length should match
        assert len(preorder_result) == len(values)
        assert len(inorder_result) == len(values)
        assert len(postorder_result) == len(values)

    def test_is_balanced_empty_tree(self) -> None:
        """Test that an empty tree is considered balanced."""
        assert self.tree._is_balanced(self.tree.root) is True

    def test_is_balanced_single_node(self) -> None:
        """Test that a single node tree is considered balanced."""
        self.tree.insert(42)
        assert self.tree._is_balanced(self.tree.root) is True

    def test_huge_balanced_tree(self) -> None:
        """Test a large balanced tree."""
        values = list(range(1, 1001))
        for value in values:
            self.tree.insert(value)

        assert self.tree._is_balanced(self.tree.root) is True
        assert self.tree.root.value == 512
        assert self.tree.root.left.value == 256
        assert self.tree.root.right.value == 768
        assert self.tree.get_height(self.tree.root) == 10
        assert self.tree.preorder_traversal()[0:7] == [512, 256, 128, 64, 32, 16, 8]
        assert self.tree.inorder_traversal() == values
        assert self.tree.postorder_traversal()[0:7] == [1, 3, 2, 5, 7, 6, 4]


class TestAVLTreeHardcoded:
    """Hardcoded test cases with specific expected tree structures."""

    def setup_method(self) -> None:
        """Set up a fresh AVL tree for each test."""
        self.tree = AVLTree()

    def test_sequential_insertion_15_nodes(self) -> None:
        """Test sequential insertion of 15 nodes and verify exact structure."""
        # Insert values 1 through 15 sequentially
        values = list(range(1, 16))
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify specific structure after all rotations
        assert self.tree.root.value == 8  # Root should be 8
        assert self.tree.get_height(self.tree.root) == 4

        # Check left subtree
        assert self.tree.root.left.value == 4
        assert self.tree.root.left.left.value == 2
        assert self.tree.root.left.right.value == 6
        assert self.tree.root.left.left.left.value == 1
        assert self.tree.root.left.left.right.value == 3
        assert self.tree.root.left.right.left.value == 5
        assert self.tree.root.left.right.right.value == 7

        # Check right subtree
        assert self.tree.root.right.value == 12
        assert self.tree.root.right.left.value == 10
        assert self.tree.root.right.right.value == 14
        assert self.tree.root.right.left.left.value == 9
        assert self.tree.root.right.left.right.value == 11
        assert self.tree.root.right.right.left.value == 13
        assert self.tree.root.right.right.right.value == 15

        # Verify traversals
        expected_inorder = list(range(1, 16))
        expected_preorder = [8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15]
        expected_postorder = [1, 3, 2, 5, 7, 6, 4, 9, 11, 10, 13, 15, 14, 12, 8]

        assert self.tree.inorder_traversal() == expected_inorder
        assert self.tree.preorder_traversal() == expected_preorder
        assert self.tree.postorder_traversal() == expected_postorder

    def test_reverse_sequential_insertion_15_nodes(self) -> None:
        """Test reverse sequential insertion of 15 nodes."""
        # Insert values 15 down to 1
        values = list(range(15, 0, -1))
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Should result in same structure as sequential insertion
        assert self.tree.root.value == 8
        assert self.tree.get_height(self.tree.root) == 4

        # Verify traversals
        expected_inorder = list(range(1, 16))
        assert self.tree.inorder_traversal() == expected_inorder

    def test_fibonacci_sequence_insertion_20_nodes(self) -> None:
        """Test insertion using Fibonacci-like sequence."""
        # Insert in a pattern that creates various rotation scenarios
        values = [
            13,
            8,
            21,
            5,
            11,
            17,
            25,
            3,
            7,
            9,
            15,
            19,
            23,
            27,
            1,
            4,
            6,
            10,
            12,
            14,
        ]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify all values are present
        for value in values:
            assert self.tree.search(value) is not None

        # Verify inorder gives sorted sequence
        assert self.tree.inorder_traversal() == sorted(values)

        # Check tree height is logarithmic
        expected_max_height = 5  # For 20 nodes, height should be ≤ 5
        assert self.tree.get_height(self.tree.root) <= expected_max_height

        # Check preorder traversal
        expected_preorder = [
            13,
            8,
            5,
            3,
            1,
            4,
            7,
            6,
            10,
            9,
            11,
            12,
            21,
            17,
            15,
            14,
            19,
            25,
            23,
            27,
        ]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_powers_of_two_insertion_16_nodes(self) -> None:
        """Test insertion of powers of 2 and their neighbors."""
        # Insert powers of 2: 1, 2, 4, 8, 16, 32, 64, 128
        # Plus their neighbors to create interesting patterns
        values = [16, 8, 32, 4, 12, 24, 48, 2, 6, 10, 14, 20, 28, 40, 56, 1]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify structure - root should be well-balanced
        root_val = self.tree.root.value
        left_height = self.tree.get_height(self.tree.root.left)
        right_height = self.tree.get_height(self.tree.root.right)
        assert abs(left_height - right_height) <= 1

        # Verify all values present and sorted
        assert self.tree.inorder_traversal() == sorted(values)

        # Check preorder traversal
        expected_preorder = [16, 8, 4, 2, 1, 6, 12, 10, 14, 32, 24, 20, 28, 48, 40, 56]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_alternating_pattern_18_nodes(self) -> None:
        """Test alternating high-low insertion pattern."""
        # Alternate between high and low values to test various rotations
        values = [50, 10, 80, 5, 60, 90, 15, 45, 75, 95, 3, 12, 42, 55, 78, 92, 98, 1]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Check specific balance properties
        assert abs(self.tree.get_balance(self.tree.root)) <= 1

        # Verify inorder traversal is sorted
        inorder_result = self.tree.inorder_traversal()
        assert inorder_result == sorted(values)
        assert len(inorder_result) == len(values)

        # Check preorder traversal
        expected_preorder = [
            50,
            10,
            3,
            1,
            5,
            15,
            12,
            45,
            42,
            80,
            60,
            55,
            75,
            78,
            92,
            90,
            95,
            98,
        ]

        assert self.tree.preorder_traversal() == expected_preorder

    def test_middle_out_insertion_13_nodes(self) -> None:
        """Test insertion starting from middle values working outward."""
        # Start with middle values and work outward
        values = [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify root is reasonable (should be close to median)
        sorted_values = sorted(values)
        median = sorted_values[len(sorted_values) // 2]
        # Root should be within a reasonable range of the median
        assert abs(self.tree.root.value - median) <= 25

        # Verify traversals
        assert self.tree.inorder_traversal() == sorted_values

        # Check preorder traversal
        expected_preorder = [
            50,
            25,
            12,
            6,
            18,
            37,
            31,
            43,
            75,
            62,
            56,
            68,
            87,
        ]

    def test_deletion_maintains_balance_12_nodes(self) -> None:
        """Test that deletions maintain balance in a specific scenario."""
        # Insert 12 values
        values = [20, 10, 30, 5, 15, 25, 35, 3, 7, 12, 18, 28]
        for value in values:
            self.tree.insert(value)

        # Verify initial balance
        assert self.tree._is_balanced(self.tree.root)
        initial_height = self.tree.get_height(self.tree.root)

        # Check preorder traversal before deletion
        expected_preorder = [
            20,
            10,
            5,
            3,
            7,
            15,
            12,
            18,
            30,
            25,
            28,
            35,
        ]
        assert self.tree.preorder_traversal() == expected_preorder

        # Delete specific nodes that should trigger rebalancing
        delete_values = [3, 7, 28, 35]
        for value in delete_values:
            self.tree.delete(value)
            # Verify tree remains balanced after each deletion
            assert self.tree._is_balanced(self.tree.root)

        # Verify remaining values
        remaining_values = [v for v in values if v not in delete_values]
        for value in remaining_values:
            assert self.tree.search(value) is not None

        # Verify deleted values are gone
        for value in delete_values:
            assert self.tree.search(value) is None

        # Verify inorder is still sorted
        assert self.tree.inorder_traversal() == sorted(remaining_values)

        # # Check preorder traversal
        expected_preorder = [20, 10, 5, 15, 12, 18, 30, 25]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_worst_case_avl_pattern_14_nodes(self) -> None:
        """Test a pattern that would be worst-case for regular BST but balanced in AVL."""
        # This pattern would create a completely unbalanced BST
        # but AVL should keep it balanced
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Height should be logarithmic, not linear
        # For 14 nodes, height should be ≤ 4 (log₂(14) ≈ 3.8)
        assert self.tree.get_height(self.tree.root) <= 4

        # Verify structure is actually balanced
        def check_subtree_balance(node):
            if not node:
                return True
            balance = self.tree.get_balance(node)
            return (
                abs(balance) <= 1
                and check_subtree_balance(node.left)
                and check_subtree_balance(node.right)
            )

        assert check_subtree_balance(self.tree.root)

        # Check preorder traversal
        expected_preorder = [8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 13, 14]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_mixed_operations_scenario_16_nodes(self) -> None:
        """Test mixed insertions and deletions maintaining balance."""
        # Phase 1: Insert initial values
        initial_values = [40, 20, 60, 10, 30, 50, 70, 5, 15, 25, 35]
        for value in initial_values:
            self.tree.insert(value)

        assert self.tree._is_balanced(self.tree.root)

        # Phase 2: Add more values
        additional_values = [45, 55, 65, 75, 3]
        for value in additional_values:
            self.tree.insert(value)

        assert self.tree._is_balanced(self.tree.root)

        # Phase 3: Delete some values
        delete_values = [5, 15, 65, 75]
        for value in delete_values:
            self.tree.delete(value)
            assert self.tree._is_balanced(self.tree.root)

        # Verify final state
        all_values = initial_values + additional_values
        remaining_values = [v for v in all_values if v not in delete_values]

        assert self.tree.inorder_traversal() == sorted(remaining_values)
        assert len(self.tree.inorder_traversal()) == len(remaining_values)

        # Check preorder traversal
        expected_preorder = [40, 20, 10, 3, 30, 25, 35, 60, 50, 45, 55, 70]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_negative_positive_mix_19_nodes(self) -> None:
        """Test with mix of negative and positive values."""
        values = [
            -50,
            -25,
            0,
            25,
            50,
            -75,
            -12,
            -6,
            12,
            37,
            62,
            -80,
            -30,
            -3,
            3,
            18,
            42,
            55,
            75,
        ]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Verify all values present
        for value in values:
            assert self.tree.search(value) is not None

        # Verify inorder gives sorted sequence
        assert self.tree.inorder_traversal() == sorted(values)

        # Check preorder traversal before deletion
        expected_preorder = [
            0,
            -25,
            -75,
            -80,
            -50,
            -30,
            -6,
            -12,
            -3,
            25,
            12,
            3,
            18,
            50,
            37,
            42,
            62,
            55,
            75,
        ]
        assert self.tree.preorder_traversal() == expected_preorder

        # TODO: Incrivelmente o site https://cmps-people.ok.ubc.ca/ylucet/DS/AVLtree.html (ou https://www.cs.usfca.edu/~galles/visualization/AVLtree.html) dá uma árvore diferente.
        # TODO: O site https://www.thebugger.us/interactive-avl-tree-visualization/ e o https://visualgo.net/en/bst confirmam a árvore gerada aqui.

        # Test some deletions
        delete_values = [-80, -3, 18, 75]
        for value in delete_values:
            self.tree.delete(value)
            assert self.tree._is_balanced(self.tree.root)

        remaining = [v for v in values if v not in delete_values]
        assert self.tree.inorder_traversal() == sorted(remaining)

        # Check preorder traversal
        expected_preorder = [
            0,
            -25,
            -50,
            -75,
            -30,
            -6,
            -12,
            25,
            12,
            3,
            50,
            37,
            42,
            62,
            55,
        ]
        assert self.tree.preorder_traversal() == expected_preorder

    def test_edge_case_small_values_11_nodes(self) -> None:
        """Test with small integer values that might cause edge cases."""
        values = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5]
        for value in values:
            self.tree.insert(value)

        # Verify tree is balanced
        assert self.tree._is_balanced(self.tree.root)

        # Root should be 0 or close to it
        assert abs(self.tree.root.value) <= 1

        # Verify perfect sorting
        assert self.tree.inorder_traversal() == sorted(values)

        # Test that balance is maintained throughout
        for node_val in values:
            node = self.tree.search(node_val)
            if node:
                assert abs(self.tree.get_balance(node)) <= 1
