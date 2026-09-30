import pygame as pg
import matrix_operations as mat_ops

def _calculate_aabb(points: list[tuple[int,int]]):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    return min(xs), min(ys), max(xs), max(ys)

def aabb_collision(a, b):
    ...