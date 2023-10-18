import pygame


class Player(object):

    def __init__(self, step):
        # define a player square (smaller than path for easier movement)
        self.rect = pygame.Rect(step*1.1, 40 + step*1.1, step*0.8, step*0.8)

    def move(self, dx, dy, walls):
        # move in the y axis, then in x
        self.move_single_axis(dx, 0, walls)
        self.move_single_axis(0, dy, walls)

    def move_single_axis(self, dx, dy, walls):
        # move
        self.rect.x += dx
        self.rect.y += dy
        # move back if inside a wall
        for w in walls:
            if self.rect.colliderect(w.rect):
                if dx > 0:
                    self.rect.right = w.rect.left
                if dx < 0:
                    self.rect.left = w.rect.right
                if dy > 0:
                    self.rect.bottom = w.rect.top
                if dy < 0:
                    self.rect.top = w.rect.bottom
    
    def reset(self, step):
        # move to start
        self.rect.x = step*1.1
        self.rect.y = 40 + step*1.1