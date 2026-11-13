import asyncio
import pygame
import math
pygame.init()
WIDTH = 1300
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Explorer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
text_surface = font.render("", True, (255, 255, 255))
text_alpha = 0
zoom = 50
cam_x = WIDTH/2
cam_y = HEIGHT/2
scroll_old_x = 0
scroll_old_y = 0
move_mode = 0 
moving_home = 0
home = (WIDTH/2,HEIGHT/2)
text_label = ""
selected_dot = 0
draw_numbers = 1
adding_label = 0
in_range_of_1 = 0
id_in_range = 0
label = ""
class point:
    def __init__(self, x, y, l, i):
        self.x = x
        self.y = y
        self.label = l
        self.in_range = 0
        self.id = i
    def draw(self):
        global text_surface, id_in_range
        if not self.id == id_in_range:
            pygame.draw.circle(screen, (100, 100, 100), (round((self.x*zoom)+cam_x), round((-self.y*zoom)+cam_y)), 10) 
        else:
            pygame.draw.circle(screen, (0, 0, 0), (round((self.x*zoom)+cam_x), round((-self.y*zoom)+cam_y)), 10)
            self.draw_extra_details()       
        text_surface = font.render(self.label, True, (0, 0, 0))
        screen.blit(text_surface, ((self.x*zoom)+cam_x, (-self.y*zoom)+cam_y-50))
    def check_in_range(self, mouse_x, mouse_y):
        global id_in_range
        dist = ((((self.x*zoom)+cam_x)-mouse_x)**2+(((-self.y*zoom)+cam_y)-mouse_y)**2)
        if dist <= 15**2:
            self.in_range = 1
            id_in_range = self.id
        else:
            self.in_range = 0
    def draw_extra_details(self):
        text_surface = font.render(f"({self.x},{self.y})", True, (0, 0, 0))
        screen.blit(text_surface, ((self.x*zoom)+cam_x, (-self.y*zoom)+cam_y+20))  
    def relabel(self):
        global label
        if self.id == id_in_range:
            self.label = label


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
    first_x = math.ceil(-cam_x / zoom)
    last_x = math.floor((WIDTH - cam_x) / zoom)
    first_y = math.ceil((cam_y - HEIGHT) / zoom)
    last_y = math.floor(cam_y / zoom)
    for x in range(first_x, last_x + 1):
        screen_x = round(cam_x + x * zoom)
        pygame.draw.line(screen, (175, 175, 175), (screen_x, 0), (screen_x, HEIGHT))
    for y in range(first_y, last_y + 1):
        screen_y = round(cam_y - y * zoom)
        pygame.draw.line(screen, (175, 175, 175), (0, screen_y), (WIDTH, screen_y))
    for x in range(first_x, last_x + 1):
        if x % 5 == 0:
            screen_x = round(cam_x + x * zoom)
            pygame.draw.line(screen, (140, 140, 140), (screen_x, 0), (screen_x, HEIGHT), 3)
    for y in range(first_y, last_y + 1):
        if y % 5 == 0:
            screen_y = round(cam_y - y * zoom)
            pygame.draw.line(screen, (140, 140, 140), (0, screen_y), (WIDTH, screen_y), 3)
    pygame.draw.line(screen, (155, 155, 255), (round(cam_x), 0), (round(cam_x), HEIGHT), 6)
    pygame.draw.line(screen, (255, 155, 155), (0, round(cam_y)), (WIDTH, round(cam_y)), 6)
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
        points.append(point(mouse_x_id, -mouse_y_id, "", len(points)))
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
    global in_range_of_1, id_in_range
    mouse_x, mouse_y = pygame.mouse.get_pos()
    in_range_of_1 = 0
    id_in_range = -1
    for i in points:
        i.check_in_range(mouse_x, mouse_y)
        if i.in_range:
            in_range_of_1 = 1
def all_relable():
    for i in points:
        i.relabel()
def draw_numerals():
    x_label_y = max(0, min(round(cam_y + 10), HEIGHT - font.get_height()))
    first_x = math.ceil(((0 - cam_x) / zoom) / 5) * 5
    last_x = math.floor(((WIDTH - cam_x) / zoom) / 5) * 5
    for x in range(first_x, last_x + 1, 5):
        label = font.render(str(x), True, (0, 0, 0))
        screen_x = round(x * zoom + cam_x + 5)
        screen_x = max(0, min(screen_x, WIDTH - label.get_width()))
        screen.blit(label, (screen_x, x_label_y))
    first_y = math.ceil(((cam_y - HEIGHT) / zoom) / 5) * 5
    last_y = math.floor((cam_y / zoom) / 5) * 5
    for y in range(first_y, last_y + 1, 5):
        if y == 0:
            continue
        label = font.render(str(y), True, (0, 0, 0))
        screen_y = round(cam_y - y * zoom + 5)
        screen_y = max(0, min(screen_y, HEIGHT - label.get_height()))
        y_label_x = max(0, min(round(cam_x + 10), WIDTH - label.get_width()))
        screen.blit(label, (y_label_x, screen_y))
async def main():
    global scroll_old_x, scroll_old_y, moving_home, text_surface, text_label, text_alpha, adding_label, label
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and moving_home == 0 and adding_label == 0:
                    add_point()
                elif event.key == pygame.K_h and moving_home == 0 and adding_label == 0:
                    moving_home = 1
                    text_label = "Going Home"
                    text_alpha = 500
                elif event.key == pygame.K_g and moving_home == 0 and adding_label == 0:
                    set_new_home()
                    text_label = "New Home Coordinates Set"
                    text_alpha = 500
                elif event.key == pygame.K_l and moving_home == 0 and adding_label == 0:
                    if in_range_of_1:
                        adding_label = 1
                        text_label = "Type then click Enter to submit"
                        text_alpha = 255
                        label = points[id_in_range].label
                    else:
                        text_label = "Please Hover over Object to relabel"
                        text_alpha = 500
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    adding_label = 0
                    text_label = "Added Label"
                    text_alpha = 500
                elif event.unicode.isprintable() and adding_label == 1:
                    label += event.unicode
                elif event.key == pygame.K_BACKSPACE and adding_label == 1:
                    label = label[:-1]
        screen.fill((255, 255, 255))
        if moving_home == 0:
            scroll_code()
        else:
            move_home()
        draw_grid()
        if adding_label == 0:
            all_range_check()
        draw_all_points()
        draw_numerals()
        if adding_label:
            all_relable()
        text_surface = font.render(text_label, True, (0, 0, 0))
        text_surface.set_alpha(text_alpha)
        screen.blit(text_surface, (5,5))
        if not adding_label:
            text_alpha -= 10
        if text_alpha < 0:
            text_alpha = 0
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)
asyncio.run(main())