import math
import heapq
import time
cols = 3
rows = 3
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def A_Star(start,heuristic):
    Parent={}
    expanded=0
    search_depth=0
    if start == goal:
        print("Reach Goal")
        return Parent,expanded,0,0
    frontier = [] # {F(State):Statue}
    visited = set() # Keep visited state
    g_n=[] # {State : G(State)}
    heapq.heappush(frontier, (0, start))
    Parent[tuple(start)]=None
    g_n = {tuple(start): 0} # G(n) for the start is 0 
    while frontier :
        f, v = heapq.heappop(frontier) # POP the Min F(n)
        visited.add(tuple(v)) # Add this State to visited list
        expanded+=1
        search_depth=max(search_depth,g_n[tuple(v)])
        if v==goal:  # Check if this the goal
            print("reach goal")
            return Parent,expanded,g_n[tuple(v)],search_depth
        for neighbour in getNeighbours(v): # Go through neighbours of Currnt State . 
            t=tuple(neighbour)
            if t not in visited:         
                g_neighbour=g_n[tuple(v)]+1   # G(neighbour) is the G(parent)+1
                if t not in g_n or g_n[t]>g_neighbour: # Add this check to prevent unneccassary states in heap        
                   h_neighbour=heuristic(neighbour,goal)   
                   f=h_neighbour+g_neighbour
                   Parent[t]=v
                   heapq.heappush(frontier, (f, neighbour))
                   g_n[t]=g_neighbour
    print ("No Solution Found !!!!!!!!!!!!! ")

def manhattan_distance(current, goal):
    h=0
    for i, tile in enumerate(current):
        if tile != 0: 
            goal_idx = goal.index(tile)
            current_x, current_y = divmod(i, cols)
            goal_x, goal_y = divmod(goal_idx, cols)
            h += abs(current_x - goal_x) + abs(current_y - goal_y)
    return h


def euclidean_distance(current, goal):
    h=0
    for i, tile in enumerate(current):
        if tile != 0: 
            goal_idx = goal.index(tile)
            current_x, current_y = divmod(i, cols)
            goal_x, goal_y = divmod(goal_idx, cols)
            h += math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2)

    return h

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
    # If number of Inversions is odd -> unsolvable
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
    parent_manhattan, expanded_manhattan,cost_path,search_depth = A_Star(start, manhattan_distance)
    printPath(parent_manhattan, goal)
    print(f"cost of path : {cost_path} , nodes expanded = {expanded_manhattan} ,search depth = {search_depth}")

  #  parent_euclidean, expanded_euclidean = A_Star(start, euclidean_distance)
   
else:
    print("This puzzle is unsolvable!")
end_time = time.time()  
print(f"Execution time: {end_time - start_time:.4f} seconds")
