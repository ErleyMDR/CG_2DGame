import math
import pygame as pg
from engine.draw import Rasterizer, Painter  # Ajuste a importação se necessário

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (215, 215, 40)
RED = (200, 0, 0)

def draw_boot_screen(screen: pg.Surface) -> None:
    font = pg.font.SysFont('Arial', 40)
    cx = screen.get_width() // 2
    cy = screen.get_height() // 2

    # 1. Duas elipses de mesmo tamanho, perpendiculares entre si no centro
    rx, ry = 420, 210
    Rasterizer.ellipse(screen, (cx, cy), rx, ry, WHITE)
    Rasterizer.ellipse(screen, (cx, cy), ry, rx, WHITE)

    # Parametrização do círculo e retas
    circle_radius = 80
    line_length = 110  # Maior que o raio para atravessar o círculo

    # 2. Duas retas a 45° e 135° atravessando o círculo (Desenhadas ANTES do círculo)
    cos45 = math.cos(math.radians(45))
    sin45 = math.sin(math.radians(45))

    dx = int(line_length * cos45)
    dy = int(line_length * sin45)

    # Reta a 45° (diagonal principal)
    line1_start = (cx - dx, cy + dy)
    line1_end = (cx + dx, cy - dy)
    Rasterizer.line(screen, line1_start, line1_end, RED)

    # Reta a 135° (diagonal secundária)
    line2_start = (cx - dx, cy - dy)
    line2_end = (cx + dx, cy + dy)
    Rasterizer.line(screen, line2_start, line2_end, RED)

    # 3. Círculo delimitador (Desenhado DEPOIS das retas para selar a borda)
    Rasterizer.circle(screen, (cx, cy), circle_radius, WHITE)

    # 4. Preenchimento azul com flood_fill dentro do círculo
    # O ponto inicial (cx + 10, cy) evita colidir com as linhas de 45°/135°
    Painter.flood_fill(screen, cx + 10, cy, BLUE, WHITE)

    cg = font.render('CG', True, BLACK)
    screen.blit(cg, (cx - 20, cy - 18))