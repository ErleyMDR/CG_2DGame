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


def clipped_line(surface, p0, p1, window, color, width=1):
    ok, x0, y0, x1, y1 = cohen_sutherland(*p0, *p1, *window)
    if ok:
        draw.Rasterizer.line(
            surface,
            (round(x0), round(y0)),
            (round(x1), round(y1)),
            color, width
        )