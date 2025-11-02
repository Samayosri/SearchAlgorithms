def IDFS(arr):
    depth = 0
    global total_expanded
    total_expanded = 0
    while True:
        
        result = DFS(arr, depth, [tuple(arr)])
        if result:
            return result
        depth += 1


def DFS(node, depth, path):
    global total_expanded
    if Isgoal(node):
        return path
    
    if depth == 0:
        return None
    
    total_expanded += 1  
    for neighbour in getneighbours(node):
        neighbour_key = tuple(neighbour)
        if neighbour_key not in path:
            result = DFS(neighbour, depth - 1, path + [neighbour_key])
            if result:
                return result
    
    return None


def getneighbours(arr):
    neighbours = []
    arr_list = list(arr) if isinstance(arr, tuple) else arr
    index = arr_list.index(0)
    i, j = divmod(index, 3)

    if i - 1 >= 0:  # up
        a = arr_list.copy()
        ni = (i - 1) * 3 + j
        a[index], a[ni] = a[ni], a[index]
        neighbours.append(a)
    if i + 1 <= 2:  # down
        a = arr_list.copy()
        ni = (i + 1) * 3 + j
        a[index], a[ni] = a[ni], a[index]
        neighbours.append(a)
    if j - 1 >= 0:  # left
        a = arr_list.copy()
        nj = i * 3 + (j - 1)
        a[index], a[nj] = a[nj], a[index]
        neighbours.append(a)
    if j + 1 <= 2:  # right
        a = arr_list.copy()
        nj = i * 3 + (j + 1)
        a[index], a[nj] = a[nj], a[index]
        neighbours.append(a)
    return neighbours


def Isgoal(arr):
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    arr_list = list(arr) if isinstance(arr, tuple) else arr
    return arr_list == goal


def print_path(path):
    print(f"\n✓ Solution found in {len(path) - 1} moves!")
    print("\nPath from start to goal:")
    for step, state in enumerate(path):
        print(f"\nStep {step}:")
        state_list = list(state)
        for i in range(0, 9, 3):
            print(state_list[i:i+3])


def checkinstances(arr):
    # Exclude 0 from inversion count
    filtered = [x for x in arr if x != 0]
    num = 0
    for i in range(len(filtered)):
        for j in range(i+1, len(filtered)):
            if filtered[i] > filtered[j]:
                num += 1
    return num % 2 == 0


# Test
arr = [1, 0, 2,
       7, 5, 4,
       8, 6, 3]

print("Starting state:")
for i in range(0, 9, 3):
    print(arr[i:i+3])

if checkinstances(arr):
    result = IDFS(arr)
    if result:
        print("\nGoal found!")
        print_path(result)
        print(f"\nTotal nodes expanded: {total_expanded}")
    else:
        print("No solution found.")
else:
    print("No solution exists for this configuration.")