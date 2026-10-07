import pygame as pg

from engine import draw


WIDTH = 1820
HEIGHT = 920

CARD_FONT = "assets/font/PressStart2P-Regular.ttf"

YELLOW = (255, 222, 89)
LIGHT_BLUE = (112, 96, 207)

BG_TOP = (21, 11, 83)
BG_BOTTOM = (111, 93, 178)


class Menu:

    def __init__(self):
        self.menu_screen = self._rasterize()

    def _rasterize(self) -> pg.Surface:
        s = pg.Surface((WIDTH, HEIGHT))

        # ==========================================
        # FUNDO - GRADIENTE VERTICAL
        # ==========================================

        background = [
            (0, 0),
            (WIDTH, 0),
            (WIDTH, HEIGHT),
            (0, HEIGHT)
        ]

        background_colors = [
            BG_TOP,
            BG_TOP,
            BG_BOTTOM,
            BG_BOTTOM
        ]

        draw.Painter.scanline_fill_gradiente(
            s,
            background,
            background_colors
        )

        # ==========================================
        # TÍTULO
        # ==========================================

        title_font = pg.font.Font(CARD_FONT, 40)

        title = title_font.render(
            "REAL TIME CARD BATTLE",
            False,
            YELLOW
        )

        title_x = (WIDTH - title.get_width()) // 2
        title_y = 105

        s.blit(title, (title_x, title_y))

        # ==========================================
        # BOTÕES
        # ==========================================

        button_width = 340
        button_height = 95
        border_width = 7

        button_x = WIDTH // 2
        button_positions = [
            320,  # INICIAR
            472,  # CONTROLES
            650   # SAIR
        ]

        for y in button_positions:
            draw.Rasterizer.rectangle(
                s,
                (button_x, y),
                button_width,
                button_height,
                color=YELLOW,
                border_width=border_width,
                fill=True,
                fill_color=LIGHT_BLUE
            )

        # ==========================================
        # TEXTOS DOS BOTÕES
        # ==========================================

        button_font = pg.font.Font(CARD_FONT, 24)

        self._draw_centered_text(
            s,
            "INICIAR",
            button_font,
            button_x,
            button_positions[0],
            YELLOW
        )

        self._draw_centered_text(
            s,
            "CONTROLES",
            button_font,
            button_x,
            button_positions[1],
            YELLOW
        )

        self._draw_centered_text(
            s,
            "SAIR",
            button_font,
            button_x,
            button_positions[2],
            YELLOW
        )

        return s

    @staticmethod
    def _draw_centered_text(
            surface: pg.Surface,
            text: str,
            font: pg.font.Font,
            x: int,
            y: int,
            color: tuple[int, int, int]
    ) -> None:

        rendered = font.render(
            text,
            False,
            color
        )

        pos = (
            x - rendered.get_width() // 2,
            y - rendered.get_height() // 2
        )

        surface.blit(rendered, pos)

    def show(self, screen: pg.Surface) -> None:
        screen.blit(self.menu_screen, (0, 0))
