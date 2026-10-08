import engine.draw as draw
import pygame as pg

# =============================
# DIMENSIONS
# =============================
DECK_FULL = (320, 310)                       # roda completa (geometria)
DECK_SURFACE = (390, DECK_FULL[1] // 2 + 1)  # só a metade superior
HPBAR_SURFACE = (285, 40)
ENEMYHPBAR_SURFACE = (380, 15)

# =============================
# COLORS
# =============================
GRAY_BORDER = (152, 152, 152)
GRAY_INTERIOR = (100, 89, 89)
NOTSOWHITE = (240, 240, 240)
HP_GREEN = (45, 240, 60)
HP_BG = (60, 25, 25)


def _fill_rect(s: pg.Surface, x0: int, y0: int, x1: int, y1: int, color) -> None:
    """Preenche os pixels x0..x1-1 e y0..y1-1 (x1 e y1 exclusivos)."""
    if x1 <= x0 or y1 <= y0:
        return
    pts = [(x0, y0), (x1 - 1, y0), (x1 - 1, y1), (x0, y1)]
    draw.Painter.scanline_fill(s, pts, color=color)


class Hud:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.deck_bg = self._rasterize_deck_background()

        self._player_ratio = None
        self._enemy_ratio = None
        self.player_hp = None
        self.enemy_hp = None
        self._refresh_bars()

    # ---------------------------------------------------------
    # RODA DO DECK (fundo estático, só a metade superior)
    # ---------------------------------------------------------
    def _rasterize_deck_background(self) -> pg.Surface:
        w, h = DECK_FULL
        cx, cy = w // 2, h // 2
        f = 40
        bw = 2

        s = pg.Surface(DECK_SURFACE, pg.SRCALPHA)   # transparente

        draw.Rasterizer.ellipse(
            s, (cx, cy), cx - 10, cy - 10,
            color=GRAY_BORDER, border_width=5, fill=True,
            fill_color=GRAY_INTERIOR)

        draw.Rasterizer.circle(
            s, (cx, cy), (cy - 10) // 2,
            color=GRAY_BORDER, border_width=2, fill_color=GRAY_INTERIOR)

        p1 = [
            (cx - (cx // 2) - bw, f), (cx - (cx // 2) + bw, f),
            (cx + (cx // 2) - bw, h - f), (cx + (cx // 2) + bw, h - f)
        ]
        p2 = [
            (cx + (cx // 2) - bw, f), (cx + (cx // 2) + bw, f),
            (cx - (cx // 2) - bw, h - f), (cx - (cx // 2) + bw, h - f)
        ]
        draw.Painter.scanline_fill(s, p1, color=GRAY_BORDER)
        draw.Painter.scanline_fill(s, p2, color=GRAY_BORDER)

        # diâmetro: fica na última linha da superfície (base da meia-roda)
        draw.Rasterizer.line(s, (10, cy), (w - 10, cy), color=GRAY_BORDER)

        return s

    # ---------------------------------------------------------
    # BARRAS DE HP
    # ---------------------------------------------------------
    @staticmethod
    def _ratio(entity) -> float:
        if entity is None or entity.MAX_HP <= 0:
            return 1.0
        return max(0.0, min(1.0, entity.HP / entity.MAX_HP))

    @staticmethod
    def _make_bar(size: tuple[int, int], bw: int, ratio: float) -> pg.Surface:
        w, h = size
        s = pg.Surface(size)

        _fill_rect(s, 0, 0, w, h, NOTSOWHITE)               # borda
        _fill_rect(s, bw, bw, w - bw, h - bw, HP_BG)        # fundo (vida perdida)

        fill_w = round((w - 2 * bw) * ratio)
        _fill_rect(s, bw, bw, bw + fill_w, h - bw, HP_GREEN)  # vida atual
        return s

    def _refresh_bars(self) -> None:
        """Só re-rasteriza quando a proporção de HP mudou."""
        pr = self._ratio(self.player)
        if pr != self._player_ratio:
            self._player_ratio = pr
            self.player_hp = self._make_bar(HPBAR_SURFACE, 3, pr)

        er = self._ratio(self.enemy)
        if er != self._enemy_ratio:
            self._enemy_ratio = er
            self.enemy_hp = self._make_bar(ENEMYHPBAR_SURFACE, 2, er)

    # ---------------------------------------------------------
    # DESENHO
    # ---------------------------------------------------------
    def draw(self, screen: pg.Surface) -> None:
        self._refresh_bars()

        sw, sh = screen.get_size()
        dw, dh = self.deck_bg.get_size()

        # meia-roda colada na base da tela, centralizada
        x = (sw - dw) // 2 + 30
        y = sh - dh
        screen.blit(self.deck_bg, (x, y))

        # cartas desenhadas por cima, a cada frame
        if self.player is not None and self.player.deck is not None:
            self.player.deck.draw_visible(
                screen,
                (x + dw // 2, y + dh - 75)
            )

        screen.blit(self.player_hp, (80, sh - 80))
        screen.blit(self.enemy_hp, (80, 80))