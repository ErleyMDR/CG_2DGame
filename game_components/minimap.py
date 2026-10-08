import pygame as pg

from engine.matrix_operations import (
    translation,
    scale,
    mat_mult,
    aplica_transformacao,
    scale_surface
)
from engine.draw import Rasterizer

MINI_SPRITE_HEIGHT = 28


class Minimap:
    def __init__(self):
        # Posição e dimensões da viewport na tela
        self.x = 1510
        self.y = 30
        self.width = 260
        self.height = 180

        # Limites da janela no mundo
        self.world_min_x = 210
        self.world_max_x = 1610
        self.world_min_y = 680
        self.world_max_y = 880

        # Matrizes mundo -> viewport
        self.matrix = self._make_matrix(self.x, self.y)   # coordenadas da tela
        self.local_matrix = self._make_matrix(0, 0)       # coordenadas da viewport

        # Cache dos mini-sprites: id(sprite) -> (sprite_original, mini_sprite)
        # Guardar o original evita que o id seja reaproveitado por outro objeto.
        self._sprite_cache = {}

        # Fundo estático, rasterizado uma única vez
        self.background = self._rasterize_background()

    # ---------------------------------------------------------
    # TRANSFORMAÇÃO MUNDO -> VIEWPORT
    # ---------------------------------------------------------
    def _make_matrix(self, offset_x: float, offset_y: float):
        sx = self.width / (self.world_max_x - self.world_min_x)
        sy = self.height / (self.world_max_y - self.world_min_y)

        return mat_mult(
            translation(offset_x, offset_y),
            mat_mult(
                scale(sx, sy),
                translation(-self.world_min_x, -self.world_min_y)
            )
        )

    def world_to_viewport(self, x, y, matrix=None):
        m = self.matrix if matrix is None else matrix
        px, py = aplica_transformacao(m, [(x, y)])[0]
        return round(px), round(py)

    def draw_world_rectangle(
            self, surface, center, width, height,
            color, fill_color, border_width=1, matrix=None
    ):
        cx, cy = center

        x1, y1 = self.world_to_viewport(
            cx - width / 2, cy - height / 2, matrix
        )
        x2, y2 = self.world_to_viewport(
            cx + width / 2, cy + height / 2, matrix
        )

        Rasterizer.rectangle(
            surface,
            center=((x1 + x2) // 2, (y1 + y2) // 2),
            width=max(1, abs(x2 - x1)),
            height=max(1, abs(y2 - y1)),
            color=color,
            border_width=border_width,
            fill=True,
            fill_color=fill_color
        )

    # ---------------------------------------------------------
    # FUNDO ESTÁTICO (executa uma vez)
    # ---------------------------------------------------------
    def _rasterize_background(self) -> pg.Surface:
        s = pg.Surface((self.width, self.height))
        m = self.local_matrix

        # Fundo da viewport
        Rasterizer.rectangle(
            s,
            center=(self.width // 2, self.height // 2),
            width=self.width,
            height=self.height,
            color=(180, 180, 190),
            border_width=3,
            fill=True,
            fill_color=(55, 55, 70)
        )

        wall_border = (175, 175, 190)
        wall_fill = (110, 110, 125)

        # Paredes laterais
        self.draw_world_rectangle(
            s, (237, 780), 54, 200, wall_border, wall_fill, matrix=m)
        self.draw_world_rectangle(
            s, (1583, 780), 54, 200, wall_border, wall_fill, matrix=m)

        # Paredes superiores
        self.draw_world_rectangle(
            s, (506, 685), 592, 11, wall_border, wall_fill, matrix=m)
        self.draw_world_rectangle(
            s, (1314, 685), 592, 11, wall_border, wall_fill, matrix=m)

        # Linha central da arena
        Rasterizer.line(
            s,
            start_point=self.world_to_viewport(264, 780, m),
            end_point=self.world_to_viewport(1556, 780, m),
            color=(110, 110, 130),
            width=2
        )

        # Elipse central da arena
        raio_x = round(
            55 * self.width /
            (self.world_max_x - self.world_min_x)
            * 1400 / 260
        )
        raio_y = round(
            40 * self.height /
            (self.world_max_y - self.world_min_y)
            * 200 / 180
        )

        Rasterizer.ellipse(
            s,
            center=self.world_to_viewport(910, 780, m),
            x_radius=raio_x,
            y_radius=raio_y,
            color=(145, 145, 165),
            border_width=2,
            fill=False
        )

        # Portão central
        self.draw_world_rectangle(
            s, (900, 686), 296, 11,
            (210, 210, 220), (155, 155, 170),
            border_width=2, matrix=m
        )

        return s.convert()   # mesmo formato da tela: blit mais rápido

    # ---------------------------------------------------------
    # MINI-SPRITES (cache por sprite)
    # ---------------------------------------------------------
    def _get_mini_sprite(self, sprite: pg.Surface) -> pg.Surface:
        key = id(sprite)
        cached = self._sprite_cache.get(key)

        if cached is not None:
            return cached[1]

        w, h = sprite.get_size()
        mini_w = max(1, round(w * MINI_SPRITE_HEIGHT / h))

        mini = scale_surface(sprite, (mini_w, MINI_SPRITE_HEIGHT)).convert_alpha()

        self._sprite_cache[key] = (sprite, mini)
        return mini

    def prepare(self, player) -> None:
        """Gera todos os mini-sprites antecipadamente, evitando engasgos
        quando um frame novo aparece pela primeira vez durante o jogo."""
        for sprite in (
                player.idle_right, player.idle_left,
                *player.walk_right, *player.walk_left
        ):
            self._get_mini_sprite(sprite)

    # ---------------------------------------------------------
    # DESENHO (executa a cada frame)
    # ---------------------------------------------------------
    def draw(self, surface, player):
        # 1. Fundo pronto: um único blit
        surface.blit(self.background, (self.x, self.y))

        # 2. Apenas o gladiador é dinâmico
        px, py = self.world_to_viewport(
            player.position[0],
            player.position[1]
        )

        mini = self._get_mini_sprite(player.sprite)
        mini_w, mini_h = mini.get_size()

        surface.blit(
            mini,
            (round(px - mini_w / 2), round(py - mini_h / 2))
        )