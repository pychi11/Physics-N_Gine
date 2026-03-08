import pygame
from physics import gravity_update, air_resistance, dt

# Draw circle


class Circle:
    def __init__(self, x: float,
                 y: float,
                 radius: float = 20,
                 color: tuple = (0, 255, 0),
                 vx: float = 0.0,
                 vy: float = 0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def update(self, screen_width: float,
               screen_height: float,
               gravity_pixels: float) -> None:
        if not self.is_dragging:
            gravity_update(self, gravity_pixels)
            air_resistance(self)
            # motiom of the ball
            self.x += self.vx * dt
            self.wall_collision(screen_width, screen_height)

    def wall_collision(self,
                       screen_width: float,
                       screen_height: float,
                       restitution: float = 0.8) -> None:

        # Left
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * restitution
        # Right
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
        if abs(self.vx) < 0.5:  # stop jittering
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
                    self.drag_offset = (
                        event.pos[0] - self.x, event.pos[1] - self.y)
                    self._prev_mouse_pos = event.pos
                    self._drag_v = (0.0, 0.0)

            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                # Update circle position
                self.x = event.pos[0] - self.drag_offset[0]
                self.y = event.pos[1] - self.drag_offset[1]

                # Calculate Velocity for ball, regarding momentum even
                # after the mouse has been released
                # and stores it
                dx = event.pos[0] - self._prev_mouse_pos[0]
                dy = event.pos[1] - self._prev_mouse_pos[1]
                if dt > 0:
                    self._drag_v = (dx / dt, dy / dt)
                self._prev_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.pointer_inside_circle(event.pos[0], event.pos[1]):
                    self.is_dragging = False

                    # Once mouse is released, set circle velocity to the last
                    # updated drag velocity
                    if hasattr(self, '_drag_v'):
                        self.vx, self.vy = self._drag_v

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(
            self.x), int(self.y)), int(self.radius))
