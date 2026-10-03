import math

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