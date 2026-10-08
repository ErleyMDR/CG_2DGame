from engine.core import draw_line

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def bounds(
        x, y,
        xmin, ymin,
        xmax, ymax
):

    codigo = INSIDE

    if x < xmin:
        codigo |= LEFT

    elif x > xmax:
        codigo |= RIGHT

    # No Pygame, Y cresce para baixo
    if y < ymin:
        codigo |= TOP

    elif y > ymax:
        codigo |= BOTTOM

    return codigo


def cohen_sutherland(
        x0, y0,
        x1, y1,
        xmin, ymin,
        xmax, ymax
):

    c0 = bounds(
        x0, y0,
        xmin, ymin,
        xmax, ymax
    )

    c1 = bounds(
        x1, y1,
        xmin, ymin,
        xmax, ymax
    )

    while True:

        # ---------------------------------------------
        # ACEITAÇÃO TRIVIAL
        # Os dois pontos estão dentro
        # ---------------------------------------------

        if not (c0 | c1):

            return (
                True,
                x0, y0,
                x1, y1
            )

        # ---------------------------------------------
        # REJEIÇÃO TRIVIAL
        # Os dois pontos estão fora do mesmo lado
        # ---------------------------------------------

        if c0 & c1:

            return (
                False,
                0, 0,
                0, 0
            )

        # Escolhe uma extremidade externa
        c_out = c0 if c0 else c1

        # ---------------------------------------------
        # INTERSEÇÃO COM O TOPO
        # ---------------------------------------------

        if c_out & TOP:

            x = (
                    x0
                    + (x1 - x0)
                    * (ymin - y0)
                    / (y1 - y0)
            )

            y = ymin

        # ---------------------------------------------
        # INTERSEÇÃO COM A BASE
        # ---------------------------------------------

        elif c_out & BOTTOM:

            x = (
                    x0
                    + (x1 - x0)
                    * (ymax - y0)
                    / (y1 - y0)
            )

            y = ymax

        # ---------------------------------------------
        # INTERSEÇÃO COM A DIREITA
        # ---------------------------------------------

        elif c_out & RIGHT:

            y = (
                    y0
                    + (y1 - y0)
                    * (xmax - x0)
                    / (x1 - x0)
            )

            x = xmax

        # ---------------------------------------------
        # INTERSEÇÃO COM A ESQUERDA
        # ---------------------------------------------

        else:

            y = (
                    y0
                    + (y1 - y0)
                    * (xmin - x0)
                    / (x1 - x0)
            )

            x = xmin

        # ---------------------------------------------
        # Substitui o ponto externo pela interseção
        # ---------------------------------------------

        if c_out == c0:

            x0 = x
            y0 = y

            c0 = bounds(
                x0, y0,
                xmin, ymin,
                xmax, ymax
            )

        else:

            x1 = x
            y1 = y

            c1 = bounds(
                x1, y1,
                xmin, ymin,
                xmax, ymax
            )


def draw_clipped_line(surface, p0, p1, window, color, width=1):
    """
    Desenha o segmento p0->p1 recortado por `window` = (xmin, ymin, xmax, ymax).
    Para width > 1, cada linha paralela é recortada separadamente, então o
    corte fica rente à borda da janela.
    """
    x0, y0 = p0
    x1, y1 = p1

    steep = abs(y1 - y0) > abs(x1 - x0)

    for i in range(width):
        off = i - (width - 1) // 2

        # Retas íngremes engrossam na horizontal, as demais na vertical.
        # Deslocar sempre em pixels inteiros evita buracos entre as linhas.
        ox, oy = (off, 0) if steep else (0, off)

        ok, cx0, cy0, cx1, cy1 = cohen_sutherland(
            x0 + ox, y0 + oy,
            x1 + ox, y1 + oy,
            *window
        )

        if ok:
            draw_line(
                surface,
                (round(cx0), round(cy0)),
                (round(cx1), round(cy1)),
                color
            )