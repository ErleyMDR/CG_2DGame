from engine import draw

def calcular_aabb(pontos):
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    return min(xs), min(ys), max(xs), max(ys)

def colisao_aabb(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b

    return (
            ax1 < bx2 and
            ax2 > bx1 and
            ay1 < by2 and
            ay2 > by1
    )

def desenhar_aabb(superficie, aabb, cor):
    x1, y1, x2, y2 = aabb

    pontos = [
        (x1, y1),
        (x2, y1),
        (x2, y2),
        (x1, y2)
    ]

    draw.Rasterizer.polygon(superficie, pontos, cor)