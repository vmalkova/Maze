import random
wall = "W"
path = " "
finish = "f"
avoid = "A"
out = "O"
solution = "B"
false = "N"


class Squares():
    def __init__(self, num_rows, num_cols):
        self.rows = []
        for row in range(num_rows):
            row_list = []
            for col in range(num_cols):
                row_list.append(wall)
            self.rows.append(row_list)
            
    # draw a symbol on a specific square
    def make_path(self, row, col):
        self.rows[row][col] = path

    def avoid_path(self, row, col):
        self.rows[row][col] = avoid
    
    def make_solution(self, row, col):
        self.rows[row][col] = solution
        
    def make_false(self, row, col):
        self.rows[row][col] = false

    # return the symbol in a specific square
    def get_square(self, row, col, num_rows, num_cols):
        if row >= 0 and col >= 0 and row < num_rows and col < num_cols:
            return self.rows[row][col]
        return out

    # return the maze as a list, with walls and a finish square added around the edge
    def get_squares(self):
        maze_list = []
        hor_walls = [f"{(wall + ' ') * (len(self.rows[0]) + 1)}{wall}",
                     f"{(wall + ' ') * (len(self.rows[0]) - 1)}{wall + ' ' + finish + ' '}{wall}"]
        maze_list.append(hor_walls[0])
        for row in self.rows:
            row_list = wall
            for sqr in row:
                if sqr == avoid or sqr == false:
                    row_list += " " + path
                else:
                    row_list += " " + sqr
            row_list += " " + wall
            maze_list.append(row_list)
        maze_list.append(hor_walls[1])
        return maze_list


class Maze():
    def __init__(self, num_rows, num_cols):
        self.row = 0
        self.col = 0
        self.path_count = 1
        self.max_paths = (num_rows + 1) * (num_cols + 1) / 4
        self.maze = Squares(num_rows, num_cols)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.all_paths = [(0, 0)]
    
    # return the maze as a list
    def show(self):
        return self.maze.get_squares()

    # return all paths (2 squares) with a "symbol" "n" squares away from current square
    def find_paths(self, n, symbol):
        paths = []
        if self.maze.get_square(self.row - n, self.col, self.num_rows, self.num_cols) == symbol:
            paths.append([(self.row - 1, self.col), (self.row - 2, self.col)])
        if self.maze.get_square(self.row + n, self.col, self.num_rows, self.num_cols) == symbol:
            paths.append([(self.row + 1, self.col), (self.row + 2, self.col)])
        if self.maze.get_square(self.row, self.col - n, self.num_rows, self.num_cols) == symbol:
            paths.append([(self.row, self.col - 1), (self.row, self.col - 2)])
        if self.maze.get_square(self.row, self.col + n, self.num_rows, self.num_cols) == symbol:
            paths.append([(self.row, self.col + 1), (self.row, self.col + 2)])
        return paths

    def dig(self):
        choices = self.find_paths(2, wall)
        if choices == []:
            # go back along path to find more paths to dig
            self.maze.avoid_path(self.row, self.col)
            choices = self.find_paths(1, path)
            av_row, av_col = choices[0][0]
            self.maze.avoid_path(av_row, av_col)
            self.row, self.col = choices[0][1]
        else:
            # dig paths into walls, without making loops
            self.path_count += 1
            steps = random.choice(choices)
            self.row, self.col = steps[1]
            for step in steps:
                self.maze.make_path(step[0], step[1])

    def make_maze(self):
        # starting from a random square
        self.row = random.randint(0, (self.num_rows - 1) / 2) * 2
        self.col = random.randint(0, (self.num_cols - 1) / 2) * 2
        self.maze.make_path(self.row, self.col)
        # dig paths until maze is made
        while self.path_count < self.max_paths:
            self.dig()
    
    # measure distance from current spot to end
    def h(self,current_spot):
        a, b = (self.num_rows, self.num_cols), current_spot
        return (a[0]-b[0])+(a[1]-b[1])
    
    def find_costs(self):
        costs = []
        paths = []
        # find paths we can go to (with symbol "path" or "avoid")
        for p in self.all_paths:
            self.row, self.col = p[0], p[1]
            for found_path in self.find_paths(1, path):
                costs.append(self.h(found_path[1]))
                paths.append(found_path)
            for found_path in self.find_paths(1, avoid):
                costs.append(self.h(found_path[1]))
                paths.append(found_path)
        # return the cost of each of these paths
        return [paths,costs]
    
    # follow back the paths we used to reach the end
    def trace_paths(self):
        paths = []
        for found_path in self.find_paths(1,false):
            paths.append(found_path)
        return paths
    
    # move along and mark a path that could possibly lead to the end
    def draw_solution(self, s_path):
        for square in s_path:
            self.maze.make_false(square[0], square[1])
        self.row, self.col = s_path[1][0], s_path[1][1]
        self.all_paths.append((self.row, self.col))
    
    # mark the path that don't lead to the actual solution as paths
    def draw_invalid_solution(self):
        self.maze.make_path(self.row, self.col)
        choice = self.find_paths(1, solution)[0]
        self.maze.make_path(choice[0][0], choice[0][1])
        self.row, self.col = choice[1][0], choice[1][1]
    
    # check if current square is the end
    def check_if_solved(self):
        return (self.row+1, self.col+1) == (self.num_rows, self.num_cols)
    
    # check if current square is the start
    def check_if_line(self):
        return (self.row, self.col) == (0,0)
    
    def solve(self):
        # draw possible solutions
        paths_costs = self.find_costs()
        paths, costs = paths_costs[0], paths_costs[1]
        # mark the path closest to the end as a possible solution
        shortest_path = paths[costs.index(min(costs))]
        self.draw_solution(shortest_path)
    
    def draw_line(self):
        self.maze.make_solution(self.row, self.col)
        paths = self.trace_paths()
        if paths == []:
            # move back if at a dead end
            self.draw_invalid_solution()
        else:
            # follow and mark the possible solution as a real solution
            for path in paths[0]:
                self.maze.make_solution(path[0], path[1])
            path = paths[0][1]
            self.row, self.col = path[0], path[1]

def show_solution(maze):
    # starting from start, find a way to reach the end
    maze.row, maze.col = 0, 0
    solved = maze.check_if_solved()
    maze.maze.make_false(0, 0)
    while not(solved):
        maze.solve()
        solved = maze.check_if_solved()
    # once end is reached, work backwards to find the line that links the start to the end
    line = False
    while not(line):
        maze.draw_line()
        line = maze.check_if_line()
    # return the maze (with a solution) as a list
    return maze.show()

def generate(num_rows, num_cols):
    # generate a maze (with no solution)
    m = Maze(num_rows, num_cols)
    m.make_maze()
    return m