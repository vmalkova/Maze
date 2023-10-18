import os
import pygame
import button_class as Btn
import maze_generator as Maze
import player_class as Plr
import input_box_class as Inp
import text_box_class as Box
from pygame.locals import *

# create a square for each wall and add it to the list of walls
class GameWall(object):

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], level["step"], level["step"])

# define all variables
wall = "W"
finish = "f"
solution = "B"
keyboard_shortcuts = f"Keyboard Shortcuts:\n  [n] - next level\n  [b] - back a level\n  [space_bar] - see solution of maze\n  [r] - reset to starting position\n  [enter] - create maze"
game_rules = f"Move the yellow block to red block (using arrow keys)\nGenerate maze of specified width (w) and height (h)"
info_text = f"{keyboard_shortcuts}\n\n{game_rules}"
levels = []
level = {"num": 0, "rows": 0, "cols": 0, "maze": [], "step": 16, "s_range": (0, 0)}
window = {"height": 500, "width": 500, "h_range": (250, 800), "w_range": (430, 1000)}

# define all buttons, input boxes & text boxes using their classes
def load_buttons():
    back_img = pygame.image.load('back_btn.png').convert_alpha()
    create_img = pygame.image.load('create_btn.png').convert_alpha()
    next_img = pygame.image.load('next_btn.png').convert_alpha()
    reset_img = pygame.image.load('reset_btn.png').convert_alpha()
    solution_img = pygame.image.load('solution_btn.png').convert_alpha()
    info_img = pygame.image.load('info_btn.png').convert_alpha()
    global info_btn, info_box, reset_btn, back_btn, next_btn, create_btn, solution_btn, width_inp, height_inp
    info_btn = Btn.Button(window["width"]-40, 5, info_img, 0.4)
    info_box = Box.TextBox(50, 15, info_text, font, window["width"]-50, window["height"]-150)
    reset_btn = Btn.Button(window["width"]-94, window["height"] - 100, reset_img, 0.5)
    back_btn = Btn.Button(10, window["height"] - 100, back_img, 0.5)
    next_btn = Btn.Button(110, window["height"] - 100, next_img, 0.5)
    solution_btn = Btn.Button(window["width"]-138, window["height"] - 50, solution_img, 0.5)
    create_btn = Btn.Button(10, window["height"] - 50, create_img, 0.48)
    width_inp = Inp.InputBox(150, window["height"] - 47, "w", font, 40, 40)
    height_inp = Inp.InputBox(200, window["height"] - 47, "h", font, 40, 40)

# display all buttons & input boxes
def show_buttons():
    info_btn.click(screen, False)
    reset_btn.click(screen, False)
    back_btn.click(screen, False)
    next_btn.click(screen, False)
    solution_btn.click(screen, False)
    create_btn.click(screen, False)
    height_inp.draw(screen, False, False, '')
    width_inp.draw(screen, False, False, '')

# display text box if user wants to
def show_text_box(hide_info):
    global window
    if not hide_info:
        b = pygame.Rect(0, 0, window["width"], window["height"])
        pygame.draw.rect(screen, (0, 0, 0), b)
        info_box.draw(screen)
    return not hide_info

# define window & block size & player speed
def size(num_l, num_s, l_range, small_range):
    global level
    level["step"] = int(small_range[0]/(num_s+2))
    screen_s = small_range[0]
    screen_l = level["step"] * (num_l+2)
    # make blocks as large as possible
    while screen_l < l_range[0]:
        level["step"] += 1
        screen_l = level["step"] * (num_l+2)
        screen_s = level["step"] * (num_s+2)
    # if blocks too large, find largest possible using axis it's too large for
    if screen_l > l_range[1]:
        level["step"] = int(l_range[1]/(num_l+2))
        screen_l = l_range[1]
    # if blocks are really small, calculate largest possible <= 16
    elif level["step"] < 16:
        level["step"] = 16
        while (num_l+2)*level["step"] > l_range[1]:
            level["step"] -= 1
        screen_l, screen_s = (num_l+2) * level["step"], (num_s+2) * level["step"]
    level["s_range"] = (level["step"] + 3, int(level["step"]*1.4 + 150/num_l + 6))
    return screen_l, screen_s

