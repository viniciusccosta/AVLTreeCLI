# AVL Tree Practice Tool

A terminal-based interactive learning tool to practice AVL tree insertions, deletions, and rotations. This CLI (Command Line Interface) allows you to explore self-balancing binary search trees with visual feedback and two learning modes: `automatic` and `practice`.

## Features

- 📈 **AVL Tree Visualization**: Displays the tree in a clear grid layout with connectors.
- 🤖 **Automatic Mode**: Automatically balances the tree after insertions/deletions.
- 🧠 **Practice Mode**: Learn AVL balancing by manually applying the correct rotations.
- 📚 **Step-by-Step Guidance**: See every rotation explained and shown.
- ⚡ **Multiple Commands**: Chain multiple commands in a single line (e.g., `a 10 a 20 a 30`).
- 🔄 **Tree Traversals**: View preorder, inorder, and postorder traversals.
- 🎨 **Color-Coded Display**:
  - `bright_green` for recently added nodes
  - `red` for unbalanced nodes

## Installation

```bash
pipx install avltreecli
```

Make sure you have Python 3.13 installed.

## Usage

```bash
avltreecli
```

## Commands

| Command                   | Description                                |
|---------------------------|--------------------------------------------|
| `a <value>`               | Add a node (values: -99 to 999)            |
| `d <value>`               | Remove a node                              |
| `rl <value>`              | Left rotation (shortcut)                   |
| `rr <value>`              | Right rotation (shortcut)                  |
| `tree`                    | Display current AVL tree                   |
| `reset`                   | Clear the tree                             |
| `status`                  | Show current configuration and tree stats  |
| `hint`                    | Show hints for how to balance the tree     |
| `preorder`                | Show preorder traversal                    |
| `inorder`                 | Show inorder traversal                     |
| `postorder`               | Show postorder traversal                   |
| `clear`                   | Clear screen and show current state        |
| `help`                    | Display help information                   |
| `exit`                    | Exit the program                           |

## Multiple Commands

You can chain multiple commands in a single line for faster operations:

```bash
# Add multiple nodes at once
> a 10 a 20 a 30 a 40 a 50

# Mix operations
> a 15 a 25 d 20 a 35

# Quick tree building
> a 50 a 30 a 70 a 20 a 40 a 60 a 80
```

## Configuration

You can change runtime settings with:

```bash
config <setting> <value>
```

Available settings:

| Setting         | Values                | Description                                  |
|----------------|------------------------|----------------------------------------------|
| `autoshow`     | `on` / `off`           | Automatically display tree after actions     |
| `steps`        | `on` / `off`           | Show step-by-step balancing actions          |
| `mode`         | `automatic` / `practice` | Switch between learning and auto-balance     |

## Modes

- 🟢 **Automatic Mode** (default):  
  The AVL tree balances itself automatically after every operation. Rotate commands are disabled.

- 🟡 **Practice Mode**:  
  Balance the tree manually with guided hints and validation. Only correct rotations are allowed.

## Example Session

```bash
# Basic operations
> a 30
Added 30 to the tree

> a 20
Added 20 to the tree

> a 10
Tree is unbalanced! Node 30 has balance factor 2
Step 1: Balancing node 30 (balance: 2)
→ Performing right rotation on node 30
Tree is now balanced!

# Multiple commands in one line
> a 40 a 50 a 60
Added 40 to the tree
Added 50 to the tree
Tree is unbalanced! Node 40 has balance factor -2
Step 1: Balancing node 40 (balance: -2)
→ Performing left rotation on node 40
Added 60 to the tree

# View tree structure
> tree
+---+---+---+---+---+---+---+
|   |   |   | 30|   |   |   |
+---+---+---+---+---+---+---+
|   | 20| < | ╩ | > | 50|   |
+---+---+---+---+---+---+---+
| 10|   |   |   | 40| ╩ | 60|
+---+---+---+---+---+---+---+

# Check traversals
> inorder
Inorder traversal: 10 -> 20 -> 30 -> 40 -> 50 -> 60
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
