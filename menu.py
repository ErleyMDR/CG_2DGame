import pygame as pg
from engine import draw

WIDTH = 1820
HEIGHT = 920

CARD_FONT = "assets/font/PressStart2P-Regular.ttf"

YELLOW = (255, 222, 89)
LIGHT_BLUE = (112, 96, 207)
WHITE = (255, 255, 255)

BG_TOP = (21, 11, 83)
BG_BOTTOM = (111, 93, 178)


class Menu:

    def __init__(self):
        self.state = "MAIN"

        self.button_width = 340
        self.button_height = 95
        self.button_x = WIDTH // 2

        self.y_iniciar = 320
        self.y_controles = 472
        self.y_sair = 650
        self.y_voltar = 750

        self.menu_screen = self._rasterize_main_menu()
        self.controls_screen = self._rasterize_controls_screen()

    def _apply_background(self, surface: pg.Surface):
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
        draw.Painter.scanline_fill_gradiente(surface, background, background_colors)

    def _draw_button(self, surface: pg.Surface, center_x: int, center_y: int):
        """Desenha o botão diretamente na posição central (center_x, center_y)."""
        draw.Rasterizer.rectangle(
            surface,
            (center_x, center_y),
            self.button_width,
            self.button_height,
            color=YELLOW,
            border_width=7,
            fill=True,
            fill_color=LIGHT_BLUE
        )

    def _rasterize_main_menu(self) -> pg.Surface:
        s = pg.Surface((WIDTH, HEIGHT))
        self._apply_background(s)

        # TÍTULO
        title_font = pg.font.Font(CARD_FONT, 40)
        title = title_font.render("REAL TIME CARD BATTLE", False, YELLOW)
        s.blit(title, ((WIDTH - title.get_width()) // 2, 105))

        # BOTÕES
        button_positions = [self.y_iniciar, self.y_controles, self.y_sair]
        for y in button_positions:
            self._draw_button(s, self.button_x, y)

        # TEXTOS DOS BOTÕES
        button_font = pg.font.Font(CARD_FONT, 24)
        self._draw_centered_text(s, "INICIAR", button_font, self.button_x, self.y_iniciar, YELLOW)
        self._draw_centered_text(s, "CONTROLES", button_font, self.button_x, self.y_controles, YELLOW)
        self._draw_centered_text(s, "SAIR", button_font, self.button_x, self.y_sair, YELLOW)

        return s

    def _rasterize_controls_screen(self) -> pg.Surface:
        s = pg.Surface((WIDTH, HEIGHT))
        self._apply_background(s)

        # TÍTULO CONTROLES
        title_font = pg.font.Font(CARD_FONT, 40)
        title = title_font.render("CONTROLES", False, YELLOW)
        s.blit(title, ((WIDTH - title.get_width()) // 2, 105))

        # INSTRUÇÕES
        info_font = pg.font.Font(CARD_FONT, 20)
        controls_info = [
            "W, A, S, D - Mover Personagem",
            "ESPAÇO - Selecionar / Usar Carta",
            "ESC - Voltar / Pausar"
        ]

        start_y = 280
        for line in controls_info:
            self._draw_centered_text(s, line, info_font, WIDTH // 2, start_y, WHITE)
            start_y += 70

        # BOTÃO VOLTAR
        self._draw_button(s, self.button_x, self.y_voltar)

        button_font = pg.font.Font(CARD_FONT, 24)
        self._draw_centered_text(s, "VOLTAR", button_font, self.button_x, self.y_voltar, YELLOW)

        return s

    @staticmethod
    def _draw_centered_text(surface: pg.Surface, text: str, font: pg.font.Font, x: int, y: int, color: tuple[int, int, int]) -> None:
        rendered = font.render(text, False, color)
        pos = (x - rendered.get_width() // 2, y - rendered.get_height() // 2)
        surface.blit(rendered, pos)

    @staticmethod
    def _is_point_inside_button(px: int, py: int, center_x: int, center_y: int, width: int, height: int) -> bool:
        """Verifica se o ponto (px, py) do mouse está dentro da caixa centralizada em (center_x, center_y)."""
        half_w = width // 2
        half_h = height // 2
        return (center_x - half_w <= px <= center_x + half_w) and (center_y - half_h <= py <= center_y + half_h)

    def handle_event(self, event: pg.event.Event) -> str | None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if self.state == "MAIN":
                if self._is_point_inside_button(mx, my, self.button_x, self.y_iniciar, self.button_width, self.button_height):
                    return "PLAYING"

                elif self._is_point_inside_button(mx, my, self.button_x, self.y_controles, self.button_width, self.button_height):
                    self.state = "CONTROLS"

                elif self._is_point_inside_button(mx, my, self.button_x, self.y_sair, self.button_width, self.button_height):
                    return "QUIT"

            elif self.state == "CONTROLS":
                if self._is_point_inside_button(mx, my, self.button_x, self.y_voltar, self.button_width, self.button_height):
                    self.state = "MAIN"

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and self.state == "CONTROLS":
                self.state = "MAIN"

        return None

    def show(self, screen: pg.Surface) -> None:
        if self.state == "MAIN":
            screen.blit(self.menu_screen, (0, 0))
        elif self.state == "CONTROLS":
            screen.blit(self.controls_screen, (0, 0))