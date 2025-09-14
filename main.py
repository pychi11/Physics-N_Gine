import pygame
import numpy as np

TITLE_NAME:str = "pyPhysics nGine"
GRAVITY_MS2:float = 9.8

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0

# this conversion is done so that in the future when there are UI inputs from the user, it can be changed realtime
# and updated as the engine is being used
gravity_pixels = GRAVITY_MS2 * 152 # 152 is the amount of pixels that equals a meter

def gravity_update(obj) -> tuple:
    """
        dt      = elapsed time in seconds since last update
        gravity = acceleration to apply (pixels/second squared)
    """

    obj.vy += gravity_pixels * dt
    # x  += vx * dt
    obj.y  += obj.vy * dt
    return obj.vy, obj.y

# Draw circle
class Circle:
    def __init__(self, x:float, y:float, radius:float, color:tuple, vx:float=0.0, vy: float=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color


    def update(self, screen_width:float, screen_height:float):
        
        gravity_update(self)
        self.wall_collision(screen_width, screen_height)


    def wall_collision(self, screen_width:float, screen_height:float, restitution:float=0.8):
        
        # left and right walls
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * restitution
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.vx = -self.vx * restitution
 
        # Top and bottom walls
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy * restitution
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.vy = -self.vy * restitution


    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

def draw_border(screen, color, width, margin=10):
    
    # Current size of screen
    rectangle_dimension = screen.get_rect().inflate(-2*margin, -2*margin)
    # rect_width, rect_height = rectangle_dimension.size

    # draw border on the top of the screen
    pygame.draw.rect(screen, color, rectangle_dimension, width)

    # Crosshair lines to show center of screen
    w, h = screen.get_size()
    pygame.draw.line(screen, (255, 160, 0), (0, h // 2), (w, h // 2), 1)
    pygame.draw.line(screen, (255, 160, 0), (w // 2, 0), (w // 2, h), 1)


def main() -> None:

    screen_size = 1200, 1200
    pygame.init()
    pygame.display.set_caption(TITLE_NAME)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    circle = Circle(400, 300, 50, (0, 255, 0))

    running = True
    while running:
        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Press 'R' to restart
            #     main()  # Restart the game by calling the main function again
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        screen.fill((0, 0, 0))
        w, h = screen.get_size()
        circle.update(w, h)
        circle.draw(screen)
        draw_border(screen, (255, 0, 0), 2, 40)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()