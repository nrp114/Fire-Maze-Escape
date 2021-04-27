import turtle
from time import sleep

import solve_maze
import copy
import random
# from freegames import line

turtle.register_shape("warrior1.gif")

class wPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(20)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("warrior1.gif")
        self.color("red")
        self.penup()
        self.speed(20)
    def go_to(self,x,y):
        screen_x = -288 + (y * 24)
        screen_y = 288 - (x * 24)
        self.goto(screen_x,screen_y)


class bPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(20)


class lbPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("navy")
        self.penup()
        self.speed(20)


class oePen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("orange")
        self.penup()
        self.speed(20)


class pPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(20)


class fPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(20)


def write_maze(x, y, pen):
    screen_x = -288 + (y * 24)
    screen_y = 288 - (x * 24)
    pen.goto(screen_x, screen_y)
    pen.stamp()


def strategy1(astar_grid, dim, grid, q):
    i = 0
    j = 0
    grid[i][j] = 2
    write_maze(i, j, bpen)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    reach = False
    while not reach:
        for direction in dirr:
            x = i + direction[0]
            y = j + direction[1]
            if x == dim - 1 and y == dim - 1:
                reach = True
                continue
            if 0 <= x < dim and 0 <= y < dim and astar_grid[x][y] == 2:
                grid = fire_spread(grid, dim, q)
                if grid[x][y] == 4:
                    print("Player burned")
                    write_maze(x, y, oepen)
                    return grid
                grid[x][y] = 2
                write_maze(x, y, bpen)
                i = x
                j = y
                break
    print("We are here!")
    grid[dim - 1][dim - 1] = 2
    write_maze(dim - 1, dim - 1, bpen)
    return grid


def strategy2(astar_grid, dim, grid, q):
    # print("In 2")
    i = 0
    j = 0
    grid[i][j] = 2
    write_maze(i, j, bpen)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    reach = False
    while not reach:
        # print(i, j)
        if grid[i][j] == 4:
            print("Player Burnt")
            write_maze(i,j,oepen)
            return False, grid
        grid[i][j] = 2
        write_maze(i, j, bpen)
        visited = solve_maze.create_visited(dim)
        astar_check = solve_maze.a_star(astar_grid, dim, visited, [i, j], [dim - 1, dim - 1])
        if astar_check:
            for direction in dirr:
                x = i + direction[0]
                y = j + direction[1]
                if x == y == dim - 1:
                    reach = True
                    break
                if 0 <= x < dim and 0 <= y < dim and astar_grid[x][y] == 2 and grid[x][y] != 2:
                    i = x
                    j = y
                    grid = fire_spread(grid, dim, q)
                    astar_grid = copy.deepcopy(grid)
                    break
        else:
            print("No Solution")
            return False, grid
    grid[dim - 1][dim - 1] = 2
    # solve_maze.printLine(grid)
    return True, grid


def strategy3(astar_grid, dim, grid, unchanged_grid, q):
    i = 0
    j = 0
    grid[i][j] = 2
    write_maze(i, j, bpen)
    # playerpen.go_to(i,j)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    reach = False
    while not reach:
        if grid[i][j] == 4:
            print("Player Burnt")
            write_maze(i, j, oepen)
            return False, grid
        visited = solve_maze.create_visited(dim)
        astar_check = solve_maze.new_a_star(astar_grid, dim, visited, [i, j], [dim - 1, dim - 1], q)
        grid[i][j] = 2
        # print("I am here {}".format([i, j]))
        # playerpen.go_to(i, j)
        write_maze(i, j, bpen)
        #print(solve_maze.fire_pos)
        if astar_check:
            for direction in dirr:
                x = i + direction[0]
                y = j + direction[1]
                if x == y == dim - 1:
                    reach = True
                    break
                if 0 <= x < dim and 0 <= y < dim and astar_grid[x][y] == 2 and grid[x][y] != 2:
                    if grid[i][j] == 4:
                        write_maze(i, j, oepen)
                        print("Error")
                    i = x
                    j = y
                    grid = fire_spread(grid, dim, q)
                    astar_grid = copy.deepcopy(unchanged_grid)
                    break
        else:
            return False, grid
    grid[dim - 1][dim - 1] = 2
    write_maze(dim - 1, dim - 1, bpen)
    return True, grid


def fire_spread(grid, dim, q):
    grid_copy = copy.deepcopy(grid)
    dirr = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    for i in range(dim):
        for j in range(dim):
            if grid[i][j] != 4 and grid[i][j] != 1:
                neighbour_fire_count = 0
                for direction in dirr:
                    x = i + direction[0]
                    y = j + direction[1]
                    if x < 0 or x >= dim or y < 0 or y >= dim:
                        continue
                    if grid[x][y] == 4:
                        neighbour_fire_count += 1
                prob = 1 - ((1 - q) ** neighbour_fire_count)
                if random.random() <= prob:
                    pen_check = True
                    if grid[i][j] == 2:
                        pen_check = False
                    grid_copy[i][j] = 4
                    solve_maze.fire_pos.append([i,j])
                    if pen_check:
                        write_maze(i, j, fpen)
                    else:
                        write_maze(i, j, lbpen)
    return grid_copy


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze game")
wn.setup(600, 600)


def setup_maze(grid):
    for i in range(dim):
        for j in range(dim):
            screen_x = -288 + (j * 24)
            screen_y = 288 - (i * 24)
            if grid[i][j] == 1:
                wpen.goto(screen_x, screen_y)
                wpen.stamp()
            elif grid[i][j] == 2:
                bpen.goto(screen_x, screen_y)
                bpen.stamp()
            elif grid[i][j] == 4:
                fpen.goto(screen_x, screen_y)
                fpen.stamp()
            elif grid[i][j] == 0:
                ppen.goto(screen_x, screen_y)
                ppen.stamp()


dim = 20
q = 0.3
grid = solve_maze.create_fire_grid(dim, 0.2, True)
wpen = wPen()
fpen = fPen()
lbpen = lbPen()
oepen = oePen()
ppen = pPen()
bpen = bPen()
# playerpen = Player()
setup_maze(grid)

#grid[0][0] = 2
#grid[-1][-1] = 2


# solve_maze.a_star(grid,dim,solve_maze.create_visited(dim),[0,0],[dim-1,dim-1])
# grid = solve_maze.create_fire_grid(dim,0.3,True)
a_star_grid = copy.deepcopy(grid)
grid0 = copy.deepcopy(grid)
grid1 = copy.deepcopy(grid)
grid2 = copy.deepcopy(grid)
grid3 = copy.deepcopy(grid)
a_star_grid_copy = copy.deepcopy(a_star_grid)
a_star_grid_copy1 = copy.deepcopy(a_star_grid)

temp_check = solve_maze.a_star(a_star_grid, dim, solve_maze.create_visited(dim), [0, 0], [dim - 1, dim - 1])
if temp_check:
    strategy1(a_star_grid, dim, grid0, q)
print("1 Done")
setup_maze(grid)
sleep(5)
strategy2(a_star_grid_copy, dim, grid1,q)
print("2 Done")
setup_maze(grid)
sleep(5)
strategy3(a_star_grid_copy1,dim,grid2,grid3,q)
print("3 Done")


#check1, p_grid = strategy2(a_star_grid_copy, dim, grid1, q)
#temp_check = solve_maze.a_star(a_star_grid, dim, solve_maze.create_visited(dim), [0, 0], [dim - 1, dim - 1])
#if temp_check:
#   grid = strategy1(a_star_grid, dim, grid, q)

wn.exitonclick()