# define variables needed to display level
def show_level(level_num):
    global level, levels, window
    # make level if it doesn't already exist
    level_generated = len(levels)
    while len(levels) < level_num:
        # size of automatically generated maze should increase as level increases
        rows = cols = (level_num)*2+1
        level = {"num": len(levels)+1, "rows": rows, "cols": cols, "maze": [], "step": 16, "s_range": (0, 0)}
        level_generated += 1
        level["maze"] = generate_level(rows, cols)
        levels.append(level)
    # find level
    level = levels[level_num-1]
    # find window & block size & player speed
    if level["cols"] < level["rows"]*window["w_range"][1]/window["h_range"][1]:
        window["height"], window["width"] = size(level["rows"], level["cols"], window["h_range"], window["w_range"])
    else:
        window["width"], window["height"] = size(level["cols"], level["rows"], window["w_range"], window["h_range"])
    window["height"] += 140
    return level

# create a new level with the solution drawn on
def generate_level(rows, cols):
    maze = Maze.generate(rows, cols)
    solved_level = Maze.show_solution(maze)
    # change the position of the end block, so there's a wall behind it
    solved_level[-2] = solved_level[-2][:-3] + f"  {wall}"
    return solved_level
    
# draw the maze on the window
def draw_window(hide = True):
    # fill screen in white colour of the path
    screen.fill((255, 255, 255))
    maze_height, maze_width = level["step"]*len(level["maze"]), level["step"]*int(len(level["maze"][0])/2+0.5)
    background = []
    background.append(pygame.Rect(0, 0, window["width"], 40))
    background.append(pygame.Rect(0, maze_height+40, window["width"], window["height"]-maze_height))
    if maze_width < window["width"]:
        background.append(pygame.Rect(maze_width, 40, window["width"] - maze_width, maze_height))
    # draw a black backgound behind the buttons around the maze
    for b in background:
        pygame.draw.rect(screen, (0, 0, 0), b)
    # draw wall, end, (solution if user wants) and player
    for w in walls:
        pygame.draw.rect(screen, (0, 0, 0), w.rect)
    pygame.draw.rect(screen, (200, 0, 0), end_rect)
    if not hide:
        x = 0
        y = 40
        for row in level["maze"]:
            for col in row:
                if col == solution:
                    solution_rect = pygame.Rect(x, y, level["step"], level["step"])
                    pygame.draw.rect(screen, (140, 170, 225), solution_rect)
                x += level["step"]/2
            y += level["step"]
            x = 0
    pygame.draw.rect(screen, (225, 160, 0), player.rect)
    
# fade screen in/out of black
def fade_screen(level, a):
    fade = pygame.Surface((window["width"], window["height"]))
    # set fade colour to black
    fade.fill((0, 0, 0))
    alpha = 150 - 150 * a
    while alpha >= 0 and alpha <= 300:
        # change the transparency of the black screen
        alpha += a
        fade.set_alpha(alpha)
        # draw the faded black over the maze window   
        draw_window(level["maze"])
        show_buttons()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

# male a new maze of inputed size
def make_new_maze():
    global bools, level, levels
    bools["new_level"] = True
    bools["auto"] = False
    rows, cols = height_inp.get_input()*2-1, width_inp.get_input()*2-1
    level = {"num": len(levels)+1, "rows": rows, "cols": cols, "maze": [], "step": 16, "s_range": (0, 0)}
    level["maze"] = generate_level(rows, cols)
    levels.append(level)
    level = show_level(len(levels))
    
# load level of that level number
def load(level_num):
    global level
    bools["new_level"] = True
    if level_num > len(levels):
        # generate new level automatically if it wasn't made yet
        bools["auto"] = True
    else:
        # set level to the one of that level number
        bools["auto"] = False
        level = show_level(level_num)

# see if input in an input box is valid
def valid(box):
    if len(box.text) > 0:
        if box.text != "1" and box.text != box.auto_text:
            return True

