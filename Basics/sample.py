import sys
sys.setrecursionlimit(10**6)
class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = {}
        self.subtree_size = 1
def update_ancestors(node, delta):
    while node:
        node.subtree_size += delta
        node = node.parent
def find_node(root, path):
    parts = path.strip().split('/')
    current = root
    if not parts or parts[0] != root.name:
        return None
    for part in parts[1:]:
        if part not in current.children:
            return None
        current = current.children[part]
    return current
def clone_node(node):
    new_node = Node(node.name)
    for child in node.children.values():
        child_clone = clone_node(child)
        child_clone.parent = new_node
        new_node.children[child_clone.name] = child_clone
        new_node.subtree_size += child_clone.subtree_size
    return new_node
def is_ancestor(ancestor, node):
    cur = node
    while cur:
        if cur == ancestor:
            return True
        cur = cur.parent
    return False
def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    n, q = map(int, input_data[0].split())
    first_line_tokens = input_data[1].split()
    root_name = first_line_tokens[0]
    root = Node(root_name)
    global_total_nodes = 1
    for i in range(1, n + 1):
        tokens = input_data[i].split()
        parent_path = tokens[0]
        parent_node = find_node(root, parent_path)
        if parent_node is None:
            continue
        for child_name in tokens[1:]:
            if child_name in parent_node.children:
                continue
            child = Node(child_name)
            child.parent = parent_node
            parent_node.children[child_name] = child
            update_ancestors(parent_node, 1)
            global_total_nodes += 1
    out_lines = []
    for i in range(n + 1, n + q + 1):
        if not input_data[i]:
            continue
        tokens = input_data[i].split()
        command = tokens[0]
        if command == "countDescendants":
            path = tokens[1]
            node = find_node(root, path)
            if node is None:
                out_lines.append("Invalid command")
            else:
                out_lines.append(str(node.subtree_size - 1))
        elif command in ("cutPaste", "copyPaste"):
            src_path = tokens[1]
            dest_path = tokens[2]
            src_node = find_node(root, src_path)
            dest_node = find_node(root, dest_path)
            if src_node is None or dest_node is None:
                out_lines.append("Invalid command")
                continue
            if src_node == dest_node:
                out_lines.append("Invalid command")
                continue
            if src_node.name in dest_node.children:
                out_lines.append("Invalid command")
                continue
            if is_ancestor(src_node, dest_node):
                out_lines.append("Invalid command")
                continue
            if command == "cutPaste":
                if src_node.parent is None:
                    out_lines.append("Invalid command")
                    continue
                subtree_size = src_node.subtree_size
                old_parent = src_node.parent
                del old_parent.children[src_node.name]
                update_ancestors(old_parent, -subtree_size)
                src_node.parent = dest_node
                dest_node.children[src_node.name] = src_node
                update_ancestors(dest_node, subtree_size)
                out_lines.append("OK")
            elif command == "copyPaste":
                clone = clone_node(src_node)
                if global_total_nodes + clone.subtree_size > 10**6:
                    out_lines.append("Invalid command")
                    continue
                clone.parent = dest_node
                dest_node.children[clone.name] = clone
                update_ancestors(dest_node, clone.subtree_size)
                global_total_nodes += clone.subtree_size
                out_lines.append("OK")
        else:
            out_lines.append("Invalid command")
    sys.stdout.write("\n".join(out_lines))

if __name__ == '__main__':
    main()
