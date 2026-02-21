#AI LAB TASK 6 
#1️ BFS Without Queue
def bfs_without_queue(graph, start):
    visited = []
    queue = [start]   # simple list as queue

    while queue:
        node = queue.pop(0)   # remove first element

        if node not in visited:
            print(node, end=" ")
            visited.append(node)

            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)


# Graph Example
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

bfs_without_queue(graph, 'A')

#2️ BFS With Queue
from collections import deque

def bfs_with_queue(graph, start):
    visited = set()
    queue = deque([start])   # real queue

    while queue:
        node = queue.popleft()   # remove from front

        if node not in visited:
            print(node, end=" ")
            visited.add(node)

            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)


# Same Graph
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

bfs_with_queue(graph, 'A')