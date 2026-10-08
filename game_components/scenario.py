import pygame
import math

from engine.draw import Rasterizer


class Scenario:
    def __init__(self, s):
        self.sky_color = (25, 30, 50)
        self.ground_color = (60, 70, 60)
        self.screen = self._rasterize(s)

    def draw(self, surf):
        surf.blit(self.screen, (0, 0))

    def _rasterize(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        surface = pygame.Surface((width, height))

        center_x = width // 2

        # Fundo
        Rasterizer.rectangle(
            surface,
            center=(width // 2, height // 2),
            width=width,
            height=height,
            color=self.sky_color,
            fill=True
        )

        # Chão
        Rasterizer.rectangle(
            surface,
            center=(width // 2, height - 140),
            width=width,
            height=200,
            color=self.ground_color,
            fill=True
        )


        # Plataforma principal da arena
        arena_points = [
            (width // 2 - 500, height - 260),
            (width // 2 + 500, height - 260),
            (width // 2 + 700, height - 40),
            (width // 2 - 700, height - 40)
        ]

        Rasterizer.polygon(
            surface,
            points=arena_points,
            color=(160, 160, 170),
            fill=True,
            fill_color=(75, 75, 90)
        )

        

        # Marca central da arena de games
        Rasterizer.ellipse(
            surface,
            center=(center_x, height - 115),
            x_radius=210,
            y_radius=65,
            color=(135, 135, 165),
            border_width=4,
            fill=False
        )

        # Círculo interno games
        Rasterizer.ellipse(
            surface,
            center=(center_x, height - 115),
            x_radius=130,
            y_radius=40,
            color=(100, 100, 135),
            border_width=3,
            fill=False
        )

        # Linhas de perspectiva da arena
        center_x = width // 2

        Rasterizer.line(
            surface,
            start_point=(center_x, height - 260),
            end_point=(center_x, height - 40),
            color=(110, 110, 125)
        )

        Rasterizer.line(
            surface,
            start_point=(center_x - 250, height - 260),
            end_point=(center_x - 350, height - 40),
            color=(110, 110, 125)
        )

        Rasterizer.line(
            surface,
            start_point=(center_x + 250, height - 260),
            end_point=(center_x + 350, height - 40),
            color=(110, 110, 125)
        )

        # ==========================================
        # FEIXE DE LUZ DA ENTRADA
        # ==========================================

        light_points = [
        # começa exatamente na abertura da porta
            (center_x - 85, height - 240),
            (center_x + 85, height - 240),
        # abre em direção à frente da arena
            (center_x + 240, height),
            (center_x - 240, height)
        ]

        Rasterizer.polygon(
            surface,
            points=light_points,
            color=(95, 88, 68),
            fill=True,
            fill_color=(95, 88, 68)
        )


        # Linhas horizontais da arena
        horizontal_lines = [
            (height - 220, 540),
            (height - 170, 585),
            (height - 110, 640)
        ]

        for y, half_width in horizontal_lines:
            Rasterizer.line(
                surface,
                start_point=(center_x - half_width, y),
                end_point=(center_x + half_width, y),
                color=(110, 110, 125),
                width=2
            )

        # Lua
            Rasterizer.circle(
            surface,
            center=(width // 2, 170),
            radius=60,
            color=(220, 220, 190),
            fill=True
        )

        # ==========================================
        # DETALHES / CRATERAS DA LUA
        # ==========================================

        moon_crater = (205, 203, 170)

         # Cratera maior - esquerda
        Rasterizer.circle(
            surface,
            center=(center_x - 25, 140),
            radius=11,
            color=moon_crater,
            fill=True,
            fill_color=moon_crater
        )

        # Cratera média - direita
        Rasterizer.circle(
            surface,
            center=(center_x + 27, 160),
            radius=8,
            color=moon_crater,
            fill=True,
            fill_color=moon_crater
        )

        # Cratera pequena
        Rasterizer.circle(
            surface,
            center=(center_x - 4, 180),
            radius=5,
            color=moon_crater,
            fill=True,
            fill_color=moon_crater
        )

        # ==========================================
        # ESTRELAS DO CÉU
        # ==========================================

        star_color = (210, 210, 190)

        stars = [
        # lado esquerdo
             (180, 120, 2),
             (310, 175, 2),
             (430, 95, 1),
             (535, 230, 2),
             (650, 145, 1),
             (250, 310, 1),
             (480, 380, 2),

        # lado direito
             (width - 180, 135, 2),
             (width - 310, 205, 1),
             (width - 430, 105, 2),
             (width - 550, 285, 1),
             (width - 660, 175, 2),
             (width - 260, 350, 1),
             (width - 470, 410, 2),
        ]

        # Tempo da animação
        time = pygame.time.get_ticks() / 1000.0

        for i, (star_x, star_y, star_radius) in enumerate(stars):
        # Cada estrela pisca em uma fase diferente
            blink = (math.sin(time * 2 + i * 0.8) + 1) / 2

        # Tamanho normal
            animated_radius = star_radius

        # Em alguns momentos cresce 1 pixel
            if blink > 0.75:
                animated_radius += 1

        # Desenha Essa estrela
            Rasterizer.circle(
            surface,
            center=(star_x, star_y),
            radius=animated_radius,
            color=star_color,
            fill=True,
            fill_color=star_color
            )

        # =========================================================
        # ESTANDARTES DA ARENA
        # =========================================================

        banner_color = (55, 45, 75)
        banner_border = (125, 120, 155)
        sword_color = (210, 170, 70)
        pole_color = (105, 100, 125)

        # Posição dos dois estandartes
        banner_positions = [
            width // 4,
            3 * width // 4
        ]

        for x in banner_positions:

            # -----------------------------------------------------
            # HASTE VERTICAL
            # -----------------------------------------------------

            Rasterizer.line(
                surface,
                start_point=(x - 48, 250),
                end_point=(x - 48, 560),
                color=pole_color,
                width=4
            )

            # Ponta superior da haste
            Rasterizer.circle(
                surface,
                center=(x - 48, 245),
                radius=5,
                color=(190, 160, 80),
                fill=True
            )

            # -----------------------------------------------------
            # BARRA HORIZONTAL
            # -----------------------------------------------------

            Rasterizer.line(
                surface,
                start_point=(x - 58, 260),
                end_point=(x + 48, 260),
                color=pole_color,
                width=4
            )

            # -----------------------------------------------------
            # CORPO DO ESTANDARTE
            # -----------------------------------------------------

            banner_points = [
                    (x - 40, 270),
                    (x + 40, 270),
                    (x + 40, 385),
                    (x, 415),
                    (x - 40, 385)
            ]

            Rasterizer.polygon(
                surface,
                points=banner_points,
                color=banner_border,
                fill=True,
                fill_color=banner_color
            )

            # =====================================================
            # DUAS ESPADAS CRUZADAS
            # =====================================================

        
            # ESPADA 1 - diagonal /
            Rasterizer.line(
                surface,
                start_point=(x - 25, 375),
                end_point=(x + 25, 300),
                color=sword_color,
                width=4
            )

            # Guarda da espada 1
            Rasterizer.line(
                surface,
                start_point=(x - 34, 360),
                end_point=(x - 17, 375),
                color=sword_color,
                width=4
            )

            # Cabo da espada 1
            Rasterizer.line(
                surface,
                start_point=(x - 25, 375),
                end_point=(x - 34, 389),
                color=sword_color,
                width=5
)


            # ESPADA 2 - diagonal \
            Rasterizer.line(
                surface,
                start_point=(x + 25, 375),
                end_point=(x - 25, 300),
                color=sword_color,
                width=4
            )

            # Guarda da espada 2
            Rasterizer.line(
                surface,
                start_point=(x + 17, 375),
                end_point=(x + 34, 360),
                color=sword_color,
                width=4
            )

            # Cabo da espada 2
            Rasterizer.line(
                surface,
                start_point=(x + 25, 375),
                end_point=(x + 34, 389),
                color=sword_color,
                width=5
            )
            # ==========================================
            # PONTAS DAS ESPADAS
            # ==========================================

            # Ponta da espada s
            Rasterizer.polygon(
                surface,
                points=[
                    (x + 25, 296),
                    (x + 20, 303),
                    (x + 27, 303)
                ],
                color=sword_color,
                fill=True,
                fill_color=sword_color
            )

            # Ponta da espada 
            Rasterizer.polygon(
                surface,
                points=[
                    (x - 25, 296),
                    (x - 27, 303),
                    (x - 20, 303)
                ],
                color=sword_color,
                fill=True,
                fill_color=sword_color
            )   

        # Arquibancada / muralha ao fundo
        stands_points = [
            (0, height - 450),
            (width, height - 450),
            (width, height - 240),
            (0, height - 240)
        ]

        Rasterizer.polygon(
            surface,
            points=stands_points,
            color=(90, 90, 110),
            fill=True,
            fill_color=(35, 35, 50)
        )

        
        # Luzes da arquibancada
        light_positions = [
            300, 500, 700,
            width - 700, width - 500, width - 300
        ]

        # Tempo usado para a rotação
        light_time = pygame.time.get_ticks() / 1000.0

        for x in light_positions:

            light_y = height - 380

        # Suporte da luminária
            Rasterizer.rectangle(
                surface,
                center=(x, light_y),
                width=36,
                height=30,
                color=(80, 80, 100),
                fill=True,
                fill_color=(50, 50, 65)
            )

        # Halo externo
            Rasterizer.circle(
                surface,
                center=(x, light_y),
                radius=18,
                color=(95, 70, 35),
                fill=True
            )

        # Halo interno
            Rasterizer.circle(
                surface,
                center=(x, light_y),
                radius=12,
                color=(210, 145, 45),
                fill=True
            )

        # Núcleo da luz
            Rasterizer.circle(
                surface,
                center=(x, light_y),
                radius=6,
                color=(255, 225, 140),
                fill=True
            )

    # ==========================================
    # Pontos luminosos girando ao redor da luz
    # ==========================================

            orbit_radius = 12

            for i in range(6):

            # 3 pontos separados por 120 graus
                angle = light_time * 2 + i * (2 * math.pi / 6)

                orbit_x = x + math.cos(angle) * orbit_radius
                orbit_y = light_y + math.sin(angle) * orbit_radius

                Rasterizer.circle(
                    surface,
                    center=(int(orbit_x), int(orbit_y)),
                    radius=2,
                    color=(255, 210, 100),
                    fill=True,
                    fill_color=(255, 210, 100)
            )

    
        # Entrada central da arenagame
        door_center_x = width // 2
        door_y = height - 315
    

        # Interior da entrada arena
        Rasterizer.rectangle(
            surface,
            center=(door_center_x, door_y),
            width=280,
            height=150,
            color=(75, 70, 65),
            border_width=5,
            fill=True,
            fill_color=(75, 70, 65)
        )

        # Porta esquerda aberta
        left_door = [
            (door_center_x - 135, door_y - 70),
            (door_center_x - 65, door_y - 45),
            (door_center_x - 65, door_y + 45),
            (door_center_x - 135, door_y + 70)
        ]
        Rasterizer.polygon(
            surface,
            points=left_door,
            color=(120, 120, 145),
            fill=True,
            fill_color=(65, 65, 85)
        )

        # Porta direita aberta
        right_door = [
            (door_center_x + 135, door_y - 70),
            (door_center_x + 65, door_y - 45),
            (door_center_x + 65, door_y + 45),
            (door_center_x + 135, door_y + 70)
        ]
        Rasterizer.polygon(
            surface,
            points=right_door,
            color=(120, 120, 145),
            fill=True,
            fill_color=(65, 65, 85)
        )

        return surface