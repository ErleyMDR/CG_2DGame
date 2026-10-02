from argparse import ArgumentError

import pygame as pg
import math

SQRTOF3: float | int = math.sqrt(3)

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

class Rasterizer:

    @staticmethod
    def line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int], width: int=1, method: str='bresenham'):
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

        match method:
            case 'bresenham':
                _bresenham(start_point[0], start_point[1], end_point[0], end_point[1])
            case 'dda':
                _dda(start_point[0], start_point[1], end_point[0], end_point[1])
            case _:
                raise NotImplementedError

    @staticmethod
    def polygon(surface: pg.Surface, /, points: list[tuple[int,int]], color: tuple[int,int,int], fill: bool=False) -> None:
        n = len(points)
        if n <= 2:
            raise ArgumentError

        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            Rasterizer.line(surface, (x0, y0), (x1, y1), color, method='bresenham')

        if fill:
            Painter.scanline_fill(surface, points=points, color=color)

    @staticmethod
    def curved_line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int]) -> None:
        ...

    @staticmethod
    def circle(surface: pg.Surface, center, radius, color, *, fill: bool=False):
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

        if fill:
            Painter.flood_fill(surface, center[0], center[1], color, color)

    @staticmethod
    def ellipse(surface: pg.Surface, /, center: tuple[int,int], x_radius: int, y_radius: int, color: tuple[int,int,int], *, fill: bool=False) -> None:
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

    @staticmethod
    def rectangle(surface: pg.Surface, center, width, height, color, *, fill: bool=False, border_width: int=1):
        w, h = width // 2, height // 2
        v = [
            (center[0] - w, center[1] - h),
            (center[0] + w, center[1] - h),
            (center[0] + w, center[1] + h),
            (center[0] - w, center[1] + h)
        ]
        Rasterizer.polygon(surface, v, color, fill=fill)
        return v

    @staticmethod
    def square(surface: pg.Surface, center, size, color, *, fill: bool=False):
       return Rasterizer.rectangle(surface, center, size, size, color, fill=fill)

    @staticmethod
    def triangle(surface: pg.Surface, center, height, side_l, color):
        if (side_l * 2) / SQRTOF3 < height:
            raise ArgumentError
        hh = height // 2
        hs = side_l // 2
        v = [
            (center[0], center[1] - hh),
            (center[0] - hs, center[1] + hh),
            (center[0] + hs, center[1] + hh),
        ]

        Rasterizer.polygon(surface, v, color)
        return v

    @staticmethod
    def half_cirle(surface: pg.Surface, center, radius, color, direction: str='north', fill: bool=False):
        ...

    @staticmethod
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

    @staticmethod
    def reuleaux_triangle(surface: pg.Surface, center, height, side_l, color): ...

class Painter:

    @staticmethod
    def flood_fill(surface: pg.Surface, x: int, y: int, /, fill_color: tuple[int,int,int], boundary_color: tuple[int,int,int]) -> None:
        height, width = surface.get_height(), surface.get_width()

        s = [(x, y)]
        while s:
            x, y = s.pop()

            if not (0 <= x < width and 0 <= y < height):
                continue

            cor_atual = surface.get_at((x, y))[:3]

            if cor_atual == fill_color or cor_atual == boundary_color:
                continue

            set_pixel(surface, x, y, fill_color)

            s.append((x + 1, y))
            s.append((x, y + 1))
            s.append((x - 1, y))
            s.append((x, y - 1))

    @staticmethod
    def scanline_fill(surface: pg.Surface, /, points: list[tuple[int,int]], color: tuple[int,int,int]) -> None:
        # Encontra Y mínimo e máximo
        ys = [p[1] for p in points]
        y_min = min(ys)
        y_max = max(ys)

        n = len(points)

        for y in range(y_min, y_max):
            intersecoes_x = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]

                # Ignora arestas horizontais
                if y0 == y1:
                    continue

                # Garante y0 < y1
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0

                # Regra Ymin ≤ y < Ymax
                if y < y0 or y >= y1:
                    continue

                # Calcula interseção
                x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                intersecoes_x.append(x)

            # Ordena interseções
            intersecoes_x.sort()

            # Preenche entre pares
            for i in range(0, len(intersecoes_x), 2):
                if i + 1 < len(intersecoes_x):
                    x_inicio = int(round(intersecoes_x[i]))
                    x_fim = int(round(intersecoes_x[i + 1]))

                    for x in range(x_inicio, x_fim + 1):
                        set_pixel(surface, x, y, color)

    @staticmethod
    def interpolate_color(color1, color2, t):
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))

        return r, g, b
    @staticmethod
    def scanline_fill_gradiente(surface: pg.Surface, /, points, colors):
        # Encontra Y mínimo e máximo
        ys = [p[1] for p in points]
        y_min = min(ys)
        y_max = max(ys)

        n = len(points)

        for y in range(y_min, y_max):
            intersecoes_x = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]

                c0 = colors[i]
                c1 = colors[(i + 1) % n]

                # Ignora arestas horizontais
                if y0 == y1:
                    continue

                # Garante y0 < y1
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    c0, c1 = c1, c0

                # Regra Ymin ≤ y < Ymax
                if y < y0 or y >= y1:
                    continue

                t = (y - y0) / (y1 - y0)

                # Calcula interseção e cor
                x = x0 + t * (x1 - x0)
                cor_y = Painter.interpolate_color(c0, c1, t)
                intersecoes_x.append((x, cor_y))

            # Ordena interseções
            intersecoes_x.sort(key=lambda p: p[0])

            # Preenche entre pares
            for i in range(0, len(intersecoes_x), 2):
                if i + 1 < len(intersecoes_x):
                    x_ini, cor_ini = intersecoes_x[i]
                    x_fim, cor_fim = intersecoes_x[i + 1]

                    if x_fim == x_ini:
                        continue

                    for x in range(int(x_ini), int(x_fim) + 1):
                        t = (x - x_ini) / (x_fim - x_ini)
                        cor = Painter.interpolate_color(cor_ini, cor_fim, t)
                        set_pixel(surface, x, y, cor)
    @staticmethod
    def fill_circle_gradient(surface: pg.Surface, center, radius, color1, color2):
        cx, cy = center

        for y in range(cy - radius, cy + radius + 1):
            dy = y - cy

            dx = math.sqrt(radius ** 2 - dy ** 2)

            x1 = round(cx - dx)
            x2 = round(cx + dx)

            for x in range(x1, x2 + 1):
                # posição relativa do pixel dentro da scanline
                t = (x - x1) / (x2 - x1)

                color = Painter.interpolate_color(color1, color2, t)

                set_pixel(surface, x, y, color)
