import engine.draw as draw
import pygame as pg

# =============================
# DIMENSIONS & COORDINATES
# =============================
DECK_SURFACE = (390, 380)
HPBAR_SURFACE = (285, 40)
ENEMYHPBAR_SURFACE = (380, 15)

# =============================
# COLORS
# =============================
GRAY_BORDER = (152, 152, 152)
GRAY_INTERIOR = (100, 89, 89)
NOTSOWHITE = (240, 240, 240)
HP_GREEN = (45, 240, 60)

class Hud:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.player_deck = self.draw_player_deck()
        self.player_hp = self.draw_hpbar()
        self.enemy_deck = None
        self.enemy_hp = self.draw_enemy_hpbar()

    def draw_player_deck(self) -> pg.Surface:
        s = pg.Surface(DECK_SURFACE)
        cx, cy = s.get_width()//2, s.get_height()//2
        f = 40
        draw.Rasterizer.ellipse(
            s, (cx, cy), cx - 10, cy - 10,
            color=GRAY_BORDER, border_width=5, fill=True, fill_color=GRAY_INTERIOR)
        draw.Rasterizer.circle(s, (cx, cy), (cy - 10)//2, color=GRAY_BORDER, border_width=2, fill_color=GRAY_INTERIOR)

        bw = 2
        p1 = [
            (cx - (cx//2)-bw, f), (cx - (cx//2)+bw, f),
            (cx + (cx//2)-bw, s.get_height() - f), (cx + (cx//2)+bw, s.get_height() - f)
        ]
        p2 = [
            (cx + (cx//2)-bw, f), (cx + (cx//2)+bw, f),
            (cx - (cx//2)-bw, s.get_height() - f), (cx - (cx//2)+bw, s.get_height() - f)
        ]
        draw.Painter.scanline_fill(s, p1, color=GRAY_BORDER)
        draw.Painter.scanline_fill(s, p2, color=GRAY_BORDER)

        draw.Rasterizer.line(s, (10, cy), (s.get_width()-10, cy), color=GRAY_BORDER)

        self.player.deck
        return s

    def draw_hpbar(self) -> pg.Surface:
        s = pg.Surface(HPBAR_SURFACE)
        x, y = s.get_width()//2, s.get_height()//2
        bw = 3
        draw.Rasterizer.rectangle(
            s, (x, y), s.get_width(), s.get_height(),
            border_width=bw,color=NOTSOWHITE, fill=True, fill_color=HP_GREEN)
        return s

    def draw_enemy_hpbar(self) -> pg.Surface:
        s = pg.Surface(ENEMYHPBAR_SURFACE)
        x, y = s.get_width()//2, s.get_height()//2
        bw = 2
        draw.Rasterizer.rectangle(
            s, (x, y), s.get_width(), s.get_height(),
            border_width=bw,color=NOTSOWHITE, fill=True, fill_color=HP_GREEN)
        return s

    def draw_enemy_deck(self) -> pg.Surface:
        ...

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.player_deck, (screen.get_width()//2, screen.get_height()//2))
        screen.blit(self.player_hp, (80, screen.get_height() - 80))
        screen.blit(self.enemy_hp, (80, 80))