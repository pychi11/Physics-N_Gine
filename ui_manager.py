import pygame
import pygame_gui


class PhysicsUserInterface:
    def __init__(self, manager):
        # Create a UIManager instance to manage UI elements
        self.manager = manager

        # Create a button
        self.circle_total_entry_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((100, 100), (200, 50)),
            manager=manager
        )

        self.set_circle_count_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((210, 70), (90, 30)),
            text="Set Circles",
            manager=manager
        )

        self.gravity_slider_label = pygame_gui.elements.UILabel(
            # Position label above slider
            relative_rect=pygame.Rect((50, 180), (150, 20)),
            text='Gravity',
            manager=manager
        )
        self.gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((100, 200), (200, 50)),
            start_value=9.8,
            value_range=(-10.0, 50.0),
            manager=manager
        )
