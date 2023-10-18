import pygame
    

class Button():
    def __init__(self, x, y, image, scale):
        # define what the button will look like
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # define where the button will be
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def click(self, surface, mouse_down):   
        pos = pygame.mouse.get_pos()
        perform_action = False
        # if button is clicked, perform action
        if mouse_down:
            if self.rect.collidepoint(pos):
                perform_action = True
        # display the button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return perform_action