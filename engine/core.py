import pygame as pg
import math

from argparse import ArgumentError

def set_pixel(surface: pg.Surface, x: int, y: int, cor: tuple[int,int,int]) -> None:
    x = int(x)
    y = int(y)

    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((x, y), cor)

def get_pixel(surface: pg.Surface, x: int, y: int) -> tuple[int, int, int] | None:
    x = int(x)
    y = int(y)

    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        c = surface.get_at((x, y))
        return c.r, c.g, c.b
    return None

def clear(surface: pg.Surface) -> None:
    surface.fill((0, 0, 0))

def draw_line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int], width: int=1, method: str='bresenham'):
    def _dda(x0: int, y0: int, x1: int, y1: int):
        dx = x1 - x0
        dy = y1 - y0

        step = max(abs(dx), abs(dy))
        dx = dx / step
        dy = dy / step
        x = x0
        y = y0
        i = 0

        while i <= step:
            px, py = round(x), round(y)
            set_pixel(surface, px, py, color)
            x += dx
            y += dy
            i += 1

    def _bresenham(x0: int, y0: int, x1: int, y1: int):
        # Flags para transformações
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0

        ystep = 1
        if dy < 0:
            ystep = -1
            dy = -dy

        # Bresenham clássico
        d = 2 * dy - dx
        incE = 2 * dy
        incNE = 2 * (dy - dx)

        x = x0
        y = y0

        while x <= x1:
            if steep:
                set_pixel(surface, y, x, color)
            else:
                set_pixel(surface, x, y, color)

            if d <= 0:
                d += incE
            else:
                d += incNE
                y += ystep

            x += 1

    x0, y0 = start_point
    x1, y1 = end_point

    # Linha de largura 1: comportamento original
    if width == 1:
        match method:
            case 'bresenham':
                _bresenham(x0, y0, x1, y1)
            case 'dda':
                _dda(x0, y0, x1, y1)
            case _:
                raise NotImplementedError
        return

    # Vetor da linha
    dx = x1 - x0
    dy = y1 - y0

    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        set_pixel(surface, x0, y0, color)
        return

    # Vetor perpendicular unitário
    nx = -dy / length
    ny = dx / length

    half = (width - 1) / 2

    for i in range(width):
        offset = i - half

        ox = round(nx * offset)
        oy = round(ny * offset)

        match method:
            case 'bresenham':
                _bresenham(
                    x0 + ox,
                    y0 + oy,
                    x1 + ox,
                    y1 + oy
                )

            case 'dda':
                _dda(
                    x0 + ox,
                    y0 + oy,
                    x1 + ox,
                    y1 + oy
                )

            case _:
                raise NotImplementedError

def draw_polygon(surface: pg.Surface, /, points: list[tuple[int,int]], color: tuple[int,int,int]) -> None:
    n = len(points)
    if n <= 2:
        raise ArgumentError

    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        draw_line(surface, (x0, y0), (x1, y1), color, method='bresenham')

def draw_circle(surface: pg.Surface, center, radius, color):
    a, b = center
    p = 1 - radius

    dx = 0
    dy = radius
    while dx <= dy:
        points = [
            (a + dx, b + dy),
            (a - dx, b + dy),
            (a + dx, b - dy),
            (a - dx, b - dy),
            (a + dy, b + dx),
            (a - dy, b + dx),
            (a + dy, b - dx),
            (a - dy, b - dx)
        ]

        for point in points:
            set_pixel(surface, point[0], point[1], color)

        dx += 1
        if p < 0:
            p += 2 * dx - 1
        else:
            dy -= 1
            p += 2 * (dx - dy) - 1

def draw_ellipse(surface: pg.Surface, /, center: tuple[int,int], x_radius: int, y_radius: int, color: tuple[int,int,int]) -> None:
    cx, cy = center

    rx2 = x_radius * x_radius
    ry2 = y_radius * y_radius

    x = 0
    y = y_radius

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    # Região 1
    p1 = ry2 - rx2 * y_radius + 0.25 * rx2

    while dx < dy:
        # Quatro pontos simétricos
        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, color)
        set_pixel(surface, cx - x, cy - y, color)

        x += 1
        dx += 2 * ry2

        if p1 < 0:
            p1 += dx + ry2
        else:
            y -= 1
            dy -= 2 * rx2
            p1 += dx - dy + ry2

    # Região 2
    p2 = (
            ry2 * (x + 0.5) ** 2
            + rx2 * (y - 1) ** 2
            - rx2 * ry2
    )

    while y >= 0:
        # Quatro pontos simétricos
        set_pixel(surface, cx + x, cy + y, color)
        set_pixel(surface, cx - x, cy + y, color)
        set_pixel(surface, cx + x, cy - y, color)
        set_pixel(surface, cx - x, cy - y, color)

        y -= 1
        dy -= 2 * rx2

        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            p2 += dx - dy + rx2

def half_ellipse(surface: pg.Surface, center, x_radius, y_radius, color, direction: str='north', fill: bool=False):
    cx, cy = center

    rx2 = x_radius * x_radius
    ry2 = y_radius * y_radius

    x = 0
    y = y_radius

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    # Região 1
    p1 = ry2 - rx2 * y_radius + 0.25 * rx2

    while dx < dy:
        # Quatro pontos simétricos
        if direction == 'south' or direction == 'east': set_pixel(surface, cx + x, cy + y, color)
        if direction == 'south' or direction == 'west': set_pixel(surface, cx - x, cy + y, color)
        if direction == 'north' or direction == 'east': set_pixel(surface, cx + x, cy - y, color)
        if direction == 'north' or direction == 'west': set_pixel(surface, cx - x, cy - y, color)

        x += 1
        dx += 2 * ry2

        if p1 < 0:
            p1 += dx + ry2
        else:
            y -= 1
            dy -= 2 * rx2
            p1 += dx - dy + ry2

    # Região 2
    p2 = (
            ry2 * (x + 0.5) ** 2
            + rx2 * (y - 1) ** 2
            - rx2 * ry2
    )

    while y >= 0:
        # Quatro pontos simétricos
        if direction == 'south' or direction == 'east': set_pixel(surface, cx + x, cy + y, color)
        if direction == 'south' or direction == 'west': set_pixel(surface, cx - x, cy + y, color)
        if direction == 'north' or direction == 'east': set_pixel(surface, cx + x, cy - y, color)
        if direction == 'north' or direction == 'west': set_pixel(surface, cx - x, cy - y, color)

        y -= 1
        dy -= 2 * rx2

        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += 2 * ry2
            p2 += dx - dy + rx2

    if direction == 'south' or direction == 'north':
        for x in range(cx - x_radius, cx + x_radius):
            set_pixel(surface, x, cy, color)
    elif direction == 'east' or direction == 'west':
        for y in range(cy - y_radius, cy + y_radius):
            set_pixel(surface, cx, y, color)