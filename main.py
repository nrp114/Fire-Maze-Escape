import random
import time
import copy
import numpy as np
from heapq import heapify, heappush, heappop


class node:
    def __init__(self, coor, parent):
        self.coor = coor
        self.parent = parent

class a_node:
    def __init__(self,time, coor, parent, aval, hval):
        self.coord = coor
        self.parent = parent
        self.aval = aval
        self.hval = hval
        self.time = time

    def __lt__(self, other):
        return self.hval < other.hval

    def __str__(self):
        return "Coordinate: {}, Actual: {}, HVal: {}".format(self.coord, self.aval, self.hval)



def create_grid(dim, p):
    grid = []
    for i in range(dim):
        col = []
        for j in range(dim):
            num = random.random()
            if num <= p:
                col.append(1)
            else:
                col.append(0)
        grid.append(col)
    grid[0][0] = 0
    grid[-1][-1] = 0
    return grid


def create_fire_grid(dim, p, check):
    grid = []
    for i in range(dim):
        col = []
        for j in range(dim):
            num = random.random()
            num2 = random.random()
            if num <= p:
                col.append(1)
            else:
                col.append(0)
        grid.append(col)
    if check:
        x = random.randint(0, dim - 1)
        y = random.randint(0, dim - 1)
        grid[x][y] = 4
    grid[0][0] = 0
    grid[-1][-1] = 0
    return grid


def h_value(coordinate, dimension):
    row = coordinate[0]
    col = coordinate[1]
    fin_row = dimension - 1
    fin_col = dimension - 1
    x = abs(fin_row - row)
    y = abs(fin_col - col)
    return np.sqrt(x * x + y * y)


def find(heap, coord):
    count = 0
    for obj in heap:
        if obj.coord == coord:
            return count
        count += 1
    return -1


def a_star(grid, dim, visited,start_node,end_node):
    closed = []
    heap = []
    heapify(heap)
    first_anode = a_node(0, start_node, None, 0, h_value(start_node, dim))
    heappush(heap, first_anode)
    time_counter = 0
    while len(heap) != 0:
        curr_node = heappop(heap)
        #print(curr_node)
        [row, col] = curr_node.coord
        if [row,col] == end_node:
            while curr_node != None:
                grid[curr_node.coord[0]][curr_node.coord[1]] = 2
                curr_node = curr_node.parent
            return True
        dir = [[0, 1], [1, 0], [-1, 0], [0, -1]]
        for direction in dir:
            x = row + direction[0]
            y = col + direction[1]
            if x < 0 or x >= dim or y < 0 or y >= dim or grid[x][y] == 1 or [x, y] in closed or grid[x][y] == 4:
                continue
            time_counter += 1
            if visited[x][y]:
                #print("Here")
                idx = find(heap, [x, y])
                if idx != -1 and heap[idx].aval > curr_node.aval+1:
                    #print("Here123")
                    heap[idx].aval = curr_node.aval+1
                    heap[idx].parent = curr_node
                    heap[idx].hval = h_value([x, y], dim) + curr_node.aval + 1
                    heap[idx].time = time_counter
                continue
            new_node = a_node(time_counter, [x, y], curr_node, curr_node.aval + 1, h_value([x, y], dim) + curr_node.aval + 1)
            heappush(heap, new_node)
            visited[x][y] = True
        visited[row][col] = True
        closed.append([row, col])
        heapify(heap)
    return False


def bfs(grid, dim, visited):
    queue = []
    n1 = node([0, 0], None)
    queue.append(n1)
    while len(queue) != 0:
        coord = queue.pop(0)
        [row, col] = coord.coor
        if row == dim - 1 and col == dim - 1:
            grid[row][col] = 2
            par = coord.parent
            while par is not None:
                tmp = par.coor
                grid[tmp[0]][tmp[1]] = 2
                par = par.parent
            return True
        dir = [[0, 1], [1, 0], [-1, 0], [0, -1]]
        for direction in dir:
            x = row + direction[0]
            y = col + direction[1]
            if x < 0 or x >= dim or y < 0 or y >= dim or visited[x][y] is True or grid[x][y] == 1:
                continue
            new_node = node([x, y], coord)
            queue.append(new_node)
            visited[x][y] = True
        visited[row][col] = True
    return False


