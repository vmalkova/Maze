import os
import pygame


colour = (0, 0, 0)
text_colour = (250, 250, 250)
    
class TextBox():
    def __init__(self, x, y, text, font, width, height):
        # define where the box is
        self.pos = (x, y)
        self.box = pygame.Rect(x, y, width, height)
        # define what the box will look like
        self.width, self.height = width, height
        self.text = text
        self.colour, self.text_colour = colour, text_colour
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.box, 2)
        text = [word.split(' ') for word in self.text.splitlines(0)]
        space = self.font.size(' ')[0]
        x, y = self.pos[0], self.pos[1]
        # add text word by word
        for line in text:
            for word in line:
                word_surface = self.font.render(word, 0, self.text_colour)
                word_width, word_height = word_surface.get_size()
                # if word doesn't fit, put it on the next line
                if x + word_width >= self.width:
                    x = self.pos[0]
                    y += word_height 
                screen.blit(word_surface, (x, y))
                x += word_width + space
            # when line is done, move down a line
            x = self.pos[0]
            y += word_height
    