import asyncio
import pygame
pygame.init()
WIDTH = 1300
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Explorer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
text_surface = font.render("", True, (255, 255, 255))
screen.blit(text_surface, (20, 20))
zoom = 50
cam_x = WIDTH/2
cam_y = HEIGHT/2
scroll_old_x = 0
scroll_old_y = 0
move_mode = 0 

class point:
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.label = l
        self.in_range = 0
    def draw(self):
        if self.in_range == 0:
            pygame.draw.circle(screen, (100, 100, 100), ((self.x*zoom)+cam_x, (self.y*zoom)+cam_y), 10)        
        else:
            pygame.draw.circle(screen, (0, 0, 0), ((self.x*zoom)+cam_x, (self.y*zoom)+cam_y), 10)
        text_surface = font.render(self.label, True, (0, 0, 0))
        screen.blit(text_surface, ((self.x*zoom)+cam_x, (self.y*zoom)+cam_y-50))
    def check_in_range(self, mouse_x, mouse_y):
        dist = ((((self.x*zoom)+cam_x)-mouse_x)**2+(((self.y*zoom)+cam_y)-mouse_y)**2)
        if dist <= 15**2:
            self.in_range = 1
        else:
            self.in_range = 0


def draw_grid():
    global cam_x, cam_y
    for i in range(0, int(WIDTH/zoom)+1):
        pygame.draw.rect(screen, (200,200,200),((i*(zoom)-3)+(cam_x%(zoom)),0,6,HEIGHT))
    for i in range(0, int(HEIGHT/zoom)+1):
        pygame.draw.rect(screen, (200,200,200),(0,(i*(zoom)-3)+(cam_y%(zoom)),WIDTH,6))
def scroll():
    global scroll_old_x, scroll_old_y, cam_x, cam_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cam_x += mouse_x - scroll_old_x
    cam_y += mouse_y - scroll_old_y
def scroll_code():
    global scroll_old_y, scroll_old_x
    if pygame.mouse.get_pressed()[0]:  # left button
        scroll()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scroll_old_x = mouse_x
    scroll_old_y = mouse_y
dot = point(0,0, "A")
dot2 = point(1,0, "B")
async def main():
    global scroll_old_x, scroll_old_y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        scroll_code()
        draw_grid()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dot.check_in_range(mouse_x, mouse_y)
        dot2.check_in_range(mouse_x, mouse_y)
        dot.draw()
        dot2.draw()
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)
asyncio.run(main())