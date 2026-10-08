
from engine.matrix_operations import (
    translation,
    scale,
    mat_mult,
    aplica_transformacao
)
from engine.matrix_operations import scale_surface
from engine.draw import Rasterizer


class Minimap:
    def __init__(self):
        # Posição e dimensões da viewport
        self.x = 1510
        self.y = 30
        self.width = 260
        self.height = 180
        # Cache para evitar redimensionar a imagem a cada frame
        self.mini_sprite_original = None
        self.mini_sprite = None

        # Limites da janela no mundo
        self.world_min_x = 210
        self.world_max_x = 1610
        self.world_min_y = 680
        self.world_max_y = 880

        # Matriz de transformação: mundo -> viewport
        sx = self.width / (self.world_max_x - self.world_min_x)
        sy = self.height / (self.world_max_y - self.world_min_y)

        self.matrix = mat_mult(
            translation(self.x, self.y),
            mat_mult(
                scale(sx, sy),
                translation(-self.world_min_x, -self.world_min_y)
            )
        )

    def world_to_viewport(self, x, y):
        px, py = aplica_transformacao(
            self.matrix, [(x, y)]
        )[0]

        return round(px), round(py)

    def draw_world_rectangle(
        self, surface, center, width, height,
        color, fill_color, border_width=1
    ):
        # Transforma os cantos do retângulo
        cx, cy = center

        x1, y1 = self.world_to_viewport(
            cx - width / 2,
            cy - height / 2
        )

        x2, y2 = self.world_to_viewport(
            cx + width / 2,
            cy + height / 2
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

    def draw(self, surface, player):

        # Fundo da viewport
        Rasterizer.rectangle(
            surface,
            center=(
                self.x + self.width // 2,
                self.y + self.height // 2
            ),
            width=self.width,
            height=self.height,
            color=(180, 180, 190),
            border_width=3,
            fill=True,
            fill_color=(55, 55, 70)
        )

        # Parede lateral esquerda
        self.draw_world_rectangle(
            surface,
            center=(237, 780),
            width=54,
            height=200,
            color=(175, 175, 190),
            fill_color=(110, 110, 125)
        )

        # Parede lateral direita
        self.draw_world_rectangle(
            surface,
            center=(1583, 780),
            width=54,
            height=200,
            color=(175, 175, 190),
            fill_color=(110, 110, 125)
        )

        # Parede superior esquerda
        self.draw_world_rectangle(
            surface,
            center=(506, 685),
            width=592,
            height=11,
            color=(175, 175, 190),
            fill_color=(110, 110, 125)
        )

        # Parede superior direita
        self.draw_world_rectangle(
            surface,
            center=(1314, 685),
            width=592,
            height=11,
            color=(175, 175, 190),
            fill_color=(110, 110, 125)
        )

        # Linha central da arena
        inicio = self.world_to_viewport(264, 780)
        fim = self.world_to_viewport(1556, 780)

        Rasterizer.line(
            surface,
            start_point=inicio,
            end_point=fim,
            color=(110, 110, 130),
            width=2
        )

        # Elipse central da arena
        centro = self.world_to_viewport(910, 780)

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
            surface,
            center=centro,
            x_radius=raio_x,
            y_radius=raio_y,
            color=(145, 145, 165),
            border_width=2,
            fill=False
        )

        # Portão central
        self.draw_world_rectangle(
            surface,
            center=(900, 686),
            width=296,
            height=11,
            color=(210, 210, 220),
            fill_color=(155, 155, 170),
            border_width=2
        )

        # Posição do gladiador
        px, py = self.world_to_viewport(
            player.position[0],
            player.position[1]
        )

                # Utiliza o sprite atual do gladiador
        sprite_original = player.sprite

        # Redimensiona apenas quando o sprite muda
        if sprite_original is not self.mini_sprite_original:
            largura, altura = sprite_original.get_size()

            mini_altura = 28
            mini_largura = max(
                1,
                round(largura * mini_altura / altura)
            )

            self.mini_sprite = scale_surface(
                sprite_original,
                (mini_largura, mini_altura)
            )

            self.mini_sprite_original = sprite_original

        # Centraliza o gladiador na posição do minimapa
        mini_w, mini_h = self.mini_sprite.get_size()

        surface.blit(
            self.mini_sprite,
            (
                round(px - mini_w / 2),
                round(py - mini_h / 2)
            )
        )
        
        