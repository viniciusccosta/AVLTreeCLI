# AVL Tree Practice Tool

A terminal-based interactive learning tool to practice AVL tree insertions, deletions, and rotations. This CLI (Command Line Interface) allows you to explore self-balancing binary search trees with visual feedback and two learning modes: `automatic` and `practice`.

## Features

- 📈 **AVL Tree Visualization**: Displays the tree in a clear grid layout.
- 🤖 **Automatic Mode**: Automatically balances the tree after insertions/deletions.
- 🧠 **Practice Mode**: Learn AVL balancing by manually applying the correct rotations.
- 🔄 **Undo/Redo Support**: Revert and replay actions easily.
- 📚 **Step-by-Step Guidance**: See every rotation explained and shown.
- 🎨 **Color-Coded Display**:
  - `bright_green` for recently added nodes
  - `red` for unbalanced nodes

## Installation

```bash
git clone https://github.com/your-username/avl-tree-practice.git
cd avl-tree-practice
pip install -r requirements.txt
```

Make sure you have Python 3.13 installed.

## Usage

```bash
python -m avltrecli.cli
```

## Commands

| Command                    | Description                                |
|---------------------------|--------------------------------------------|
| `add <value>` / `a`       | Add a node                                 |
| `remove <value>` / `r`    | Remove a node                              |
| `rotate left <value>`     | Apply left rotation                        |
| `rotate right <value>`    | Apply right rotation                       |
| `rl <value>`              | Left rotation (shortcut)                   |
| `rr <value>`              | Right rotation (shortcut)                  |
| `tree`                    | Display current AVL tree                   |
| `reset`                   | Clear the tree and command history         |
| `undo`                    | Undo last action                           |
| `redo`                    | Redo previously undone action              |
| `status`                  | Show current configuration and tree stats  |
| `hint`                    | Show hints for how to balance the tree     |
| `clear`                   | Clear screen and show current state        |
| `help`                    | Display help information                   |
| `exit`                    | Exit the program                           |

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
> add 30
Added 30 to the tree
> add 20
Added 20 to the tree
> add 10
Tree is unbalanced! Node 30 has balance factor 2
Step 1: Balancing node 30 (balance: 2)
→ Performing right rotation on node 30
Tree is now balanced!
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
