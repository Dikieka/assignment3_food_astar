import heapq
import time

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(pos, grid):
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dx, dy in dirs:
        x, y = pos[0]+dx, pos[1]+dy
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != "#":
            neighbors.append((x, y))
    return neighbors

def a_star(grid, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g = {start: 0}
    f = {start: manhattan(start, goal)}
    visited = set()
    node_count = 1 

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct(came_from, start, goal), node_count

        visited.add(current)

        for neighbor in get_neighbors(current, grid):
            temp_g = g[current] + 1
            if neighbor not in g or temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + manhattan(neighbor, goal)
                if neighbor not in visited:
                    heapq.heappush(open_set, (f[neighbor], neighbor))
                    node_count += 1  
    return None, node_count

def reconstruct(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path

def print_grid(grid, path):
    grid_copy = [row[:] for row in grid]
    for x, y in path:
        if grid_copy[x][y] not in "RC":
            grid_copy[x][y] = "*"
    for row in grid_copy:
        print("".join(row))

def run_assignment3():
    grid = [
        list("R...#"),
        list("..#.."),
        list("..#.."),
        list("....."),
        list("..C..")
    ]
    start = find(grid, "R")
    goal = find(grid, "C")

    start_time = time.time()

    path, node_count = a_star(grid, start, goal)
    
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000

    print("\nAssignment 3 - A* Path (Food Delivery):")
    if path:
        print_grid(grid, path)
    else:
        print("No path found.")
    
    print(f"Execution Time: {execution_time:.4f} ms")
    print(f"Nodes Explored: {node_count}")

def find(grid, symbol):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == symbol:
                return (i, j)