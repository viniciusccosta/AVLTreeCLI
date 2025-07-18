from rich import print as rprint
from rich.console import Console

from .avl_tree import AVLTree, Node


class AVLTreeCLI:
    def __init__(self):
        self.tree = AVLTree()
        self.console = Console()

        # Configuration settings
        self.auto_show_tree = True  # Show tree after every command
        self.mode = "automatic"  # Modes: "automatic", "practice"
        self.show_steps = True  # Show each step during automatic rotations

        # Visual enhancements
        self.recently_added = None  # Track the most recently added node
        self.recently_removed = None  # Track the most recently removed node

    def run(self):
        self.console.clear()
        rprint("[bold green]AVL Tree Practice Tool[/bold green]")
        rprint(f"[bold]Mode:[/bold] {self.mode.title()}")
        rprint(f"[bold]Auto-show tree:[/bold] {'On' if self.auto_show_tree else 'Off'}")
        rprint(f"[bold]Show steps:[/bold] {'On' if self.show_steps else 'Off'}\n")
        rprint("Type 'help' for commands.")
        while True:
            command_line = input("> ").strip().lower()
            if command_line == "exit":
                break
            self.process_command_line(command_line)

    def process_command_line(self, command_line):
        """Process a line that may contain multiple commands"""
        if not command_line:
            return

        # Split the command line into individual commands
        commands = self._parse_multiple_commands(command_line)

        for command in commands:
            if command == "exit":
                return
            self.process_command(command)

    def _parse_multiple_commands(self, command_line):
        """Parse a command line into individual commands"""
        commands = []
        parts = command_line.split()
        i = 0

        while i < len(parts):
            cmd = parts[i]

            # Single word commands
            if cmd in [
                "tree",
                "clear",
                "reset",
                "status",
                "hint",
                "preorder",
                "inorder",
                "postorder",
                "help",
                "exit",
            ]:
                commands.append(cmd)
                i += 1

            # Commands that take one argument
            elif cmd in ["a", "d", "rr", "rl"] and i + 1 < len(parts):
                commands.append(f"{cmd} {parts[i + 1]}")
                i += 2

            # Commands that take two arguments
            elif cmd == "rotate" and i + 2 < len(parts):
                commands.append(f"{cmd} {parts[i + 1]} {parts[i + 2]}")
                i += 3

            # Config commands that take two arguments
            elif cmd == "config" and i + 2 < len(parts):
                commands.append(f"{cmd} {parts[i + 1]} {parts[i + 2]}")
                i += 3

            # If we can't parse the command properly, treat it as a single command
            else:
                commands.append(cmd)
                i += 1

        return commands

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "a" and len(args) == 1:
                value = int(args[0])

                # Check if value already exists in the tree
                if self.tree.search(value):
                    rprint(
                        f"[red]Value {value} already exists in the tree! Cannot add duplicates.[/red]"
                    )
                    return

                self.recently_added = value  # Track the recently added node
                self.recently_removed = None  # Clear recently removed
                if self.mode == "automatic":
                    self._insert_with_auto_balance(value)
                elif self.mode == "practice":
                    # Check if tree is already unbalanced
                    if self._find_unbalanced_node(self.tree.root):
                        rprint(
                            "[yellow]Tree is currently unbalanced! Please balance it first before adding new nodes.[/yellow]"
                        )
                        rprint(
                            "[yellow]Use 'hint' command for guidance on how to balance it.[/yellow]"
                        )
                        return
                    # In practice mode, insert without auto-balancing
                    self.tree.root = self._insert_manual(self.tree.root, value)
                    self._check_balance_and_guide()
                rprint(f"[green]Added {value} to the tree[/green]")
                if self.auto_show_tree:
                    self.display_tree()

                # In automatic mode, clear recently added tracking after final display
                # only if the tree is balanced (so green shows during steps but clears after)
                if self.mode == "automatic" and not self._find_unbalanced_node(
                    self.tree.root
                ):
                    self.recently_added = None

            elif cmd == "d" and len(args) == 1:
                value = int(args[0])

                # Check if value exists in the tree before trying to remove it
                if not self.tree.search(value):
                    rprint(
                        f"[red]Value {value} not found in the tree! Cannot remove.[/red]"
                    )
                    return

                self.recently_removed = value  # Track the recently removed node
                self.recently_added = None  # Clear recently added
                if self.mode == "automatic":
                    self._delete_with_auto_balance(value)
                elif self.mode == "practice":
                    # Check if tree is already unbalanced
                    if self._find_unbalanced_node(self.tree.root):
                        rprint(
                            "[yellow]Tree is currently unbalanced! Please balance it first before removing nodes.[/yellow]"
                        )
                        rprint(
                            "[yellow]Use 'hint' command for guidance on how to balance it.[/yellow]"
                        )
                        return
                    # In practice mode, delete without auto-balancing
                    self.tree.root = self._delete_manual(self.tree.root, value)
                    self._check_balance_and_guide()
                rprint(f"[green]Removed {value} from the tree[/green]")
                if self.auto_show_tree:
                    self.display_tree()

                # In automatic mode, clear recently removed tracking after final display
                # only if the tree is balanced (so coloring shows during steps but clears after)
                if self.mode == "automatic" and not self._find_unbalanced_node(
                    self.tree.root
                ):
                    self.recently_removed = None

            elif cmd in ["rr", "rl"] and len(args) == 1:
                if self.mode == "automatic":
                    rprint(
                        "[yellow]Rotate commands are disabled in automatic mode[/yellow]"
                    )
                    return

                # Handle different command formats
                if cmd == "rr":
                    direction = "right"
                    value = int(args[0])
                elif cmd == "rl":
                    direction = "left"
                    value = int(args[0])

                node = self.tree.search(value)
                if not node:
                    rprint("[red]Node not found[/red]")
                    return

                if self.mode == "practice":
                    if not self._is_rotation_needed(value, direction):
                        rprint(
                            "[yellow]This rotation is not needed or correct right now. Try to balance the tree properly.[/yellow]"
                        )
                        return

                if direction == "left":
                    # Find parent to properly update tree structure
                    if node == self.tree.root:
                        self.tree.root = self.tree.left_rotate(node)
                    else:
                        self._rotate_node_and_update_parent(node, "left")
                    # Update heights throughout the tree after manual rotation
                    self._update_all_heights(self.tree.root)
                    rprint(f"[green]Performed left rotation on node {value}[/green]")
                elif direction == "right":
                    # Find parent to properly update tree structure
                    if node == self.tree.root:
                        self.tree.root = self.tree.right_rotate(node)
                    else:
                        self._rotate_node_and_update_parent(node, "right")
                    # Update heights throughout the tree after manual rotation
                    self._update_all_heights(self.tree.root)
                    rprint(f"[green]Performed right rotation on node {value}[/green]")
                else:
                    rprint("[red]Use 'left' or 'right'[/red]")
                    return

                # Clear recently added/removed tracking after rotation
                self.recently_added = None
                self.recently_removed = None

                if self.auto_show_tree:
                    self.display_tree()

                # After rotation in practice mode, check if tree is now balanced
                if self.mode == "practice":
                    self._check_balance_and_guide()

            elif cmd == "config" and len(args) >= 2:
                self._handle_config(args)

            elif cmd == "clear":
                self.console.clear()
                rprint("[bold green]AVL Tree Practice Tool[/bold green]")
                rprint(f"[bold]Mode:[/bold] {self.mode.title()}")
                rprint(
                    f"[bold]Auto-show tree:[/bold] {'On' if self.auto_show_tree else 'Off'}"
                )
                rprint(
                    f"[bold]Show steps:[/bold] {'On' if self.show_steps else 'Off'}\n"
                )
                rprint("[green]Screen cleared[/green]")
                if self.auto_show_tree and self.tree.root:
                    self.display_tree()

            elif cmd == "reset":
                self.tree = AVLTree()
                self.recently_added = None
                self.recently_removed = None
                rprint("[green]Tree reset[/green]")
                if self.auto_show_tree:
                    self.display_tree()

            elif cmd == "tree":
                self.display_tree()
                return

            elif cmd == "status":
                self._show_status()
                return

            elif cmd == "hint":
                self._show_hint()
                return

            elif cmd == "preorder":
                self._show_preorder()
                return

            elif cmd == "inorder":
                self._show_inorder()
                return

            elif cmd == "postorder":
                self._show_postorder()
                return

            elif cmd == "help":
                self.show_help()
                return
            else:
                rprint("[red]Invalid command. Try 'help'.[/red]")
                return
        except ValueError:
            rprint("[red]Invalid number[/red]")

    def display_tree(self):
        """Display the tree in a fancy grid format with visual connectors"""
        if not self.tree.root:
            rprint("[yellow]Tree is empty[/yellow]")
            return

        # Calculate tree dimensions
        height = self._get_tree_height(self.tree.root)
        cols = 2**height - 1  # Total columns needed

        # Create a grid to hold the tree with color information
        grid = [
            [{"value": " ", "color": None} for _ in range(cols)] for _ in range(height)
        ]

        # Get all nodes organized by level
        levels = self._get_tree_levels_with_positions(self.tree.root)

        # Get unbalanced nodes for coloring
        unbalanced_nodes = self._get_all_unbalanced_nodes(self.tree.root)

        # Place nodes and connectors in the grid
        for level_idx, level_nodes in enumerate(levels):
            if level_idx >= height:
                break

            # Calculate positions for this level
            positions = self._calculate_level_positions(level_idx, height, cols)

            # Place each node at its calculated position with appropriate color
            for i, node in enumerate(level_nodes):
                if i < len(positions) and node is not None:
                    col = positions[i]
                    if 0 <= col < cols:
                        node_value = str(node.value)
                        node_color = self._get_node_color(node.value, unbalanced_nodes)
                        grid[level_idx][col] = {
                            "value": node_value,
                            "color": node_color,
                        }

                        # Add connectors if not the last level
                        if level_idx < height - 1:
                            # Add ╩ below parent if it has children
                            if node.left or node.right:
                                if level_idx + 1 < height:
                                    grid[level_idx + 1][col] = {
                                        "value": "╩",
                                        "color": None,
                                    }

                            # Add connecting lines for left child
                            if node.left and level_idx + 1 < len(levels):
                                left_positions = self._calculate_level_positions(
                                    level_idx + 1, height, cols
                                )
                                left_child_idx = i * 2
                                if left_child_idx < len(left_positions):
                                    left_col = left_positions[left_child_idx]
                                    if left_col < col and level_idx + 1 < height:
                                        # Fill the path from trunk to left child with '<'
                                        for path_col in range(left_col + 1, col):
                                            grid[level_idx + 1][path_col] = {
                                                "value": "<",
                                                "color": None,
                                            }

                            # Add connecting lines for right child
                            if node.right and level_idx + 1 < len(levels):
                                right_positions = self._calculate_level_positions(
                                    level_idx + 1, height, cols
                                )
                                right_child_idx = i * 2 + 1
                                if right_child_idx < len(right_positions):
                                    right_col = right_positions[right_child_idx]
                                    if right_col > col and level_idx + 1 < height:
                                        # Fill the path from trunk to right child with '>'
                                        for path_col in range(col + 1, right_col):
                                            grid[level_idx + 1][path_col] = {
                                                "value": ">",
                                                "color": None,
                                            }

        # Print the fancy grid with colors and connectors
        self._print_fancy_grid_colored(grid)

    def _calculate_level_positions(self, level, height, cols):
        """Calculate positions for nodes at a specific level using the mathematical formula"""
        nodes_at_level = 2**level

        if level == 0:
            # Root is at the center
            return [cols // 2]

        # Calculate leading space and space between nodes
        leading_space = 2 ** (height - level - 1) - 1
        space_between = 2 ** (height - level) - 1

        positions = []
        for i in range(nodes_at_level):
            if i == 0:
                # First node position
                pos = leading_space
            else:
                # Subsequent nodes
                pos = leading_space + i * (space_between + 1)
            positions.append(pos)

        return positions

    def _get_tree_levels_with_positions(self, root):
        """Get nodes organized by level in breadth-first order, including None for missing nodes"""
        if not root:
            return []

        levels = []
        current_level = [root]

        while current_level and any(node is not None for node in current_level):
            # Add current level to levels
            levels.append(current_level[:])

            # Generate next level
            next_level = []
            for node in current_level:
                if node:
                    next_level.extend([node.left, node.right])
                else:
                    next_level.extend([None, None])

            current_level = next_level

        return levels

    def _rotate_node_and_update_parent(self, node, direction):
        """Rotate a node and update its parent's reference"""
        # Find the parent of the node
        parent = None
        current = self.tree.root

        while current and current != node:
            parent = current
            if node.value < current.value:
                current = current.left
            else:
                current = current.right

        # Perform the rotation
        if direction == "left":
            rotated_node = self.tree.left_rotate(node)
        else:
            rotated_node = self.tree.right_rotate(node)

        # Update parent's reference
        if parent:
            if parent.left == node:
                parent.left = rotated_node
            else:
                parent.right = rotated_node
        else:
            # This shouldn't happen as we check for root above
            self.tree.root = rotated_node

    def _update_all_heights(self, node):
        """Update heights for all nodes in the tree (post-order traversal)"""
        if not node:
            return

        # Update children first
        self._update_all_heights(node.left)
        self._update_all_heights(node.right)

        # Update current node's height
        node.height = 1 + max(
            self.tree.get_height(node.left), self.tree.get_height(node.right)
        )

    def _handle_config(self, args):
        """Handle configuration commands"""
        if len(args) < 2:
            rprint("[red]Usage: config <setting> <value>[/red]")
            return

        setting = args[0]
        value = args[1]

        if setting == "autoshow":
            if value in ["on", "true", "1"]:
                self.auto_show_tree = True
                rprint("[green]Auto-show tree enabled[/green]")
            elif value in ["off", "false", "0"]:
                self.auto_show_tree = False
                rprint("[green]Auto-show tree disabled[/green]")
            else:
                rprint("[red]Use 'on' or 'off'[/red]")

        elif setting == "mode":
            if value in ["automatic", "practice"]:
                self.mode = value
                rprint(f"[green]Mode set to {value}[/green]")
                if value == "automatic":
                    rprint(
                        "[yellow]Note: Rotate commands are disabled in automatic mode[/yellow]"
                    )
                elif value == "practice":
                    rprint(
                        "[yellow]Note: Only correct rotations are allowed in practice mode[/yellow]"
                    )
            else:
                rprint("[red]Valid modes: automatic, practice[/red]")

        elif setting == "steps":
            if value in ["on", "true", "1"]:
                self.show_steps = True
                rprint("[green]Show steps enabled[/green]")
            elif value in ["off", "false", "0"]:
                self.show_steps = False
                rprint("[green]Show steps disabled[/green]")
            else:
                rprint("[red]Use 'on' or 'off'[/red]")
        else:
            rprint("[red]Unknown setting. Use: autoshow, mode, or steps[/red]")

    def _insert_with_auto_balance(self, value):
        """Insert with automatic balancing and step-by-step display"""
        # First insert without auto-balancing to show unbalanced state
        self.tree.root = self._insert_manual(self.tree.root, value)

        if self.show_steps and self.auto_show_tree:
            # Check if tree became unbalanced
            unbalanced_node = self._find_unbalanced_node(self.tree.root)
            if unbalanced_node:
                rprint("[yellow]After insertion (before balancing):[/yellow]")
                self.display_tree()
                rprint(
                    f"[yellow]Tree is unbalanced! Node {unbalanced_node.value} has balance factor {self.tree.get_balance(unbalanced_node)}[/yellow]"
                )

        # Now check and apply rotations step by step
        self._balance_tree_with_steps()

    def _delete_with_auto_balance(self, value):
        """Delete with automatic balancing and step-by-step display"""
        # First delete without auto-balancing to show unbalanced state
        self.tree.root = self._delete_manual(self.tree.root, value)

        if self.show_steps and self.auto_show_tree:
            # Check if tree became unbalanced
            unbalanced_node = self._find_unbalanced_node(self.tree.root)
            if unbalanced_node:
                rprint("[yellow]After deletion (before balancing):[/yellow]")
                self.display_tree()
                rprint(
                    f"[yellow]Tree is unbalanced! Node {unbalanced_node.value} has balance factor {self.tree.get_balance(unbalanced_node)}[/yellow]"
                )

        # Now check and apply rotations step by step
        self._balance_tree_with_steps()

    def _insert_manual(self, node, value):
        """Insert without automatic balancing"""
        if not node:
            return Node(value)
        elif value < node.value:
            node.left = self._insert_manual(node.left, value)
        else:
            node.right = self._insert_manual(node.right, value)

        node.height = 1 + max(
            self.tree.get_height(node.left), self.tree.get_height(node.right)
        )
        return node

    def _delete_manual(self, node, value):
        """Delete without automatic balancing"""
        if not node:
            return node
        elif value < node.value:
            node.left = self._delete_manual(node.left, value)
        elif value > node.value:
            node.right = self._delete_manual(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self.tree.get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_manual(node.right, temp.value)

        node.height = 1 + max(
            self.tree.get_height(node.left), self.tree.get_height(node.right)
        )
        return node

    def _balance_tree_with_steps(self):
        """Balance the tree step by step, showing each rotation"""
        step = 1
        while True:
            unbalanced_node = self._find_unbalanced_node(self.tree.root)
            if not unbalanced_node:
                if step > 1 and self.show_steps and self.auto_show_tree:
                    rprint("[green]Tree is now balanced![/green]")
                break

            if self.show_steps and self.auto_show_tree:
                balance = self.tree.get_balance(unbalanced_node)
                rprint(
                    f"[yellow]Step {step}: Balancing node {unbalanced_node.value} (balance: {balance})[/yellow]"
                )

                # Show what rotation will be performed
                if balance > 1:
                    left_balance = self.tree.get_balance(unbalanced_node.left)
                    if left_balance >= 0:
                        rprint(
                            f"[yellow]Performing right rotation on node {unbalanced_node.value}[/yellow]"
                        )
                    else:
                        rprint(
                            f"[yellow]Performing left-right rotation: first left on {unbalanced_node.left.value}, then right on {unbalanced_node.value}[/yellow]"
                        )
                else:
                    right_balance = self.tree.get_balance(unbalanced_node.right)
                    if right_balance <= 0:
                        rprint(
                            f"[yellow]Performing left rotation on node {unbalanced_node.value}[/yellow]"
                        )
                    else:
                        rprint(
                            f"[yellow]Performing right-left rotation: first right on {unbalanced_node.right.value}, then left on {unbalanced_node.value}[/yellow]"
                        )

            # Apply the rotation with detailed steps for double rotations
            self.tree.root = self._balance_node_and_update_root_with_steps(
                unbalanced_node, step
            )

            step += 1

    def _balance_node_and_update_root_with_steps(self, target_node, step_num):
        """Balance a specific node showing individual rotation steps"""
        # Find the parent of the target node
        parent = None
        current = self.tree.root

        while current and current != target_node:
            parent = current
            if target_node.value < current.value:
                current = current.left
            else:
                current = current.right

        balance = self.tree.get_balance(target_node)
        balanced_node = None

        # Handle double rotations with intermediate steps
        if balance > 1:  # Left heavy
            left_balance = self.tree.get_balance(target_node.left)
            if left_balance < 0:  # Left-Right case
                # First rotation: left on left child
                if self.show_steps and self.auto_show_tree:
                    rprint(
                        f"[yellow]Step {step_num}a: Left rotation on node {target_node.left.value}[/yellow]"
                    )
                target_node.left = self.tree.left_rotate(target_node.left)

                # Update parent reference after first rotation
                if parent is None:
                    self.tree.root = target_node
                elif parent.left == target_node:
                    parent.left = target_node
                else:
                    parent.right = target_node

                if self.show_steps and self.auto_show_tree:
                    rprint(f"[yellow]After step {step_num}a:[/yellow]")
                    self.display_tree()

                # Second rotation: right on target node
                if self.show_steps and self.auto_show_tree:
                    rprint(
                        f"[yellow]Step {step_num}b: Right rotation on node {target_node.value}[/yellow]"
                    )
                balanced_node = self.tree.right_rotate(target_node)
            else:  # Left-Left case
                balanced_node = self.tree.right_rotate(target_node)

        elif balance < -1:  # Right heavy
            right_balance = self.tree.get_balance(target_node.right)
            if right_balance > 0:  # Right-Left case
                # First rotation: right on right child
                if self.show_steps and self.auto_show_tree:
                    rprint(
                        f"[yellow]Step {step_num}a: Right rotation on node {target_node.right.value}[/yellow]"
                    )
                target_node.right = self.tree.right_rotate(target_node.right)

                # Update parent reference after first rotation
                if parent is None:
                    self.tree.root = target_node
                elif parent.left == target_node:
                    parent.left = target_node
                else:
                    parent.right = target_node

                if self.show_steps and self.auto_show_tree:
                    rprint(f"[yellow]After step {step_num}a:[/yellow]")
                    self.display_tree()

                # Second rotation: left on target node
                if self.show_steps and self.auto_show_tree:
                    rprint(
                        f"[yellow]Step {step_num}b: Left rotation on node {target_node.value}[/yellow]"
                    )
                balanced_node = self.tree.left_rotate(target_node)
            else:  # Right-Right case
                balanced_node = self.tree.left_rotate(target_node)
        else:
            # No rotation needed
            balanced_node = target_node

        # Update the parent's reference or root with the final balanced node
        if parent is None:
            self.tree.root = balanced_node  # target_node was the root
        elif parent.left == target_node:
            parent.left = balanced_node
        else:
            parent.right = balanced_node

        # Show final state after this rotation sequence
        if self.show_steps and self.auto_show_tree:
            # Determine if this was a double rotation
            is_double_rotation = (
                balance > 1 and self.tree.get_balance(target_node.left) < 0
            ) or (balance < -1 and self.tree.get_balance(target_node.right) > 0)
            final_step = f"{step_num}b" if is_double_rotation else str(step_num)
            rprint(f"[yellow]After step {final_step}:[/yellow]")
            self.display_tree()

        return self.tree.root

    def _balance_node_and_update_root(self, target_node):
        """Balance a specific node and properly update the tree structure"""
        # We need to find the parent of the target node to update the reference
        parent = None
        current = self.tree.root

        # Find the parent of the target node
        while current and current != target_node:
            parent = current
            if target_node.value < current.value:
                current = current.left
            else:
                current = current.right

        # Balance the target node
        balanced_node = self._balance_node(target_node)

        # Update the parent's reference or root
        if parent is None:
            return balanced_node  # target_node was the root
        elif parent.left == target_node:
            parent.left = balanced_node
        else:
            parent.right = balanced_node

        return self.tree.root

    def _find_unbalanced_node(self, node):
        """Find the first unbalanced node in post-order traversal"""
        if not node:
            return None

        # Check children first (post-order)
        left_unbalanced = self._find_unbalanced_node(node.left)
        if left_unbalanced:
            return left_unbalanced

        right_unbalanced = self._find_unbalanced_node(node.right)
        if right_unbalanced:
            return right_unbalanced

        # Check current node
        balance = self.tree.get_balance(node)
        if abs(balance) > 1:
            return node

        return None

    def _get_all_unbalanced_nodes(self, node):
        """Get all unbalanced nodes in the tree"""
        unbalanced = []
        if not node:
            return unbalanced

        # Check current node
        balance = self.tree.get_balance(node)
        if abs(balance) > 1:
            unbalanced.append(node.value)

        # Check children
        unbalanced.extend(self._get_all_unbalanced_nodes(node.left))
        unbalanced.extend(self._get_all_unbalanced_nodes(node.right))

        return unbalanced

    def _get_node_color(self, node_value, unbalanced_nodes):
        """Determine the color for a node based on its status"""
        if node_value == self.recently_added:
            return "bright_green"  # Recently added node in bright green
        elif node_value in unbalanced_nodes:
            return "red"  # Unbalanced nodes in red
        else:
            return None  # Default color (no special coloring)

    def _balance_node(self, node):
        """Balance a specific node and return the new root"""
        if not node:
            return node

        balance = self.tree.get_balance(node)

        # Left heavy
        if balance > 1:
            if self.tree.get_balance(node.left) < 0:
                node.left = self.tree.left_rotate(node.left)
            return self.tree.right_rotate(node)

        # Right heavy
        if balance < -1:
            if self.tree.get_balance(node.right) > 0:
                node.right = self.tree.right_rotate(node.right)
            return self.tree.left_rotate(node)

        return node

    def _check_balance_and_guide(self):
        """Check if tree is balanced and provide warning in practice mode"""
        unbalanced_node = self._find_unbalanced_node(self.tree.root)
        if unbalanced_node:
            balance = self.tree.get_balance(unbalanced_node)
            rprint(
                f"[yellow]Tree is unbalanced! Node {unbalanced_node.value} has balance factor {balance}[/yellow]"
            )
            rprint(
                "[yellow]Use 'hint' command if you need guidance on how to balance it.[/yellow]"
            )
        else:
            rprint("[green]Tree is balanced![/green]")

    def _show_hint(self):
        """Show hints for balancing the tree"""
        unbalanced_node = self._find_unbalanced_node(self.tree.root)
        if not unbalanced_node:
            rprint("[green]Tree is already balanced! No hints needed.[/green]")
            return

        balance = self.tree.get_balance(unbalanced_node)
        rprint(
            f"[yellow]Hint for balancing node {unbalanced_node.value} (balance: {balance}):[/yellow]"
        )

        # Provide guidance on what rotation is needed
        if balance > 1:
            left_balance = self.tree.get_balance(unbalanced_node.left)
            if left_balance >= 0:
                rprint(
                    f"[yellow]→ Try 'rotate right {unbalanced_node.value}' (Left-Left case)[/yellow]"
                )
            else:
                rprint(
                    f"[yellow]→ First 'rotate left {unbalanced_node.left.value}', then 'rotate right {unbalanced_node.value}' (Left-Right case)[/yellow]"
                )
        else:
            right_balance = self.tree.get_balance(unbalanced_node.right)
            if right_balance <= 0:
                rprint(
                    f"[yellow]→ Try 'rotate left {unbalanced_node.value}' (Right-Right case)[/yellow]"
                )
            else:
                rprint(
                    f"[yellow]→ First 'rotate right {unbalanced_node.right.value}', then 'rotate left {unbalanced_node.value}' (Right-Left case)[/yellow]"
                )

    def _is_rotation_needed(self, value, direction):
        """Check if a rotation on the given node is the correct next step"""
        node = self.tree.search(value)
        if not node:
            return False

        # First, check if this node itself is unbalanced and needs the specified rotation
        balance = self.tree.get_balance(node)
        if abs(balance) > 1:
            # Check if the rotation direction is correct for this unbalanced node
            if balance > 1 and direction == "right":
                # Left-heavy, right rotation might be correct
                left_balance = self.tree.get_balance(node.left)
                return left_balance >= 0  # Simple right rotation
            elif balance < -1 and direction == "left":
                # Right-heavy, left rotation might be correct
                right_balance = self.tree.get_balance(node.right)
                return right_balance <= 0  # Simple left rotation

        # Second, check if this is the correct first step in a double rotation
        # We need to find an unbalanced ancestor that would need this rotation as part of its balancing
        unbalanced_ancestor = self._find_unbalanced_ancestor_needing_rotation(
            node, direction
        )
        return unbalanced_ancestor is not None

    def _find_unbalanced_ancestor_needing_rotation(self, node, direction):
        """Find an unbalanced ancestor that needs the given rotation on this node as first step"""
        # Search for an unbalanced ancestor
        current = self.tree.root

        while current:
            balance = self.tree.get_balance(current)
            if abs(balance) > 1:
                # Found an unbalanced node, check if it needs this rotation
                if balance > 1 and direction == "left" and current.left == node:
                    # Left-heavy ancestor, needs left rotation on left child (LR case)
                    left_balance = self.tree.get_balance(current.left)
                    return current if left_balance < 0 else None
                elif balance < -1 and direction == "right" and current.right == node:
                    # Right-heavy ancestor, needs right rotation on right child (RL case)
                    right_balance = self.tree.get_balance(current.right)
                    return current if right_balance > 0 else None

            # Continue searching down the tree towards the node
            if node.value < current.value:
                current = current.left
            elif node.value > current.value:
                current = current.right
            else:
                break

        return None

    def _show_status(self):
        """Show current configuration and tree status"""
        rprint("[bold]Current Configuration:[/bold]")
        rprint(f"  Mode: {self.mode.title()}")
        rprint(f"  Auto-show tree: {'On' if self.auto_show_tree else 'Off'}")
        rprint(f"  Show steps: {'On' if self.show_steps else 'Off'}")

        if self.tree.root:
            height = self._get_tree_height(self.tree.root)
            unbalanced = self._find_unbalanced_node(self.tree.root)
            rprint(f"\n[bold]Tree Status:[/bold]")
            rprint(f"  Height: {height}")
            rprint(f"  Balanced: {'No' if unbalanced else 'Yes'}")
            if unbalanced:
                balance = self.tree.get_balance(unbalanced)
                rprint(f"  Unbalanced node: {unbalanced.value} (balance: {balance})")
        else:
            rprint(f"\n[bold]Tree Status:[/bold] Empty")

    def _get_tree_height(self, node):
        """Calculate the height of the tree"""
        if not node:
            return 0
        return 1 + max(
            self._get_tree_height(node.left), self._get_tree_height(node.right)
        )

    def _print_fancy_grid(self, grid):
        """Print the grid in fancy tabulate/grid style"""
        if not grid:
            return

        # Create separator line
        separator = "+" + "+".join(["-" * 3 for _ in range(len(grid[0]))]) + "+"

        # Print top border
        rprint(f"[cyan]{separator}[/cyan]")

        # Print each row with borders
        for row in grid:
            row_str = "|" + "|".join([f"{cell:^3}" for cell in row]) + "|"
            rprint(f"[cyan]{row_str}[/cyan]")
            rprint(f"[cyan]{separator}[/cyan]")

    def _print_fancy_grid_colored(self, grid):
        """Print the grid in fancy tabulate/grid style with colors and connectors"""
        if not grid:
            return

        # Create separator line
        separator = "+" + "+".join(["-" * 3 for _ in range(len(grid[0]))]) + "+"

        # Print top border
        rprint(f"[cyan]{separator}[/cyan]")

        # Print each row with borders and colors
        for row in grid:
            colored_cells = []
            for cell in row:
                cell_value = cell["value"]
                cell_color = cell["color"]

                # Handle empty cells
                if cell_value == " ":
                    colored_cells.append("   ")
                elif cell_color:
                    colored_cells.append(
                        f"[{cell_color}]{cell_value:^3}[/{cell_color}]"
                    )
                else:
                    # Special formatting for connector characters
                    if cell_value in ["╩", "<", ">"]:
                        colored_cells.append(f"[dim white]{cell_value:^3}[/dim white]")
                    else:
                        colored_cells.append(f"{cell_value:^3}")

            row_str = (
                "[cyan]|[/cyan]"
                + "[cyan]|[/cyan]".join(colored_cells)
                + "[cyan]|[/cyan]"
            )
            rprint(row_str)
            rprint(f"[cyan]{separator}[/cyan]")

    def show_help(self):
        rprint("[bold]Commands:[/bold]")
        rprint("  a <value>             - Add a node")
        rprint("  d <value>             - Delete a node")
        rprint("  rl <value>            - Left rotation")
        rprint("  rr <value>            - Right rotation")
        rprint("  tree                  - Display current tree")
        rprint("  clear                 - Clear screen")
        rprint("  reset                 - Reset tree")
        rprint("  status                - Show configuration and tree status")
        rprint("  hint                  - Show balancing hints (practice mode)")
        rprint("  preorder              - Show preorder traversal")
        rprint("  inorder               - Show inorder traversal")
        rprint("  postorder             - Show postorder traversal")
        rprint("  help                  - Show this")
        rprint("  exit                  - Quit")
        rprint("\n[bold]Multiple Commands:[/bold]")
        rprint("  You can chain commands: 'a 10 a 20 d 10'")
        rprint("  Example: 'a 10 a 20 a 30 a 40 a 50' adds multiple nodes")
        rprint("\n[bold]Configuration:[/bold]")
        rprint("  config autoshow on/off    - Toggle auto-show tree")
        rprint("  config steps on/off       - Toggle show rotation steps")
        rprint("  config mode <mode>        - Set mode:")
        rprint("    • automatic  - Auto-balance")
        rprint("    • practice   - Guide learning (only allow correct rotations).")
        rprint("\n[bold]Visual Indicators:[/bold]")
        rprint("  [bright_green]Green nodes[/bright_green]  - Recently added")
        rprint("  [red]Red nodes[/red]    - Unbalanced (need rotation)")

    def _show_preorder(self):
        """Show preorder traversal of the tree"""
        if not self.tree.root:
            rprint("[yellow]Tree is empty[/yellow]")
            return

        traversal = []
        self._preorder_traversal(self.tree.root, traversal)
        rprint(f"[bold]Preorder traversal:[/bold] {' -> '.join(map(str, traversal))}")

    def _show_inorder(self):
        """Show inorder traversal of the tree"""
        if not self.tree.root:
            rprint("[yellow]Tree is empty[/yellow]")
            return

        traversal = []
        self._inorder_traversal(self.tree.root, traversal)
        rprint(f"[bold]Inorder traversal:[/bold] {' -> '.join(map(str, traversal))}")

    def _show_postorder(self):
        """Show postorder traversal of the tree"""
        if not self.tree.root:
            rprint("[yellow]Tree is empty[/yellow]")
            return

        traversal = []
        self._postorder_traversal(self.tree.root, traversal)
        rprint(f"[bold]Postorder traversal:[/bold] {' -> '.join(map(str, traversal))}")

    def _preorder_traversal(self, node, traversal):
        """Perform preorder traversal: root -> left -> right"""
        if node:
            traversal.append(node.value)
            self._preorder_traversal(node.left, traversal)
            self._preorder_traversal(node.right, traversal)

    def _inorder_traversal(self, node, traversal):
        """Perform inorder traversal: left -> root -> right"""
        if node:
            self._inorder_traversal(node.left, traversal)
            traversal.append(node.value)
            self._inorder_traversal(node.right, traversal)

    def _postorder_traversal(self, node, traversal):
        """Perform postorder traversal: left -> right -> root"""
        if node:
            self._postorder_traversal(node.left, traversal)
            self._postorder_traversal(node.right, traversal)
            traversal.append(node.value)


def main():
    cli = AVLTreeCLI()
    cli.run()


if __name__ == "__main__":
    main()
