from argparse import ArgumentError

import pygame as pg

from engine.line import Line

def set_pixel(surface: pg.Surface, x: int, y: int, cor: tuple[int,int,int]) -> None:
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((x, y), cor)

def line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int], width: int=1, method: str='bresenham') -> Line:
    l = Line(start_point, end_point, raster=False)
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
            l.cache.append((px, py))
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

    return l

def polygon(surface: pg.Surface, /, points: list[tuple[int,int]], color: tuple[int,int,int]) -> None:
    n = len(points)
    if n <= 2:
        raise ArgumentError

    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        line(surface, (x0, y0), (x1, y1), color, method='bresenham')

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