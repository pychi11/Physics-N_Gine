import pygame
import pygame_gui
import random

from objects.circle import Circle
from physics import (
    collision_detection,
    dt,
    clock,
    GRAVITY_MS2
)
from ui_manager import PhysicsUserInterface

TITLE_NAME: str = "pyPhysics nGine"


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

    circles = []
    number_of_circles = 2

    manager = pygame_gui.UIManager((800, 600))

    ui = PhysicsUserInterface(manager)

    for i in range(number_of_circles):
        circles.append(Circle(100 + i*100, 500))

    gravity_pixels = GRAVITY_MS2 * 152

    running = True
    while running:
        events = pygame.event.get()
        w, h = screen.get_size()
        for event in events:
            # Press 'R' to restart
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            #     main()  # Restart the game by calling the main function again
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                              event.key == pygame.K_ESCAPE)):
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.USEREVENT:
                if (event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED
                        and event.ui_element == ui.gravity_slider):
                    # global gravity_pixels
                    gravity_pixels = event.value * 152
                if (event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == ui.set_circle_count_button):

                    try:
                        user_input = int(ui.circle_total_entry_box.get_text())
                        number_of_circles = user_input if user_input > 0 else number_of_circles

                        circles = []
                        for i in range(number_of_circles):
                            circles.append(Circle(random.randrange(
                                50, w, 31), random.randrange(50, h, 50)))
                    except ValueError:
                        # Handle invalid input
                        # need to work on adding a pop up message to only
                        # provide integer
                        print("Please enter a valid integer")

            manager.process_events(event)

        screen.fill((0, 0, 0))

        for circle in circles:
            circle.update(w, h, gravity_pixels)
            collision_detection(circles)
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
