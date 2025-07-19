# """
# Tests for the CLI interface of AVLTreeCLI.

# Tests cover:
# - Command parsing and validation
# - Number range validation (-99 to 999)
# - Tree visualization and formatting
# - User input handling
# - Error cases and edge conditions
# - Integration with AVL tree operations
# """

# import sys
# from io import StringIO
# from typing import List
# from unittest.mock import MagicMock, patch

# import pytest

# from avltreecli.avl_tree import AVLTree
# from avltreecli.cli import AVLTreeCLI


# class TestAVLTreeCLI:
#     """Test cases for the AVL Tree CLI interface."""

#     def setup_method(self) -> None:
#         """Set up a fresh CLI instance for each test."""
#         self.cli = AVLTreeCLI()

#     def test_cli_initialization(self) -> None:
#         """Test that CLI is initialized correctly."""
#         assert isinstance(self.cli.tree, AVLTree)
#         assert self.cli.tree.root is None

#     def test_parse_command_insert_valid(self) -> None:
#         """Test parsing valid insert commands."""
#         # Test single insert
#         assert self.cli.parse_command("insert 10") == ("insert", [10])
#         assert self.cli.parse_command("INSERT 10") == ("insert", [10])
#         assert self.cli.parse_command("  insert   10  ") == ("insert", [10])

#         # Test multiple inserts
#         assert self.cli.parse_command("insert 10 20 30") == ("insert", [10, 20, 30])
#         assert self.cli.parse_command("insert -5 0 5") == ("insert", [-5, 0, 5])

#     def test_parse_command_delete_valid(self) -> None:
#         """Test parsing valid delete commands."""
#         assert self.cli.parse_command("delete 10") == ("delete", [10])
#         assert self.cli.parse_command("DELETE 10") == ("delete", [10])
#         assert self.cli.parse_command("delete -5") == ("delete", [-5])
#         assert self.cli.parse_command("delete 10 20 30") == ("delete", [10, 20, 30])

#     def test_parse_command_search_valid(self) -> None:
#         """Test parsing valid search commands."""
#         assert self.cli.parse_command("search 10") == ("search", [10])
#         assert self.cli.parse_command("SEARCH 10") == ("search", [10])
#         assert self.cli.parse_command("search -5") == ("search", [-5])

#     def test_parse_command_display(self) -> None:
#         """Test parsing display command."""
#         assert self.cli.parse_command("display") == ("display", [])
#         assert self.cli.parse_command("DISPLAY") == ("display", [])
#         assert self.cli.parse_command("  display  ") == ("display", [])

#     def test_parse_command_clear(self) -> None:
#         """Test parsing clear command."""
#         assert self.cli.parse_command("clear") == ("clear", [])
#         assert self.cli.parse_command("CLEAR") == ("clear", [])

#     def test_parse_command_help(self) -> None:
#         """Test parsing help command."""
#         assert self.cli.parse_command("help") == ("help", [])
#         assert self.cli.parse_command("HELP") == ("help", [])

#     def test_parse_command_quit(self) -> None:
#         """Test parsing quit commands."""
#         assert self.cli.parse_command("quit") == ("quit", [])
#         assert self.cli.parse_command("exit") == ("quit", [])
#         assert self.cli.parse_command("q") == ("quit", [])

#     def test_parse_command_invalid(self) -> None:
#         """Test parsing invalid commands."""
#         assert self.cli.parse_command("invalid") == ("unknown", [])
#         assert self.cli.parse_command("") == ("unknown", [])
#         assert self.cli.parse_command("   ") == ("unknown", [])

#     def test_validate_number_valid_range(self) -> None:
#         """Test number validation for valid range (-99 to 999)."""
#         valid_numbers = [-99, -50, -1, 0, 1, 50, 99, 100, 500, 999]
#         for num in valid_numbers:
#             assert self.cli.validate_number(num) is True

#     def test_validate_number_invalid_range(self) -> None:
#         """Test number validation for invalid range."""
#         invalid_numbers = [-100, -150, -1000, 1000, 1500, 2000]
#         for num in invalid_numbers:
#             assert self.cli.validate_number(num) is False

#     def test_parse_numbers_valid(self) -> None:
#         """Test parsing valid number strings."""
#         assert self.cli.parse_numbers(["10"]) == [10]
#         assert self.cli.parse_numbers(["10", "20", "30"]) == [10, 20, 30]
#         assert self.cli.parse_numbers(["-5", "0", "5"]) == [-5, 0, 5]
#         assert self.cli.parse_numbers(["999", "-99"]) == [999, -99]

#     def test_parse_numbers_invalid_format(self) -> None:
#         """Test parsing invalid number formats."""
#         assert self.cli.parse_numbers(["abc"]) == []
#         assert self.cli.parse_numbers(["10.5"]) == []
#         assert self.cli.parse_numbers(["10", "abc", "20"]) == []

