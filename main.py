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
        self.is_dragging = False
        self.drag_offset = (0, 0)


    def update(self, screen_width:float, screen_height:float):
        if not self.is_dragging:
            gravity_update(self)
            # motiom of the ball
            self.x += self.vx * dt
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


    def pointer_inside_circle(self, px, py) -> bool:
        # Returns True if pointer is inside the cicle
        dx = px - self.x
        dy = py - self.y
        return dx*dx + dy*dy <= self.radius * self.radius



    def mouse_control(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pointer_inside_circle(event.pos[0], event.pos[1]):
                    self.is_dragging = True
                    self.drag_offset = (event.pos[0] - self.x, event.pos[1] - self.y)
                    self._prev_mouse_pos = event.pos
                    self._drag_v = (0.0, 0.0)

            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                # Update circle position
                self.x = event.pos[0] - self.drag_offset[0]
                self.y = event.pos[1] - self.drag_offset[1]

                # Calculate Velocity for ball, regarding momentum even after the mouse has been released
                # and stores it
                dx = event.pos[0] - self._prev_mouse_pos[0]
                dy = event.pos[1] - self._prev_mouse_pos[1]
                if dt > 0:
                    self._drag_v = (dx / dt, dy / dt)
                self._prev_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and  event.button == 1:
                if self.pointer_inside_circle(event.pos[0], event.pos[1]):
                    self.is_dragging = False

                    # Once mouse is released, set circle velocity to the last updated drag velocity
                    if hasattr(self, '_drag_v'):
                        print(self._drag_v)
                        self.vx, self.vy = self._drag_v 
                        print(f"{self.vx}, velocity_'X'_axis")


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
    circle_1 = Circle(400, 300, 50, (0, 255, 0))
    circle_2 = Circle(200, 300, 50, (0, 0, 244))

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Press 'R' to restart
            #     main()  # Restart the game by calling the main function again
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        screen.fill((0, 0, 0))
        w, h = screen.get_size()

        circle_1.update(w, h)
        circle_1.mouse_control(events)
        circle_1.draw(screen)

        circle_2.update(w, h)
        circle_2.mouse_control(events)
        circle_2.draw(screen)

        draw_border(screen, (255, 0, 0), 2, 40)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()