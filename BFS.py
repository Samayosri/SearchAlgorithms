from queue import Queue

cols = 3
rows = 3
Parent={}
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def BFS(start: list):
    
    
    if start == goal:
        print("Reach Goal")
        return
    
    frontier = Queue()
    frontier.put(start)
    visited = set() 
    Parent[tuple(start)]=None
    while not frontier.empty():
        v = frontier.get()
        visited.add(tuple(v))
        if v == goal:
            print("Reach Goal")
            return
        
        for neighbour in getNeighbours(v):
            t = tuple(neighbour)
            if t not in visited:
                Parent[t]=v
                frontier.put(neighbour)
    
    print("No solution found !!!!!!!!!!!!!!!!")


def valid(i, j):
    return i >= 0 and i < rows and j >= 0 and j < cols


def getNeighbours(v: list):
    indexOfZero = v.index(0)
    i = indexOfZero // cols
    j = indexOfZero % cols
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


start = [1, 2, 5, 3, 4, 0, 6, 7, 8]
BFS(start)
printPath(Parent,goal)
