import pygame

colour_inactive = (255, 255, 255)
colour_active = (250, 160, 180)
    

class InputBox():
    def __init__(self, x, y, text, font, width, height):
        # define where the inpt box will be
        self.input_box = pygame.Rect(x, y, width, height)
        self.width, self.height = width, height
        # define what it will look like and say
        self.active = False
        self.text = self.auto_text = text
        self.colour = colour_inactive
        self.font = font

    def draw(self, screen, mouse_down, k_backspace, k_unicode):      
        pos = pygame.mouse.get_pos()
        # update box if acive
        if self.active:
            # backspace will remove the last character
            if k_backspace:
                self.text = self.text[:-1]
            # character will be added if it's valid
            elif k_unicode != '':
                if len(self.text) < 2:
                    if not (k_unicode == "0" and len(self.text) == 0):
                        self.text += k_unicode
        # activate box if it's clicked
        if mouse_down:
            if self.input_box.collidepoint(pos) and self.active == False:
                self.activate()
            else:
                self.deactivate()
        # draw the input box
        txt_surface = self.font.render(self.text, True, self.colour)
        self.input_box.w = max(self.width, txt_surface.get_width()+10)
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(screen, self.colour, self.input_box, 2)
    
    def activate(self):
        self.active = True
        if self.text == self.auto_text:
            self.text = ''
        self.colour = colour_active
    
    def deactivate(self):
        self.active = False
        if self.text == '':
            self.text = self.auto_text
        self.colour = colour_inactive
    
    def get_input(self):
        return int(self.text)