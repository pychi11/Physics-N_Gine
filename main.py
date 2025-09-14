import pygame
import pygame_gui
import numpy as np

TITLE_NAME:str = "pyPhysics nGine"
GRAVITY_MS2:float = 9.8

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0

# this conversion is done so that in the future when there are UI inputs from the user, it can be changed realtime
# and updated as the engine is being used
gravity_pixels = GRAVITY_MS2 * 152 # 152 is the amount of pixels that equals a meter
air_resistance_value = 0.999

def gravity_update(obj) -> tuple:
    """
        dt      = elapsed time in seconds since last update
        gravity = acceleration to apply (pixels/second squared)
    """

    obj.vy += gravity_pixels * dt
    # x  += vx * dt
    obj.y  += obj.vy * dt
    return obj.vy, obj.y


def air_resistance(obj) -> tuple:
    """
        dt      = elapsed time in seconds since last update
        air_resistance = coefficient of air resistance (pixels/second squared)
    """
    # obj.vx *= 0.999 # Air resistance
    obj.vx -= air_resistance_value * dt
    obj.vy -= air_resistance_value * dt
    if abs(obj.vx) < 5: # apply floor friction
        obj.vx = 0.0
    return obj.vx, obj.vy


# Draw circle
class Circle:
    def __init__(self, x:float, y:float, radius:float=20, color:tuple=(0, 255, 0), vx:float=0.0, vy: float=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.is_dragging = False
        self.drag_offset = (0, 0)


    def update(self, screen_width:float, screen_height:float) -> None:
        if not self.is_dragging:
            gravity_update(self)
            air_resistance(self)
            # motiom of the ball
            self.x += self.vx * dt
            self.wall_collision(screen_width, screen_height)


    def wall_collision(self, screen_width:float, screen_height:float, restitution:float=0.8) -> None:
        
        # left and right walls
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * restitution
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.vx = -self.vx * restitution
 
        # Top 
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy * restitution
        
        # Bottoom Wall
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.vy = -self.vy * restitution
            self.apply_floor_friction()

    def apply_floor_friction(self):
        # friction is applied when circle touches the wall 
        friction_coeff = 0.98
        self.vx *= friction_coeff
        if abs(self.vx) < 0.5: # stop jittering
            self.vx = 0


    def pointer_inside_circle(self, px, py) -> bool:
        # Returns True if pointer is inside the cicle
        dx = px - self.x
        dy = py - self.y
        return dx*dx + dy*dy <= self.radius * self.radius


    def mouse_control(self, events) -> None:
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
                        self.vx, self.vy = self._drag_v 


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

    screen_size = 1200, 800
    pygame.init()
    pygame.display.set_caption(TITLE_NAME)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    # Create a UIManager instance to manage UI elements
    manager = pygame_gui.UIManager((300, 300))

    # Create a button
    circle_total_entry_box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((100, 100), (200, 50)),
        manager=manager
    )

    set_circle_count_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((210, 70), (90, 30)),
    text="Set Circles",
    manager=manager
    )

    gravity_slider_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 180), (150, 20)),  # Position label above slider
        text='Gravity',
        manager=manager
    )
    gravity_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((100, 200), (200, 50)),
        start_value=9.8,
        value_range=(-10.0, 50.0),
        manager=manager
    )

    circles  = [] 
    number_of_circles = 2
    
    for i in range(number_of_circles):
        circles.append(Circle(100 + i*100, 500))

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
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == gravity_slider:
                    global gravity_pixels
                    gravity_pixels = event.value * 152 
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == set_circle_count_button:
                    
                    try:
                        user_input = int(circle_total_entry_box.get_text()) 
                        number_of_circles = user_input if user_input > 0 else number_of_circles
                        
                        circles = []
                        for i in range(number_of_circles):
                            circles.append(Circle(100 + i*100, 500))
                    except ValueError:
                        # Handle invalid input
                        # need to work on adding a pop up message to only provide integer
                        print("Please enter a valid integer")

            
            manager.process_events(event)


        screen.fill((0, 0, 0))
        w, h = screen.get_size()


        for circle in circles:
            circle.update(w, h)
            circle.mouse_control(events)
            circle.draw(screen)

        # UI screen update
        manager.update(dt)
        manager.draw_ui(screen)

        draw_border(screen, (255, 0, 0), 2, 40)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()