# define boolean and key variables used in the while loop
bools = {"run": True, "new_level": True, "auto": True, "hide_info": True, "hide_solution": True, "fade": False}
k = {"mouse": False, "return": False, "back": False, "num": ''}
while bools["run"]:
    # if another level needs to be loaded
    if bools["new_level"]:
        walls = []
        # when new level loads, hide the solution
        bools["hide_solution"] = True
        pygame.display.quit()
        if bools["auto"]:
            # generate new level automatically
            level = show_level(level["num"]+1)
        # define walls & end in the maze
        x = 0
        y = 40
        for row in level["maze"]:
            for col in row:
                if col == wall:
                    GameWall((x, y))
                elif col == finish:
                    end_rect = pygame.Rect(x, y-level["step"], level["step"], level["step"])
                    GameWall((x,y))
                x += level["step"]/2
            y += level["step"]
            x = 0
        # set up the pygame display window
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(f"level {level['num']} ({int((level['cols']+1)/2)}x{int((level['rows']+1)/2)})")
        screen = pygame.display.set_mode((window["width"], window["height"]))
        font = pygame.font.Font(None, 40)
        player = Plr.Player(level["step"])
        load_buttons()
        if bools["fade"]:
            # fade out of black if needed
            fade_screen(level, -1)
        clock = pygame.time.Clock()
        speed = level["s_range"][0]
        bools["new_level"] = bools["fade"] = False
        
    clock.tick(60)
    # show input box if needed
    if not show_text_box(bools["hide_info"]):
        # redraw the window, so we can see the updated position of the player
        draw_window(bools["hide_solution"])

    # set all the keys to not being pressed
    for key in k.keys():
        if key == "num":
            k[key] = ''
        else:
            k[key] = False
        
    # record inputs from the keyboard and mouse and record what they were
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            bools["run"] = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            k["mouse"] = True
        if e.type == pygame.KEYDOWN:
            if e.unicode in [str(i) for i in range(10)]:
                k["num"] = e.unicode
            if e.key == pygame.K_ESCAPE:
                bools["run"] = False
            if e.key == pygame.K_SPACE:
                bools["hide_solution"] = not bools["hide_solution"]
            if e.key == pygame.K_i:
                bools["hide_info"] = not bools["hide_info"]
            if e.key == pygame.K_RETURN:
                k["return"] = True
            elif e.key == pygame.K_BACKSPACE:
                k["back"] = True
            
    # move player
    key = pygame.key.get_pressed()
    moving = False
    if key[pygame.K_LEFT]:
        player.move(-speed/6, 0, walls)
        moving = True
    elif key[pygame.K_RIGHT]:
        player.move(speed/6, 0, walls)
        moving = True
    if key[pygame.K_UP]:
        player.move(0, -speed/6, walls)
        moving = True
    elif key[pygame.K_DOWN]:
        player.move(0, speed/6, walls)
        moving = True
    # change speed
    if moving:
        speed = min(speed + level["s_range"][0]/100, level["s_range"][1])
        bools["hide_info"] = True
    else:
        speed = level["s_range"][0]
    # react to info, reset, next, back and solution button
    if info_btn.click(screen, k["mouse"]):
        bools["hide_info"] = not bools["hide_info"]
    if key[pygame.K_r] or reset_btn.click(screen, k["mouse"]):
        player.reset(level["step"])
    if key[pygame.K_n] or next_btn.click(screen, k["mouse"]):
        load(level["num"]+1)
    if solution_btn.click(screen, k["mouse"]):
        bools["hide_solution"] = not bools["hide_solution"]
    elif key[pygame.K_b] or back_btn.click(screen, k["mouse"]):
        load(level["num"]-1)
    # make new maze if valid inputs, otherwise activate the invalid input box
    if k["return"] or create_btn.click(screen, k["mouse"]):
        if valid(height_inp):
            width_inp.activate()
            height_inp.deactivate()
        else:
            width_inp.deactivate()
            height_inp.activate()
        if valid(height_inp) and valid(width_inp):
            make_new_maze()
              
    # if number added, switch which input box is active if it's full
    if len(k["num"]) == 1:
        if len(width_inp.text) == 2 or len(height_inp.text) < 2 and height_inp.active:
            width_inp.deactivate()
            height_inp.activate()
        else:
            width_inp.activate()
            height_inp.deactivate()
    
    # if backspace pressed on an empty active box, switch the active box
    if k["back"]:
        if width_inp.active and width_inp.text == "":
            width_inp.deactivate()
            height_inp.activate()
        elif height_inp.active and height_inp.text == "":
            width_inp.activate()
            height_inp.deactivate()
        
    # draw and update input boxes
    height_inp.draw(screen, k["mouse"], k["back"], k["num"])
    width_inp.draw(screen, k["mouse"], k["back"], k["num"])

    # if player reaches end, fade screen and load next level
    if player.rect.colliderect(end_rect):
        bools["fade"] = True
        fade_screen(level, 1)
        load(level["num"]+1)

    pygame.display.flip()
    clock.tick(360)
    
pygame.quit()