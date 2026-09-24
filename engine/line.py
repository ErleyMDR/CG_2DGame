import pygame as pg

class Line:
    def __init__(self, start_point:tuple[int, int], end_point:tuple[int, int], /, *, raster: bool=False, method: str='bresenham'):
        self.start_x: int = start_point[0]
        self.start_y: int = start_point[1]
        self.end_x: int = end_point[0]
        self.end_y: int = end_point[1]
        self._cache: list[tuple[int, int]] = []

        if raster:
            match method:
                case 'dda':
                    self._cache = self._dda()
                case 'bresenham':
                    self._cache = self._bresenham()
                case _:
                    self._cache = self._bresenham()

    def _dda(self) -> list[tuple[int, int]]:
        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        raster = []

        step = max(abs(dx), abs(dy))
        dx = dx / step
        dy = dy / step
        x = self.start_x
        y = self.start_y
        i = 0

        while i <= step:
            raster.append((round(x), round(y)))
            x += dx
            y += dy
            i += 1

        return raster


    def _bresenham(self) -> list[tuple[int, int]]:
        raster = []
        def bres_low(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            yi = 1
            if dy < 0:
                yi = -1
                dy = -dy
            d = (2 * dy) - dx
            y = y0
            for x in range(x0, x1 + 1):
                raster.append((x, y))
                if d > 0:
                    y += yi
                    d = d + (2 * (dy - dx))
                else:
                    d += (2 * dy)

        def bres_high(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            xi = 1
            if dx < 0:
                xi = -1
                dx = -dx
            d = (2 * dx) - dy
            x = x0

            for y in range(y0, y1 + 1):
                raster.append((x, y))
                if d > 0:
                    x += xi
                    d = d + (2 * (dx - dx))
                else:
                    d += (2 * dx)

        if abs(self.end_y - self.start_y) > abs(self.end_x - self.start_x):
            if self.start_x < self.end_x:
                bres_low(self.start_x, self.start_y, self.end_x, self.end_y)
            else:
                bres_low(self.end_x, self.end_y, self.start_x, self.start_y)
        else:
            if self.start_y < self.end_y:
                bres_high(self.start_x, self.start_y, self.end_x, self.end_y)
            else:
                bres_high(self.end_x, self.end_y, self.start_x, self.start_y)

        return raster



    def draw(self, surface: pg.Surface, *, color: tuple[int,int,int]) -> None:
        if not self._cache: self._bresenham()
        for x, y in self._cache:
            surface.set_at((x, y), color)

    @property
    def cache(self):
        return self._cache