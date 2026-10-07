import math
from engine.core import *

SQRTOF3: float | int = math.sqrt(3)

class Rasterizer:

    @staticmethod
    def line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int], width: int=1, method: str='bresenham'):
        draw_line(surface, start_point, end_point, color, width, method)

    @staticmethod
    def polygon(surface: pg.Surface, /, points: list[tuple[int,int]], color: tuple[int,int,int], *, fill: bool=False, fill_color: tuple[int,int,int]=None):
        draw_polygon(
            surface,
            points,
            color
        )
        if fill:
            if fill_color is None: Painter.scanline_fill(surface, points=points, color=color)
            else: Painter.scanline_fill(surface, points=points, color=fill_color)

    @staticmethod
    def curved_line(surface: pg.Surface, /, start_point: tuple[int,int], end_point: tuple[int,int], color: tuple[int,int,int]) -> None:
        ...

    @staticmethod
    def rectangle(surface: pg.Surface, center, width, height, color, *,
                  border_width: int=1, fill: bool=False, fill_color: tuple[int,int,int]=None):
        w, h = width // 2, height // 2
        v = [
            (center[0] - w, center[1] - h),
            (center[0] + w, center[1] - h),
            (center[0] + w, center[1] + h),
            (center[0] - w, center[1] + h)
        ]
        if fill:
            interior = color if fill_color is None else fill_color
            Painter.scanline_fill(
                surface,
                points=v,
                color=color
            )

            v = [
                (v[0][0] + border_width, v[0][1] + border_width),
                (v[1][0] - border_width, v[1][1] + border_width),
                (v[2][0] - border_width, v[2][1] - border_width),
                (v[3][0] + border_width, v[3][1] - border_width)
            ]
            Painter.scanline_fill(
                surface,
                points=v,
                color=interior
            )

        else:
            draw_polygon(surface, points=v, color=color)

        return v

    @staticmethod
    def square(surface: pg.Surface, center, size, color, *, fill: bool=False):
       return Rasterizer.rectangle(surface, center, size, size, color, fill=fill)

    @staticmethod
    def triangle(surface: pg.Surface, center, height, side_l, color, border_width: int=1):
        if (side_l * 2) / SQRTOF3 < height:
            raise ArgumentError
        hh = height // 2
        hs = side_l // 2
        v = [
            (center[0], center[1] - hh),
            (center[0] - hs, center[1] + hh),
            (center[0] + hs, center[1] + hh),
        ]

        for i in range(border_width):
            v = [(x - i, y - i) for x, y in v]
            draw_polygon(
                surface,
                v,
                color
            )
        return v

    @staticmethod
    def circle(surface: pg.Surface, center, radius, color, *, border_width: int=1, fill: bool=False, fill_color: tuple[int,int,int]=None):
        if fill:
            interior_color = color if fill_color is None else fill_color

            Painter.fill_circle(
                surface,
                center,
                radius,
                color
            )

            Painter.fill_circle(
                surface,
                center,
                radius - border_width,
                interior_color
            )

        else:
            draw_circle(
                surface,
                center,
                radius,
                color
            )

    @staticmethod
    def ellipse(surface: pg.Surface, /, center: tuple[int,int], x_radius: int, y_radius: int, color: tuple[int,int,int], *,
                border_width: int=1, fill: bool=False, fill_color: tuple[int,int,int]=None):
        if fill:
            interior_color = color if fill_color is None else fill_color
            Painter.fill_ellipse(
                surface,
                center,
                x_radius,
                y_radius,
                color
            )

            Painter.fill_ellipse(
                surface,
                center,
                x_radius - border_width,
                y_radius - border_width,
                interior_color
            )

        else:
            draw_ellipse(
                surface,
                center,
                x_radius,
                y_radius,
                color
            )

    @staticmethod
    def half_cirle(surface: pg.Surface, center, radius, color, direction: str='north', fill: bool=False):
        ...

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
    def fill_circle(surface, center, radius, color):
        cx, cy = center

        for y in range(cy - radius, cy + radius + 1):
            dy = y - cy

            dx = math.sqrt(radius * radius - dy * dy)

            x1 = round(cx - dx)
            x2 = round(cx + dx)

            for x in range(x1, x2 + 1):
                set_pixel(surface, x, y, color)

    @staticmethod
    def fill_ellipse(surface, center, rx, ry, color):
        cx, cy = center

        for y in range(cy - ry, cy + ry + 1):
            dy = y - cy

            dx = rx * math.sqrt(
                1 - (dy * dy) / (ry * ry)
            )

            x1 = round(cx - dx)
            x2 = round(cx + dx)

            for x in range(x1, x2 + 1):
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

    @staticmethod
    def fill_ellipse_gradient(surface, center, rx, ry, color1, color2):
        cx, cy = center

        for y in range(cy - ry, cy + ry + 1):
            dy = y - cy

            dx = rx * math.sqrt(
                1 - (dy * dy) / (ry * ry)
            )

            x1 = round(cx - dx)
            x2 = round(cx + dx)

            for x in range(x1, x2 + 1):
                t = (x - x1) / (x2 - x1)

                color = Painter.interpolate_color(color1, color2, t)

                set_pixel(surface, x, y, color)

    @staticmethod
    def scanline_texture(surface: pg.Surface, /, points, uvs, texture_img):
        n = len(points)
        tex_w = texture_img.get_width()
        tex_h = texture_img.get_height()
        ys = [p[1] for p in points]
        y_min = int(min(ys))
        y_max = int(max(ys))

        for y in range(y_min, y_max):
            intersecoes = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                u0, v0 = uvs[i]
                u1, v1 = uvs[(i + 1) % n]

                if y0 == y1:
                    continue

                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    u0, v0, u1, v1 = u1, v1, u0, v0

                if y < y0 or y >= y1:
                    continue

                t = (y - y0) / (y1 - y0)
                x = x0 + t * (x1 - x0)
                u = u0 + t * (u1 - u0)
                v = v0 + t * (v1 - v0)
                intersecoes.append((x, u, v))

            intersecoes.sort(key=lambda item: item[0])

            for i in range(0, len(intersecoes), 2):
                if i + 1 >= len(intersecoes):
                    continue

                x_ini, u_ini, v_ini = intersecoes[i]
                x_fim, u_fim, v_fim = intersecoes[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    u = u_ini + t * (u_fim - u_ini)
                    v = v_ini + t * (v_fim - v_ini)

                    tx = int(u * (tex_w - 1))
                    ty = int(v * (tex_h - 1))

                    if 0 <= tx < tex_w and 0 <= ty < tex_h:
                        cor = texture_img.get_at((tx, ty))
                        set_pixel(surface, x, y, cor)