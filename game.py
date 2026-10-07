import pygame as pg
import random

from engine import draw
from game_components.cards import Card, AttackCard, MagicCard, DefenseCard
from game_components.hud import Hud
from game_components.entities import *
from menu import Menu

FPS: int = 60
WIDTH: int = 1820
HEIGHT: int = 920
CARD_FONT: str = "assets/font/PressStart2P-Regular.ttf"
FONT: str = 'Serif'
FONT_SIZE: int = 12

BLACK: tuple[int,int,int] = (0,0,0)
WHITE: tuple[int,int,int] = (255,255,255)
RED: tuple[int, int, int] = (200, 0, 0)
GREEN: tuple[int, int, int] = (0, 200, 0)
BLUE: tuple[int, int, int] = (0, 0, 200)
YELLOW: tuple[int,int,int] = (215, 215, 40)

card_values: list[int] = [0,1,2,3,4,5,6,7,8,9]

cx = WIDTH // 2
cy = HEIGHT // 2

w = 372
h = 670

cut = 20

card_p = [
    (cx - w//2 + cut, cy - h//2),  # superior-esquerdo
    (cx + w//2 - cut, cy - h//2),  # superior-direito

    (cx + w//2,       cy - h//2 + cut),  # direita-superior
    (cx + w//2,       cy + h//2 - cut),  # direita-inferior

    (cx + w//2 - cut, cy + h//2),  # inferior-direito
    (cx - w//2 + cut, cy + h//2),  # inferior-esquerdo

    (cx - w//2,       cy + h//2 - cut),  # esquerda-inferior
    (cx - w//2,       cy - h//2 + cut),  # esquerda-superior
]

uvs = [
    (cut / w,       0.01),             # superior-esquerdo
    ((w - cut) / w, 0.01),             # superior-direito

    (0.99,            cut / h),        # direita-superior
    (0.99,            (h - cut) / h),  # direita-inferior

    ((w - cut) / w, 0.99),             # inferior-direito
    (cut / w,       0.99),              # inferior-esquerdo

    (0.01,            (h - cut) / h),  # esquerda-inferior
    (0.01,            cut / h),         # esquerda-superior
]

# uvs = [
#     (0.0941, 0.0),
#     (0.9059, 0.0),
#
#     (1.0,    0.0522),
#     (1.0,    0.9478),
#
#     (0.9059, 1.0),
#     (0.0941, 1.0),
#
#     (0.0,    0.9478),
#     (0.0,    0.0522),
# ]

class Game:
    def __init__(self):
        # pygame setup
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.SysFont(FONT, FONT_SIZE)
        pg.display.set_caption(self.__repr__())

        # Estado do Jogo
        self.state = "TEST"

        self.menu = Menu()

        self.is_debug_mode = True
        self.player = None
        self.enemy = None
        self.hud = None

        self.player_active_card = None
        self.enemy_active_card = None

        self.play_counter = 0


    def __repr__(self):
        return "RTCB - Real Time Card Battle"

    def generate_cards(self):
        cards = []

        # Quantidade de cada tipo
        attack_count = 12
        magic_count = 10
        defense_count = 8

        # ==========================================
        # VALORES
        # ==========================================

        # Garante pelo menos uma carta de cada valor
        values = card_values.copy()

        # As outras 20 cartas podem ter qualquer valor
        values += random.choices(card_values, k=20)

        # Embaralha os valores
        random.shuffle(values)

        # ==========================================
        # TIPOS
        # ==========================================

        card_types = (
                ["attack"] * attack_count +
                ["magic"] * magic_count +
                ["defense"] * defense_count
        )

        random.shuffle(card_types)

        # ==========================================
        # GERAÇÃO DAS CARTAS
        # ==========================================

        magic_types = ["Fire", "Ice", "Thunder"]

        for card_type, value in zip(card_types, values):

            if card_type == "attack":
                cards.append(
                    AttackCard(value)
                )

            elif card_type == "magic":
                magic = random.choice(magic_types)

                cards.append(
                    MagicCard(value, magic)
                )

            elif card_type == "defense":
                cards.append(
                    DefenseCard(value)
                )

        # Embaralhamento adicional das cartas
        random.shuffle(cards)

        return cards

    def card_breaks(self, new_card: Card, active_card: Card) -> bool:
        if new_card.value == 0:
            return new_card.play_order > active_card.play_order

        if active_card.value == 0:
            return new_card.play_order > active_card.play_order

        return new_card.value > active_card.value

    def play_player_card(self):
        if self.player is None:
            return

        if self.player.deck.current is None:
            return

        card = self.player.deck.current.card

        self.play_counter += 1
        card.play_order = self.play_counter
        card.active = True

        # Remove a carta do deck
        self.player.deck.remove_current()

        # Resolve o confronto com a carta inimiga
        if self.enemy_active_card is not None:
            if self.card_breaks(card, self.enemy_active_card):
                self.break_card(self.enemy_active_card)

        # A nova carta passa a ser a carta ativa
        self.player_active_card = card

        # Executa o efeito
        self.activate_card(card, self.player)

    def decide_winner(self):
        ...

    def debug_mode(self):
        fps = int(self.clock.get_fps())
        fps_t = self.font.render(f'FPS: {fps}', True, WHITE)
        t_pos = (10, 10)
        self.screen.blit(fps_t, t_pos)
        # Meant to highlight debug stats
        # sp = (t_pos[0] - 4, t_pos[1] + fps_t.height)
        # ep = (t_pos[0] + 4 + fps_t.width, t_pos[1] + fps_t.height)
        # draw.line(self.screen, color=YELLOW, start_point=sp, end_point=ep)

    def run(self):
        while self.running:

            # self.screen.fill(BLACK)

            if self.state == "MENU":
                self.menu.show(self.screen)

            elif self.state == "PLAYING":
                # if self.player
                pass

            elif self.state == "GAME_OVER":
                pass

            elif self.state == "CONTROLS":
                pass

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_CTRL:
                        print("DEBUG MODE OPENED")
                        self.is_debug_mode = not self.is_debug_mode

            # fill the screen with a color to wipe away anything from last frame

            # RENDER YOUR GAME HERE
            # self.hud.draw(self.screen)


            # Calls debug_mode() if active
            if self.is_debug_mode: self.debug_mode()

            # flip() the display to put your work on screen
            pg.display.flip()

            self.clock.tick(FPS)  # limits FPS to 60

        pg.quit()