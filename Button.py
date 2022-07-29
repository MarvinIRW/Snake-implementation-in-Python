import pygame

class Button():
    '''class to represent a button'''
    def __init__(self, x, y, image, caption="", height=250, width=250, color=(0,128,0)):
        self.image = pygame.transform.scale(image, (int(height), int(width)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.caption = caption
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.caption_surf = self.font.render(caption, False, color)
        self.caption_rect = self.caption_surf.get_rect(midtop=self.rect.midtop).move(0, -40)

    def draw(self, screen):
        '''draws button on screen
        
        return:
        
        action -- True if Button is clicked'''
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        # check mousover and clicked pos
        if self.rect.collidepoint(pos):
            hover = self.rect.copy()
            hover.inflate_ip(20, 20)
            pygame.draw.rect(screen, 'Yellow', hover, border_radius=10)
            # leftclick detected
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw rect on screen
        screen.blit(self.image, self.rect)
        screen.blit(self.caption_surf, self.caption_rect)

        return action