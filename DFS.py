import copy

def DfS(arr):
    stack = [(arr, 0)]
    visited = {tuple(arr)} 
    parent = {}
    expanded = 0
    max_search_depth = 0
    
    while stack:
        node, depth = stack.pop()
        key = tuple(node)
        expanded += 1
        max_search_depth = max(max_search_depth, depth)
        
        if Isgoal(node):
            return node, parent, expanded, max_search_depth
        
        for neighbour in getneighbours(node):
            nkey = tuple(neighbour)
            if nkey not in visited:
                visited.add(nkey)
                parent[nkey] = key
                new_depth = depth + 1
                max_search_depth = max(max_search_depth, new_depth)  # FIX: Track depth when adding
                stack.append((neighbour, new_depth))
                
    return None, None, expanded, max_search_depth


def calculate_solution_depth(goal, parent):
    """Calculate the number of moves in the solution path"""
    depth = 0
    key = tuple(goal)
    while key in parent:
        depth += 1
        key = parent[key]
    return depth


def getneighbours(arr):
    neighbours = []
    index = arr.index(0)
    i, j = divmod(index, 3)

    if i - 1 >= 0:  # up
        a = arr.copy()
        ni = (i - 1) * 3 + j
        a[index], a[ni] = a[ni], a[index]
        neighbours.append(a)
    if i + 1 <= 2:  # down
        a = arr.copy()
        ni = (i + 1) * 3 + j
        a[index], a[ni] = a[ni], a[index]
        neighbours.append(a)
    if j - 1 >= 0:  # left
        a = arr.copy()
        nj = i * 3 + (j - 1)
        a[index], a[nj] = a[nj], a[index]
        neighbours.append(a)
    if j + 1 <= 2:  # right
        a = arr.copy()
        nj = i * 3 + (j + 1)
        a[index], a[nj] = a[nj], a[index]
        neighbours.append(a)
    return neighbours


def Isgoal(arr):
    goal = [0, 1, 2,
            3, 4, 5,
            6, 7, 8]
    return arr == goal


def print_path(goal, parent):
    path = []
    key = tuple(goal)
    while key in parent:
        path.append(list(key))
        key = parent[key]
    path.append(list(key))  # start
    path.reverse()

    print("\nPath from start to goal:")
    for step, state in enumerate(path):
        print(f"\nStep {step}:")
        for i in range(0, 9, 3):
            print(state[i:i+3])


# --- MAIN ---
arr = [1, 2, 5,
       3, 4, 0,
       6, 7, 8]

def checkinstances(arr):
    # Exclude 0 from inversion count
    filtered = [x for x in arr if x != 0]
    num = 0
    for i in range(len(filtered)):
        for j in range(i+1, len(filtered)):
            if filtered[i] > filtered[j]:
                num += 1
    return num % 2 == 0


if checkinstances(arr):
    result = DfS(arr)
    goal, parent, expanded, max_depth = result
    
    if goal:
        solution_depth = calculate_solution_depth(goal, parent)
        print("Goal found!")
        print(f"\nStatistics:")
        print(f"  Solution depth (moves): {solution_depth}")
        print_path(goal, parent)
        print(f"  Max search depth: {max_depth}")
        print(f"  Expanded nodes: {expanded}")
    else:
        print("No solution found.")
        print(f"Expanded nodes: {expanded}")
        print(f"Max search depth: {max_depth}")
else:
    print("No solution exists (puzzle has odd number of inversions).")