#     def test_parse_numbers_out_of_range(self) -> None:
#         """Test parsing numbers out of valid range."""
#         assert self.cli.parse_numbers(["1000"]) == []
#         assert self.cli.parse_numbers(["-100"]) == []
#         assert self.cli.parse_numbers(["10", "1000"]) == []

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_insert(self, mock_console: MagicMock) -> None:
#         """Test executing insert commands."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Test single insert
#         with patch.object(self.cli, "parse_numbers", return_value=[10]):
#             self.cli.execute_command("insert", ["10"])
#             assert self.cli.tree.search(10) is not None

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_delete(self, mock_console: MagicMock) -> None:
#         """Test executing delete commands."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Insert then delete
#         self.cli.tree.insert(10)
#         with patch.object(self.cli, "parse_numbers", return_value=[10]):
#             self.cli.execute_command("delete", ["10"])
#             assert self.cli.tree.search(10) is None

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_search_found(self, mock_console: MagicMock) -> None:
#         """Test searching for existing values."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Insert value then search
#         self.cli.tree.insert(10)
#         with patch.object(self.cli, "parse_numbers", return_value=[10]):
#             self.cli.execute_command("search", ["10"])
#             # Verify success message was printed
#             mock_console_instance.print.assert_called()

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_search_not_found(self, mock_console: MagicMock) -> None:
#         """Test searching for non-existing values."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         with patch.object(self.cli, "parse_numbers", return_value=[10]):
#             self.cli.execute_command("search", ["10"])
#             # Verify not found message was printed
#             mock_console_instance.print.assert_called()

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_clear(self, mock_console: MagicMock) -> None:
#         """Test clearing the tree."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Insert values then clear
#         self.cli.tree.insert(10)
#         self.cli.tree.insert(20)
#         self.cli.execute_command("clear", [])
#         assert self.cli.tree.root is None

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_help(self, mock_console: MagicMock) -> None:
#         """Test help command."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         self.cli.execute_command("help", [])
#         # Verify help text was printed
#         mock_console_instance.print.assert_called()

#     @patch("avltreecli.cli.Console")
#     def test_execute_command_invalid_numbers(self, mock_console: MagicMock) -> None:
#         """Test executing commands with invalid number parsing."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         with patch.object(self.cli, "parse_numbers", return_value=[]):
#             self.cli.execute_command("insert", ["abc"])
#             # Should print error message
#             mock_console_instance.print.assert_called()

#     def test_get_tree_height_empty(self) -> None:
#         """Test getting height of empty tree."""
#         assert self.cli.get_tree_height() == 0

#     def test_get_tree_height_with_nodes(self) -> None:
#         """Test getting height of tree with nodes."""
#         self.cli.tree.insert(10)
#         assert self.cli.get_tree_height() == 1

#         self.cli.tree.insert(5)
#         self.cli.tree.insert(15)
#         assert self.cli.get_tree_height() >= 2

#     def test_collect_tree_nodes_empty(self) -> None:
#         """Test collecting nodes from empty tree."""
#         nodes = self.cli.collect_tree_nodes()
#         assert nodes == []

#     def test_collect_tree_nodes_with_values(self) -> None:
#         """Test collecting nodes from tree with values."""
#         values = [10, 5, 15, 3, 7]
#         for value in values:
#             self.cli.tree.insert(value)

#         nodes = self.cli.collect_tree_nodes()
#         node_values = [node.value for node in nodes]

#         # All inserted values should be present
#         for value in values:
#             assert value in node_values

#     def test_format_tree_empty(self) -> None:
#         """Test formatting empty tree."""
#         result = self.cli.format_tree()
#         assert "empty" in result.lower()

#     def test_format_tree_with_nodes(self) -> None:
#         """Test formatting tree with nodes."""
#         self.cli.tree.insert(10)
#         self.cli.tree.insert(5)
#         self.cli.tree.insert(15)

#         result = self.cli.format_tree()
#         # Should contain the values in some format
#         assert "10" in result
#         assert "5" in result
#         assert "15" in result

#     @patch("builtins.input")
#     @patch("avltreecli.cli.Console")
#     def test_run_quit_command(
#         self, mock_console: MagicMock, mock_input: MagicMock
#     ) -> None:
#         """Test that quit command exits the run loop."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance
#         mock_input.return_value = "quit"

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Should exit without error
#         self.cli.run()

#     @patch("builtins.input")
#     @patch("avltreecli.cli.Console")
#     def test_run_with_commands(
#         self, mock_console: MagicMock, mock_input: MagicMock
#     ) -> None:
#         """Test running CLI with a sequence of commands."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Simulate a sequence of commands
#         mock_input.side_effect = ["insert 10", "insert 5", "display", "quit"]

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         self.cli.run()

