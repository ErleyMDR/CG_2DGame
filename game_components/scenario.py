from pygame import surface

from engine.draw import Rasterizer


class Scenario:
    def __init__(self):
        self.sky_color = (25, 30, 50)
        self.ground_color = (60, 70, 60)

    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()
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
            center=(width // 2, height - 100),
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

        # Linhas horizontais da arena
        horizontal_lines = [
            (height - 220, 540),
            (height - 170, 585),
            (height - 110, 640)
        ]

        for y, half_width in horizontal_lines:

            # Parte esquerda da linha
            Rasterizer.line(
                surface,
                start_point=(center_x - half_width, y),
                end_point=(center_x - 140, y),
                color=(110, 110, 125)
            )

            # Parte direita da linha
            Rasterizer.line(
                surface,
                start_point=(center_x + 140, y),
                end_point=(center_x + half_width, y),
                color=(110, 110, 125)
        )

    
        # Lua ao fundo
        Rasterizer.circle(
            surface,
            center=(width // 2, 180),
            radius=85,
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
            center=(center_x - 35, 135),
            radius=16,
            color=moon_crater,
            fill=True,
            fill_color=moon_crater
        )

        # Cratera média - direita
        Rasterizer.circle(
            surface,
            center=(center_x + 38, 165),
            radius=11,
            color=moon_crater,
            fill=True,
            fill_color=moon_crater
        )

        # Cratera pequena - parte inferior
        Rasterizer.circle(
            surface,
            center=(center_x - 5, 195),
            radius=7,
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

        for star_x, star_y, star_radius in stars:
            Rasterizer.circle(
                surface,
                center=(star_x, star_y),
                radius=star_radius,
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
                start_point=(x - 70, 215),
                end_point=(x - 70, 455),
                color=pole_color,
                width=5
            )

            # Ponta superior da haste
            Rasterizer.circle(
                surface,
                center=(x - 70, 210),
                radius=7,
                color=(190, 160, 80),
                fill=True
            )

            # -----------------------------------------------------
            # BARRA HORIZONTAL
            # -----------------------------------------------------

            Rasterizer.line(
                surface,
                start_point=(x - 85, 235),
                end_point=(x + 70, 235),
                color=pole_color,
                width=5
            )

            # -----------------------------------------------------
            # CORPO DO ESTANDARTE
            # -----------------------------------------------------

            banner_points = [
                (x - 55, 245),
                (x + 55, 245),
                (x + 55, 410),
                (x, 450),
                (x - 55, 410)
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

            # Haste principal - vai do topo até o solo
            Rasterizer.line(
                surface,
                start_point=(x - 70, 210),
                end_point=(x - 70, height - 165),
                color=pole_color,
                width=6
            )

            # ESPADA 1 - diagonal /
            Rasterizer.line(
                surface,
                start_point=(x - 35, 390),
                end_point=(x + 35, 300),
                color=sword_color,
                width=5
            )

            # Guarda da espada 1
            Rasterizer.line(
                surface,
                start_point=(x - 45, 370),
                end_point=(x - 20, 390),
                color=sword_color,
                width=5
            )

            # Cabo da espada 1
            Rasterizer.line(
                surface,
                start_point=(x - 35, 390),
                end_point=(x - 48, 407),
                color=sword_color,
                width=6
            )


            # ESPADA 2 - diagonal \
            Rasterizer.line(
                surface,
                start_point=(x + 35, 390),
                end_point=(x - 35, 300),
                color=sword_color,
                width=5
            )

            # Guarda da espada 2
            Rasterizer.line(
                surface,
                start_point=(x + 20, 390),
                end_point=(x + 45, 370),
                color=sword_color,
                width=5
            )

            # Cabo da espada 2
            Rasterizer.line(
                surface,
                start_point=(x + 35, 390),
                end_point=(x + 48, 407),
                color=sword_color,
                width=6
            )

            # ==========================================
            # PONTAS DAS ESPADAS
            # ==========================================

            # Ponta da espada /
            Rasterizer.polygon(
                surface,
                points=[
                    (x + 31, 297),
                    (x + 26, 302),
                    (x + 30, 304)
                ],
                color=sword_color,
                fill=True,
                fill_color=sword_color
            )

            # Ponta da espada \
            Rasterizer.polygon(
                surface,
                points=[
                    (x - 31, 297),
                    (x - 30, 304),
                    (x - 26, 302)
                ],
                color=sword_color,
                fill=True,
                fill_color=sword_color
            )
            
                # Arquibancada / muralha ao fundo
        stands_points = [
            (120, height - 300),
            (width - 120, height - 300),
            (width - 250, height - 180),
            (250, height - 180)
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

        for x in light_positions:
            # Suporte da luminária
            Rasterizer.rectangle(
                surface,
                center=(x, height - 240),
                width=45,
                height=35,
                color=(80, 80, 100),
                fill=True,
                fill_color=(50, 50, 65)
            )
            
            # Halo externo
            Rasterizer.circle(
                surface,
                center=(x, height - 240),
                radius=18,
                color=(95, 70, 35),
                fill=True
            )

            # Halo interno
            Rasterizer.circle(
                surface,
                center=(x, height - 240),
                radius=12,
                color=(210, 145, 45),
                fill=True
            )

            # Núcleo da luz
            Rasterizer.circle(
                surface,
                center=(x, height - 240),
                radius=6,
                color=(255, 225, 140),
                fill=True
            )

        # ==========================================
        # FEIXE DE LUZ DA ENTRADA
        # ==========================================

        light_points = [
        # começa exatamente na abertura da porta
            (center_x - 38, height - 170),
            (center_x + 38, height - 170),

        # abre em direção à frente da arena
            (center_x + 150, height),
            (center_x - 150, height)
        ]

        Rasterizer.polygon(
            surface,
            points=light_points,
            color=(95, 88, 68),
            fill=True,
            fill_color=(95, 88, 68)
        )

    
        # Entrada central da arenagame
        door_center_x = width // 2
        door_y = height - 225
    

        # Interior da entrada arena
        Rasterizer.rectangle(
            surface,
            center=(door_center_x, door_y),
            width=220,
            height=110,
            color=(75, 70, 65),
            border_width=5,
            fill=True,
            fill_color=(75, 70, 65)
        )

        # Porta esquerda aberta
        left_door = [
            (door_center_x - 110, door_y - 55),
            (door_center_x - 55, door_y - 35),
            (door_center_x - 55, door_y + 35),
            (door_center_x - 110, door_y + 55)
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
            (door_center_x + 110, door_y - 55),
            (door_center_x + 55, door_y - 35),
            (door_center_x + 55, door_y + 35),
            (door_center_x + 110, door_y + 55)
        ]

        Rasterizer.polygon(
            surface,
            points=right_door,
            color=(120, 120, 145),
            fill=True,
            fill_color=(65, 65, 85)
        )