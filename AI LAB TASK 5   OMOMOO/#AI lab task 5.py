#AI lab task 5 
def dfs(graph, start):
    visited = set()      # visited nodes track karega
    stack = [start]      # stack mein start node daal do

    while stack:
        node = stack.pop()   # last element nikaalo

        if node not in visited:
            print(node, end=" ")
            visited.add(node)

            # neighbours ko stack mein daalo
            # reverse isliye taake order correct aaye
            for neighbour in reversed(graph[node]):
                stack.append(neighbour)


# Graph
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': [],
    'E': []
}

dfs(graph, 'A')

#2 
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# Preorder Traversal (Root → Left → Right)
def preorder(root):
    if root:
        print(root.data, end=" ")
        preorder(root.left)
        preorder(root.right)


# Inorder Traversal (Left → Root → Right)
def inorder(root):
    if root:
        inorder(root.left)
        print(root.data, end=" ")
        inorder(root.right)


# Postorder Traversal (Left → Right → Root)
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.data, end=" ")


# Creating Binary Tree
root = Node("A")
root.left = Node("B")
root.right = Node("C")
root.left.left = Node("D")
root.left.right = Node("E")
root.right.right = Node("F")

print("Preorder:")
preorder(root)

print("\nInorder:")
inorder(root)

print("\nPostorder:")
postorder(root)