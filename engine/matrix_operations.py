import math

from engine.core import set_pixel_alpha
from engine.draw import pg

def eye():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def translation(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def scale(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotation(theta):
    s = math.sin(theta)
    c = math.cos(theta)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ]

def mat_mult(a, b):
    result = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += a[i][k] * b[k][j]

    return result


def aplica_transformacao(m, pontos):
    novos = []
    for x, y in pontos:

        v = [x, y, 1]

        x_novo = (
                m[0][0] * v[0]
                + m[0][1] * v[1]
                + m[0][2]
        )

        y_novo = (
                m[1][0] * v[0]
                + m[1][1] * v[1]
                + m[1][2]
        )

        novos.append(
            (x_novo, y_novo)
        )

    return novos

def scale_surface(
        surface: pg.Surface,
        size: tuple[int, int]
) -> pg.Surface:

    dst_w, dst_h = size
    src_w, src_h = surface.get_size()

    result = pg.Surface(
        (dst_w, dst_h),
        pg.SRCALPHA
    )

    sx = src_w / dst_w
    sy = src_h / dst_h

    for y in range(dst_h):
        for x in range(dst_w):

            src_x = round(x * sx)
            src_y = round(y * sy)

            if (
                    0 <= src_x < src_w
                    and 0 <= src_y < src_h
            ):
                c = surface.get_at((src_x, src_y))

                set_pixel_alpha(
                    result,
                    x,
                    y,
                    (c.r, c.g, c.b, c.a)
                )

    return result

def surface_bounds(surface: pg.Surface, min_alpha: int = 1) -> tuple[int, int, int, int]:
    """Retorna (x, y, w, h) da região com alpha >= min_alpha."""
    w, h = surface.get_size()
    left, top, right, bottom = w, h, -1, -1

    for y in range(h):
        for x in range(w):
            if surface.get_at((x, y)).a >= min_alpha:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y

    return left, top, right - left + 1, bottom - top + 1


def flip_surface_horizontal(surface: pg.Surface) -> pg.Surface:
    w, h = surface.get_size()
    result = pg.Surface((w, h), pg.SRCALPHA)

    for y in range(h):
        for x in range(w):
            c = surface.get_at((w - 1 - x, y))
            set_pixel_alpha(result, x, y, (c.r, c.g, c.b, c.a))

    return result

def rotate_surface(surface: pg.Surface, theta: float, canvas: int) -> pg.Surface:
    """
    Rotaciona 'surface' em torno do seu centro por 'theta' radianos
    (positivo = sentido horário na tela, pois Y cresce para baixo).
    O resultado é uma Surface quadrada 'canvas' x 'canvas'.
    """
    src_w, src_h = surface.get_size()

    scx, scy = (src_w - 1) / 2, (src_h - 1) / 2
    dcx = dcy = (canvas - 1) / 2

    # destino -> origem:  T(src_c) · R(-theta) · T(-dst_c)
    m = mat_mult(
        translation(scx, scy),
        mat_mult(rotation(-theta), translation(-dcx, -dcy))
    )

    result = pg.Surface((canvas, canvas), pg.SRCALPHA)

    # só percorre a caixa que o sprite rotacionado ocupa
    c, s = abs(math.cos(theta)), abs(math.sin(theta))
    half_w = (src_w * c + src_h * s) / 2 + 1
    half_h = (src_w * s + src_h * c) / 2 + 1

    for y in range(max(0, int(dcy - half_h)), min(canvas, int(dcy + half_h) + 2)):
        for x in range(max(0, int(dcx - half_w)), min(canvas, int(dcx + half_w) + 2)):

            sx = round(m[0][0] * x + m[0][1] * y + m[0][2])
            sy = round(m[1][0] * x + m[1][1] * y + m[1][2])

            if 0 <= sx < src_w and 0 <= sy < src_h:
                p = surface.get_at((sx, sy))
                if p.a > 0:
                    set_pixel_alpha(result, x, y, (p.r, p.g, p.b, p.a))

    return result