#         # Verify tree has the inserted values
#         assert self.cli.tree.search(10) is not None
#         assert self.cli.tree.search(5) is not None

#     @patch("builtins.input")
#     @patch("avltreecli.cli.Console")
#     def test_run_with_keyboard_interrupt(
#         self, mock_console: MagicMock, mock_input: MagicMock
#     ) -> None:
#         """Test handling KeyboardInterrupt during run."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance
#         mock_input.side_effect = KeyboardInterrupt()

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Should handle KeyboardInterrupt gracefully
#         self.cli.run()


# class TestCLIIntegration:
#     """Integration tests for CLI with AVL tree operations."""

#     def setup_method(self) -> None:
#         """Set up for integration tests."""
#         self.cli = AVLTreeCLI()

#     def test_full_workflow(self) -> None:
#         """Test a complete workflow of operations."""
#         # Insert multiple values
#         self.cli.tree.insert(50)
#         self.cli.tree.insert(25)
#         self.cli.tree.insert(75)
#         self.cli.tree.insert(10)
#         self.cli.tree.insert(30)

#         # Verify all values are present
#         for value in [50, 25, 75, 10, 30]:
#             assert self.cli.tree.search(value) is not None

#         # Delete some values
#         self.cli.tree.delete(25)
#         self.cli.tree.delete(10)

#         # Verify deleted values are gone
#         assert self.cli.tree.search(25) is None
#         assert self.cli.tree.search(10) is None

#         # Verify remaining values are still present
#         for value in [50, 75, 30]:
#             assert self.cli.tree.search(value) is not None

#     def test_edge_case_values(self) -> None:
#         """Test CLI with edge case values."""
#         # Test boundary values
#         boundary_values = [-99, -1, 0, 1, 999]

#         for value in boundary_values:
#             assert self.cli.validate_number(value) is True
#             self.cli.tree.insert(value)
#             assert self.cli.tree.search(value) is not None

#     def test_large_tree_formatting(self) -> None:
#         """Test formatting performance with larger trees."""
#         # Insert many values
#         for i in range(1, 32):  # Creates a reasonably sized tree
#             self.cli.tree.insert(i)

#         # Should be able to format without error
#         result = self.cli.format_tree()
#         assert isinstance(result, str)
#         assert len(result) > 0

#     @patch("avltreecli.cli.Console")
#     def test_error_handling_in_execute(self, mock_console: MagicMock) -> None:
#         """Test error handling in command execution."""
#         mock_console_instance = MagicMock()
#         mock_console.return_value = mock_console_instance

#         # Re-initialize CLI with mocked console
#         self.cli = AVLTreeCLI()

#         # Test with unknown command
#         self.cli.execute_command("unknown", [])

#         # Should handle gracefully
#         mock_console_instance.print.assert_called()


# # Parametrized tests for comprehensive CLI testing
# class TestCLIParametrized:
#     """Parametrized tests for CLI functionality."""

#     @pytest.fixture
#     def cli(self) -> AVLTreeCLI:
#         """Fixture to provide a fresh CLI for each test."""
#         return AVLTreeCLI()

#     @pytest.mark.parametrize(
#         "command,args,expected",
#         [
#             ("insert 10", None, ("insert", [10])),
#             ("delete 5", None, ("delete", [5])),
#             ("search 15", None, ("search", [15])),
#             ("display", None, ("display", [])),
#             ("clear", None, ("clear", [])),
#             ("help", None, ("help", [])),
#             ("quit", None, ("quit", [])),
#             ("invalid", None, ("unknown", [])),
#         ],
#     )
#     def test_command_parsing_parametrized(
#         self, cli: AVLTreeCLI, command: str, args: None, expected: tuple
#     ) -> None:
#         """Test command parsing with various inputs."""
#         result = cli.parse_command(command)
#         assert result == expected

#     @pytest.mark.parametrize(
#         "numbers,expected",
#         [
#             ([-99], True),
#             ([0], True),
#             ([999], True),
#             ([-100], False),
#             ([1000], False),
#             ([500, 600], True),
#             ([500, 1000], False),  # One invalid makes all invalid
#         ],
#     )
#     def test_number_validation_parametrized(
#         self, cli: AVLTreeCLI, numbers: List[int], expected: bool
#     ) -> None:
#         """Test number validation with various inputs."""
#         if expected:
#             # All numbers should be valid
#             for num in numbers:
#                 assert cli.validate_number(num) is True
#         else:
#             # At least one number should be invalid
#             valid_count = sum(1 for num in numbers if cli.validate_number(num))
#             assert valid_count < len(numbers)
