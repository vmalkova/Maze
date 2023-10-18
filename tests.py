import random


# main

# V load_buttons() & show_buttons() photo
# V show_text_box() photo (regular size & stretched out)
# V size() photo (of edge cases)
# V show_level() & find_dimensions() video (scrolling back through levels)
# V make_new_maze() & generate_level() video (new levels)
# V draw_window() photo 
# V fade_screen() video
# V valid() video (entering values into input boxes and pressing "create")


# text_box_class

# V draw() photo & show_text_box()


# button_class

# V click() video (clicking all buttons)


# input_box_class

# V draw() video (entering numbers and hitting backspace)
# V activate() video (clicking on an empty and not empty box)
# V deactivate() video (clicking off an empty and not empty box)
# V get_input() video (clicking "create")


# player_class

# V move() & move_single_axis() video (using arrow keys)
# V reset() video (clicking "reset")


import maze_generator as M


wall = "W"
path = " "
finish = "f"
avoid = "A"
out = "O"
solution = "B"
false = "N"

# Squares class


def test_make_path(m1):
    row = random.randint(0, m1.num_rows-1)
    col = random.randint(0, m1.num_cols-1)
    m1.maze.make_path(row, col)
    assert m1.show()[row+1][col*2+1] == path, "path not made"
    
def test_avoid_path(m1):
    row = random.randint(0, m1.num_rows-1)
    col = random.randint(0, m1.num_cols-1)
    m1.maze.avoid_path(row, col)
    assert m1.maze.get_square(row, col, m1.num_rows, m1.num_cols) == avoid, "path not avoided"

def test_make_solution(m1):
    row = random.randint(0, m1.num_rows-1)
    col = random.randint(0, m1.num_cols-1)
    m1.maze.make_solution(row, col)
    assert m1.maze.get_square(row, col, m1.num_rows, m1.num_cols) == solution, "solution not made"

def test_make_false(m1):
    row = random.randint(0, m1.num_rows-1)
    col = random.randint(0, m1.num_cols-1)
    m1.maze.make_false(row, col)
    assert m1.maze.get_square(row, col, m1.num_rows, m1.num_cols) == false, "false solution not made"
    
def test_get_square(m1):
    row = random.randint(0, m1.num_rows-1)
    col = random.randint(0, m1.num_cols-1)
    m1.maze.make_path(row, col)
    assert m1.show()[row+1][col*2+1] == path, "path not made"
    assert m1.maze.get_square(row, col, m1.num_rows, m1.num_cols) == path, "path not received"
    
def test_get_squares():
    test_show()
    
# Maze class

def test_show():
    num_rows = random.randint(7,13)
    num_cols = random.randint(3,6)*2+1
    m1 = M.Maze(num_rows, num_cols)
    assert len(m1.show()) == num_rows+2, "Num rows wrong"
    assert len(m1.show()[0]) == num_cols*2+3, "Num cols wrong"
    m1.row = random.randint(2, m1.num_rows - 3)
    m1.col = random.randint(2, (m1.num_cols-3)/2)
    total_walls = [row.count(wall) for row in m1.show()]
    assert total_walls[:-1].count(num_cols+2) == num_rows+1, "Top must only contain walls"
    assert total_walls[-1] == num_cols+1, "Bottom must cointain only walls other than the end"
    assert m1.show()[-1][-3] == finish, "Finish not in right place"
    m1.maze.avoid_path(m1.row, m1.col)
    total_avoid = [row.count(avoid) for row in m1.show()]
    assert sum(total_avoid) == 0, "Should turn avoid into path"
    m1.maze.make_false(m1.row, m1.col)
    total_false = [row.count(false) for row in m1.show()]
    assert sum(total_false) == 0, "Should turn false solution into path"
    m1.maze.rows[m1.row][m1.col] = wall
    return m1

def test_find_paths(m1):
    assert len(m1.find_paths(2, wall)) == 4, "find_paths doesn't find all the walls"

def test_dig(m1):
    original_pos = (m1.row+1, m1.col*2+1)
    m1.dig()
    final_pos = (m1.row+1, m1.col*2+1)
    mid_pos = (int(sum([final_pos[0], original_pos[0]])/2),int(sum([final_pos[1], original_pos[1]])/2))
    assert m1.show()[final_pos[0]][final_pos[1]] == path, "doesn't dig path"
    assert m1.show()[mid_pos[0]][mid_pos[1]] == path, "doesn't dig path"

def test_make_maze():
    num_rows = random.randint(3,6)*2-1
    num_cols = random.randint(3,6)*2-1
    m2 = M.Maze(num_rows, num_cols)
    m2.make_maze()
    total_walls = [row.count(wall) for row in m2.show()]
    total_paths = (num_rows+2) * (num_cols+2) - sum(total_walls)
    assert int(total_paths/2) == m2.max_paths, "not right amount of paths dug"
    return m2

def test_h(m1):
    pos = (random.randint(3,6)*2-1, random.randint(3,6)*2-1)
    assert m1.h(pos) == (m1.num_rows-pos[0])+(m1.num_cols-pos[1]), "not right h"
    