def dfs(grid, dim, visited):
    stack = []
    stack.append([0, 0])
    while len(stack) != 0:
        x_curr,y_curr = stack[-1]
        if x_curr == dim - 1 and y_curr == dim - 1:
            visited[x_curr][y_curr] = True
            grid[x_curr][y_curr] = 2
            return grid, True
        else:
            visited[x_curr][y_curr] = True
            grid[x_curr][y_curr] = 2
            dirr = [[-1, 0], [0, -1],[0, 1], [1, 0]]
            check =0
            for direction in dirr:
                x = x_curr + direction[0]
                y = y_curr + direction[1]
                if x < 0 or x >= dim or y < 0 or y >= dim or visited[x][y] is True or grid[x][y] == 1 or grid[x][y] == 2:
                    continue
                stack.append([x,y])
                check += 1
            if check == 0:
                stack.pop()
                grid[x_curr][y_curr] = 0
    return grid, False


def dfs1(grid, dim):
    stack = []
    stack.append([0, 0])
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    while len(stack) != 0:
        current_state = stack[-1]
        x_coor = current_state[0]
        y_coor = current_state[1]
        check = 0
        for direction in dirr:
            x = x_coor + direction[0]
            y = y_coor + direction[1]
            if x < 0 or x >= dim or y < 0 or y >= dim or grid[x][y] == 1 or grid[x][y] == -1:
                check += 1
                continue
            stack.append([x, y])
        if check == 4:
            grid[x_coor][y_coor] = 0
            stack.pop()
        grid[x_coor][y_coor] = -1
    print(grid)


def strategy1(astar_grid,dim, grid,q):
    i=0
    j=0
    grid[i][j] = 2
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    while i != dim-1 and j!= dim -1:
        for direction in dirr:
            x = i + direction[0]
            y = j + direction[1]
            if x >= 0 and x < dim and y >= 0 and y < dim and astar_grid[x][y] == 2:
                grid = fire_spread(grid,dim,q)
                if grid[x][y] == 4:
                    # if on fire
                    print("Player burned")
                    return grid,True
                grid[x][y] = 2
                i = x
                j =y
                break
        yield grid,False
    return grid,True


def strategy2(astar_grid,dim, grid,q):
    i = 0
    j = 0
    grid[i][j] = 2
    # visited_copy = copy.deepcopy(visited)
    # astar_grid = copy.deepcopy(astar_grid)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    while i != dim - 1 and j != dim - 1:
        print()
        printLine(grid)
        print("--")
        visited = create_visited(dim)
        astar_check = a_star(astar_grid,dim,visited,[i,j],[dim-1,dim-1])
        if astar_check:
            for direction in dirr:
                x = i + direction[0]
                y = j + direction[1]
                if x >= 0 and x < dim and y >= 0 and y < dim and astar_grid[x][y] == 2:
                    grid[i][j] = 2
                    i = x
                    j = y
                    grid = fire_spread(grid,dim,q)
                    astar_grid = copy.deepcopy(grid)
                    break
        else:
            return False
    grid[x][y] = 2
    grid[-1][-1] = 2
    return True


def create_visited(dim):
    visited = []
    for i in range(dim):
        col = []
        for j in range(dim):
            col.append(False)
        visited.append(col)
    return visited


def printLine(printG):
    for i in range(len(printG)):
        print(printG[i])


def fire_spread(grid,dim,q):
    grid_copy = copy.deepcopy(grid)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    for i in range(dim):
        for j in range(dim):
            if grid[i][j] != 4 and grid[i][j] != 1:
                neighbour_fire_count = 0
                for direction in dirr:
                    x = i + direction[0]
                    y = j + direction[1]
                    if x >= 0 and x < dim and y >= 0 and y < dim and grid[x][y] == 4:
                        neighbour_fire_count +=1
                prob = 1-((1-q)**neighbour_fire_count)
                if random.random() <= prob:
                    grid_copy[i][j] = 4
    return grid_copy


if __name__ == '__main__':
    dim = int(input("Enter dimension of grid: "))
    if dim <= 0:
        print("Enter a positive value for dimension")
        exit(-1)
    prob = float(input("Enter probability: "))
    if prob > 1 or prob < 0:
        print("Enter a value between 0 and 1 for probability")
        exit(-1)
    grid = create_grid(dim, prob)

    visited = create_visited(dim)
    #printLine(grid)
    #printLine(grid)
    #a_star(grid, dim, visited)
    #printLine(grid)
    #exit(0)
    q = 0.1
    printLine(grid)
    print("-----------------")
    # a_star(a_star_grid,dim,visited,[0,0],[dim-1,dim-1])
    # exit(0)
    grid = create_fire_grid(dim,0.1,True)
    printLine(grid)
    print("-----------------")
    a_star_grid = copy.deepcopy(grid)
    strategy2(a_star_grid,dim,grid,q)
    printLine(grid)

    #start = time.time()
    #var1, var2 = (dfs(grid, dim, visited))
    #print(var2)
    #print(time.time() - start)
    # printLine(grid)
    # printLine(variable)
