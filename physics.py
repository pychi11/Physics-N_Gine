import math
import pygame

GRAVITY_MS2: float = 9.8

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0

# this conversion is done so that in the future when
# there are UI inputs from the user, it can be changed realtime
# and updated as the engine is being used
# 152 is the amount of pixels that equals a meter
air_resistance_value = 0.999


def gravity_update(obj, gravity_pixels) -> tuple:
    """
        dt      = elapsed time in seconds since last update
        gravity = acceleration to apply (pixels/second squared)
    """

    obj.vy += gravity_pixels * dt
    # x  += vx * dt
    obj.y += obj.vy * dt
    return obj.vy, obj.y


def air_resistance(obj) -> tuple:
    """
        dt      = elapsed time in seconds since last update
        air_resistance = coefficient of air resistance (pixels/second squared)
    """
    # obj.vx *= 0.999 # Air resistance
    obj.vx -= air_resistance_value * dt
    obj.vy -= air_resistance_value * dt
    if abs(obj.vx) < 5:  # apply floor friction
        obj.vx = 0.0
    return obj.vx, obj.vy


def resolve_circle_collision(c1, c2):
    # Vector between centers
    dx = c2.x - c1.x
    dy = c2.y - c1.y
    distance = math.hypot(dx, dy)
    if distance == 0:
        return  # Prevent division by zero, or optionally jitter
        # the objects apart

    # Minimum translation distance to push balls apart
    overlap = (c1.radius + c2.radius) - distance
    nx = dx / distance
    ny = dy / distance

    # Push them apart
    c1.x -= nx * overlap / 2
    c1.y -= ny * overlap / 2
    c2.x += nx * overlap / 2
    c2.y += ny * overlap / 2

    # Velocity difference along normal
    dvx = c2.vx - c1.vx
    dvy = c2.vy - c1.vy
    vn = dvx * nx + dvy * ny

    if vn > 0:
        return  # They are moving apart already

    # Elastic collision response for equal mass and radius
    c1.vx += vn * nx
    c1.vy += vn * ny
    c2.vx -= vn * nx
    c2.vy -= vn * ny


def collision_detection(circles: list) -> None:

    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            c1 = circles[i]
            c2 = circles[j]
            dx = c2.x - c1.x
            dy = c2.y - c1.y
            distance_sq = dx ** 2 + dy ** 2
            radii_sum = c1.radius + c2.radius
            if distance_sq <= radii_sum ** 2:
                resolve_circle_collision(c1, c2)