def test_find_costs(m2):
    m2.row, m2.col = 0, 0
    [paths, costs] = m2.find_costs()
    sum_paths = 0
    if m2.show()[1][4] == path:
        sum_paths += 1
    if m2.show()[2][2] == path:
        sum_paths += 1
    assert len(paths) == sum_paths, "not right amount of paths found"
    assert costs[0] == m2.num_rows + m2.num_cols - 2, "not right cost"
    return paths[0]

def test_trace_paths(m2):
    m2.row = random.randint(2, m2.num_rows-3)
    m2.col = random.randint(2, m2.num_cols-3)
    around = [(m2.row-1, m2.col), (m2.row+1, m2.col), (m2.row, m2.col-1), (m2.row, m2.col+1)]
    for (row, col) in around:
        m2.maze.make_false(row, col)
    assert len(m2.trace_paths()) == 4, "not all false solutions found"
    for (row, col) in around:
        m2.maze.make_path(row, col)
    assert len(m2.trace_paths()) == 0, "no false solutions shuold've been found"

def test_draw_solution(m2, s_path):
    m2.draw_solution(s_path)
    assert m2.maze.get_square(s_path[0][0], s_path[0][1], m2.num_rows, m2.num_cols) == false, "solution not drawn"
    assert m2.maze.get_square(s_path[1][0], s_path[1][1], m2.num_rows, m2.num_cols) == false, "solution not drawn"

def test_draw_invalid_solution(m2):
    c_sqr = (m2.row, m2.col)
    s_sqr = random.choice([(m2.row-1, m2.col), (m2.row+1, m2.col), (m2.row, m2.col-1), (m2.row, m2.col+1)])
    m2.maze.make_solution(s_sqr[0], s_sqr[1])
    m2.draw_invalid_solution()
    assert m2.maze.get_square(c_sqr[0], c_sqr[1], m2.num_rows, m2.num_cols) == path, "original square not path"
    assert m2.maze.get_square(s_sqr[0], s_sqr[1], m2.num_rows, m2.num_cols) == path, "square in between not path"
    
def test_check_if_solved(m2):
    m2.row = m2.num_rows-1
    m2.col = m2.num_cols-1
    assert m2.check_if_solved() == True, "Should be solved"
    m2.row = random.randint(0, m2.num_rows-1)
    m2.col = random.randint(0, m2.num_cols-2)
    assert m2.check_if_solved() == False, "Shouldn't be solved"
    
def test_check_if_line(m2):
    m2.row = 0
    m2.col = 0
    assert m2.check_if_line() == True, "Should finish line"
    m2.row = random.randint(0, m2.num_rows-1)
    m2.col = random.randint(1, m2.num_cols-1)
    assert m2.check_if_line() == False, "Shouldn't finish line"
    
def test_solve(m3):
    m3.solve()
    assert m3.maze.get_square(1, 0, m3.num_rows, m3.num_cols) == false or m3.maze.get_square(0, 1, m3.num_rows, m3.num_cols) == false, "possible solution not drawn"
    assert (m3.row, m3.col) ==(0, 2) or (m3.row, m3.col) == (2, 0), "not moved along path"
    paths, costs = m3.find_costs()
    shortest_path = paths[costs.index(min(costs))]
    m3.solve()
    assert (m3.row, m3.col) == shortest_path[1], "not moved along shortest path"
    
def test_draw_line(m3):
    for i in range(2):
        m3.draw_line()
        if (m3.row, m3.col) == (0, 0):
            break
    assert (m3.row, m3.col) == (0, 0), "not moved along path"
    assert m3.maze.get_square(1, 0, m3.num_rows, m3.num_cols) == solution or m3.maze.get_square(0, 1, m3.num_rows, m3.num_cols) == solution, "solution not drawn"
    
def test_show_solution(m4):
    M.show_solution(m4)
    m4.row, m4.col = 0, 0
    while not m4.check_if_solved():
        path = m4.find_paths(1, solution)[0]
        assert len(m4.find_paths(1, solution)) != 0, "solution doesn't lead to end"
        m4.maze.make_path(path[0][0], path[0][1])
        (m4.row, m4.col) = path[1]
    
def test_generate():
    return test_make_maze()
        

def test():
    test_get_squares()
    m1 = test_show()
    test_find_paths(m1)
    test_dig(m1)
    
    test_make_path(m1)
    test_avoid_path(m1)
    test_make_solution(m1)
    test_make_false(m1)
    test_get_square(m1)
    
    m2 = test_make_maze()
    test_h(m2)
    s_path = test_find_costs(m2)
    test_draw_solution(m2, s_path)
    test_trace_paths(m2)
    test_draw_invalid_solution(m2)
    test_check_if_solved(m2)
    test_check_if_line(m2)
    
    m3 = test_make_maze()
    test_solve(m3)
    test_draw_line(m3)
    
    m4 = test_generate()
    test_show_solution(m4)
    
test()