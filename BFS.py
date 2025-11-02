from queue import Queue
import time
cols = 3
rows = 3
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def BFS(start: list):
    Parent={}
    expanded=0
    search_depth=0
    g_n=[]
    if start == goal:

        print("Reach Goal")
        return Parent,expanded,0,0
    
    frontier = Queue()
    frontier.put(start)
    visited = set() 
    g_n = {tuple(start): 0} 
    Parent[tuple(start)]=None
    visited.add(tuple(start))
    while not frontier.empty():
        v = frontier.get()
        search_depth=max(search_depth,g_n[tuple(v)])
        expanded+=1
        if v == goal:
            print("Reach Goal")
            return Parent,expanded,g_n[tuple(v)],search_depth
       
        
        for neighbour in getNeighbours(v):
            t = tuple(neighbour)
            if t not in visited:
                g_n[t]=g_n[tuple(v)]+1 
                Parent[t]=v
                frontier.put(neighbour)
                visited.add(t)
    
    print("No solution found !!!!!!!!!!!!!!!!")


def valid(i, j):
    return i >= 0 and i < rows and j >= 0 and j < cols


def getNeighbours(v: list):
    indexOfZero = v.index(0)
    i, j = divmod(indexOfZero, cols)
    neighbours = []
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    for k in range(4):
        new_i = i + dx[k]
        new_j = j + dy[k]
        
        if valid(new_i, new_j):
            new_index = new_i * cols + new_j
            new_state = v.copy()
            new_state[indexOfZero], new_state[new_index] = new_state[new_index], new_state[indexOfZero]
            neighbours.append(new_state)
    
    return neighbours

def printPath(Parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = Parent[tuple(goal)]
    path.reverse()

    print("\nPath to goal ({} moves):".format(len(path)-1))
    for state in path:
        printPuzzle(state)
        print("-----")


def printPuzzle(state):
    for i in range(rows):
        print(state[i*cols:(i+1)*cols])

def is_solvable(puzzle):
    inv_count = 0
    arr = [x for x in puzzle if x != 0]  # ignore the blank
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count % 2 == 0


# start = [8, 1, 2, 0, 4, 3, 7, 6, 5]
# start = [1, 2, 5, 3, 4, 0, 6, 7, 8]
start = [1, 0, 2 ,7, 5, 4, 8, 6, 3]
# start = [1, 2, 3 ,4, 5, 6, 8, 7, 0]
# start = [6, 4, 7 ,8, 5, 0, 3, 2, 1]
# start = [8, 6, 7 ,2, 5, 4, 3, 0, 1]

start_time = time.time()
if is_solvable(start):
    Parent, expanded, cost_path, search_depth = BFS(start)
    printPath(Parent, goal)
    print(f"Cost of path: {cost_path}, Nodes expanded: {expanded}, Search depth: {search_depth}")
else:
    print("This puzzle is unsolvable!")

end_time = time.time()  
print(f"Execution time: {end_time - start_time:.4f} seconds")