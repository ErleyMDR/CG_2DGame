import engine.draw as draw
import pygame as pg

HUD_DIMENSIONS = (135, 390)
GRAY_BORDER = (152, 152, 152)
GRAY_INTERIOR = (100, 89, 89)

class Hud:
    def __init__(self):
        pass

    def draw_player_deck(self) -> pg.Surface:
        s = pg.Surface(HUD_DIMENSIONS)
        draw.Rasterizer.ellipse(s, (s.get_width()//2, s.get_height()//2), s.get_width()//2, s.get_height()//2, GRAY_BORDER)
        return s

    def draw_hpbar(self) -> pg.Surface:
        ...

    def draw_enemy_hpbar(self) -> pg.Surface:
        ...

    def draw_enemy_deck(self) -> pg.Surface:
        ...