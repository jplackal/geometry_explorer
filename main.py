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
text_alpha = 0
zoom = 75
cam_x = WIDTH/2
cam_y = HEIGHT/2
scroll_old_x = 0
scroll_old_y = 0
move_mode = 0 
moving_home = 0
home = (WIDTH/2,HEIGHT/2)
text_label = ""
selected_dot = 0

class point:
    def __init__(self, x, y, l):
        self.x = x
        self.y = y
        self.label = l
        self.in_range = 0
    def draw(self):
        global text_surface
        if self.in_range == 0:
            pygame.draw.circle(screen, (100, 100, 100), (round((self.x*zoom)+cam_x), round((-self.y*zoom)+cam_y)), 10)        
        else:
            pygame.draw.circle(screen, (0, 0, 0), (round((self.x*zoom)+cam_x), round((-self.y*zoom)+cam_y)), 10)
        text_surface = font.render(self.label, True, (0, 0, 0))
        screen.blit(text_surface, ((self.x*zoom)+cam_x, (-self.y*zoom)+cam_y-50))
    def check_in_range(self, mouse_x, mouse_y):
        dist = ((((self.x*zoom)+cam_x)-mouse_x)**2+(((-self.y*zoom)+cam_y)-mouse_y)**2)
        if dist <= 15**2:
            self.in_range = 1
            self.draw_extra_details()
        else:
            self.in_range = 0
    def draw_extra_details(self):
        text_surface = font.render(f"({self.x},{self.y})", True, (0, 0, 0))
        screen.blit(text_surface, ((self.x*zoom)+cam_x, (-self.y*zoom)+cam_y+20))     

points = []
def already_exists(x, y):
    exists = 0
    for i in points:
        if i.x == x and i.y == y:
            exists = 1
    return exists
def move_home():
    global cam_x, cam_y, moving_home,scroll_old_x, scroll_old_y
    d_x = home[0]-cam_x
    d_y = home[1]-cam_y
    cam_x += d_x/5
    cam_y += d_y/5
    if abs(d_x)<1 and abs(d_y)<1:
        moving_home = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        scroll_old_x = mouse_x
        scroll_old_y = mouse_y
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
def add_point():
    global text_label, text_alpha
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x_id = round((mouse_x-cam_x)/zoom)
    mouse_y_id = round((mouse_y-cam_y)/zoom)
    if already_exists(mouse_x_id, -mouse_y_id) == 0:
        points.append(point(mouse_x_id, -mouse_y_id, ""))
        text_label = "Point Added"
        text_alpha = 255
    else:
        text_label = "Point Already Exists"
        text_alpha = 500
def draw_all_points():
    for point in points:
        point.draw()
def set_new_home():
    global cam_x, cam_y, home
    home = (cam_x, cam_y)
def all_range_check():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in points:
        i.check_in_range(mouse_x, mouse_y)
async def main():
    global scroll_old_x, scroll_old_y, moving_home, text_surface, text_label, text_alpha
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and moving_home == 0:
                    add_point()
                if event.key == pygame.K_h and moving_home == 0:
                    moving_home = 1
                    text_label = "Going Home"
                    text_alpha = 500
                if event.key == pygame.K_g and moving_home == 0:
                    set_new_home()
                    text_label = "New Home Coordinates Set"
                    text_alpha = 500

        screen.fill((255, 255, 255))
        if moving_home == 0:
            scroll_code()
        else:
            move_home()
        draw_grid()
        all_range_check()
        draw_all_points()
        text_surface = font.render(text_label, True, (0, 0, 0))
        text_surface.set_alpha(text_alpha)
        screen.blit(text_surface, (5,5))
        text_alpha -= 10
        if text_alpha < 0:
            text_alpha = 0
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)
asyncio.run(main())