import pygame
import numpy as np

TITLE_NAME = "pyPhysics nGine"

def draw_border(screen, color, width, margin=10):
    
    # Current size of screen
    rectangle_dimension = screen.get_rect().inflate(-2*margin, -2*margin)
    rect_width, rect_height = rectangle_dimension.size

    # draw border on the top of the screen
    pygame.draw.rect(screen, color, rectangle_dimension, width)

    # Crosshair lines to show center of screen
    w, h = screen.get_size()
    pygame.draw.line(screen, (255, 160, 0), (0, h // 2), (w, h // 2), 1)
    pygame.draw.line(screen, (255, 160, 0), (w // 2, 0), (w // 2, h), 1)


def main() -> None:

    screen_size = 800, 600
    pygame.init()
    pygame.display.set_caption(TITLE_NAME)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        draw_border(screen, (255, 0, 0), 2, 40)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()