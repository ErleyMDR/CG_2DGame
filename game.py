import random

from game_components.entities import *
from game_components.scenario import Scenario
from game_components.minimap import Minimap
from game_components.hud import Hud
from menu import Menu
from game_components.boot_screen import draw_boot_screen

FPS: int = 60
WIDTH: int = 1820
HEIGHT: int = 920
CARD_FONT: str = "assets/font/PressStart2P-Regular.ttf"
FONT: str = 'Serif'
FONT_SIZE: int = 12
MUSIC = "assets/sound/The_March_to_Gold.mp3"

BLACK: tuple[int,int,int] = (0,0,0)
WHITE: tuple[int,int,int] = (255,255,255)
RED: tuple[int, int, int] = (200, 0, 0)
GREEN: tuple[int, int, int] = (0, 200, 0)
BLUE: tuple[int, int, int] = (0, 0, 200)
YELLOW: tuple[int,int,int] = (215, 215, 40)

card_values: list[int] = [0,1,2,3,4,5,6,7,8,9]

from game_components.cards import (
    Card, AttackCard, MagicCard, DefenseCard, ActiveCard,
    init_card_system
)

class Game:
    def __init__(self):
        # 1. Cria a janela do Pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.SysFont(FONT, FONT_SIZE)
        pg.display.set_caption(self.__repr__())

        # 2. Inicializa o sistema de texturas de cartas APÓS a janela existir
        init_card_system()

        # 3. Adiciona o estado BOOT e o cronômetro
        self.state = "BOOT"
        self.boot_timer = 0.0
        self.boot_duration = 14.0  # Duração em segundos (ex: 3s)
        self.menu = Menu()

        self.is_debug_mode = True
        self.player = Player(200, 10, 10)
        self.enemy = None
        self.hud = None
        self.scenario = Scenario()
        self.minimap = Minimap()
        self.player_active_card = None
        self.enemy_active_card = None

        self.play_counter = 0

        self.count_till_restart = 0
        self.game_over_text = pg.font.SysFont("Arial", 50).render("GAME OVER", True, BLACK)


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

    def activate_card(self, card, player):
        pass

    def cancel_card_effect(self, card):
        pass

    def break_card(self, card: Card):
        card.active = False

        # Cancela o efeito que estava ativo
        self.cancel_card_effect(card)

        if card is self.player_active_card:
            self.player_active_card = None

        elif card is self.enemy_active_card:
            self.enemy_active_card = None

    def update_player(self, dt: float) -> None:
        if self.player is None:
            return

        if self.player.is_dead:
            self.player.update_animation(False, dt)
            return

        if self.player.state == "playing":
            self.player.update_animation(False, dt)
            return

        keys = pg.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pg.K_w]:
            dy -= 1

        if keys[pg.K_s]:
            dy += 1

        if keys[pg.K_a]:
            dx -= 1

        if keys[pg.K_d]:
            dx += 1

        moving = dx != 0 or dy != 0

        self.player.move(
            dx,
            dy,
            dt
        )

        self.player.update_animation(
            moving,
            dt
        )

    def play_music(self):
        pg.mixer.music.load(MUSIC)
        pg.mixer.music.play(-1)

    def stop_music(self):
        pg.mixer.music.stop()

    def game_over(self):
        self.screen.blit(self.game_over_text, (WIDTH//2 - 100, HEIGHT//2))

    def counter_until_restart(self):
        self.count_till_restart += 1
        if self.count_till_restart > FPS * 6.5:
            self.state = "MENU"

    def debug_mode(self):
        fps = int(self.clock.get_fps())
        fps_t = self.font.render(f'FPS: {fps}', True, WHITE)
        t_pos = (10, 10)
        self.screen.blit(fps_t, t_pos)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # EVENTOS
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_CTRL:
                        print("DEBUG MODE OPENED")
                        self.is_debug_mode = not self.is_debug_mode
                    elif event.key == pg.K_f and pg.key.get_mods() & pg.KMOD_CTRL:
                        self.player.HP = 0
                        self.player.die()

                    elif self.state == "PLAYING" and event.key == pg.K_q:
                        if self.player.deck is not None:
                            self.player.deck.prev_card()

                    elif self.state == "PLAYING" and event.key == pg.K_e:
                        if self.player.deck is not None:
                            self.player.deck.next_card()

                    elif self.state == "PLAYING" and event.key == pg.K_SPACE:
                        if self.player.deck is not None:
                            self.player.start_card()
                            self.player.finish_action()

                # Pula a Boot Screen com qualquer tecla ou clique do mouse
                elif self.state == "BOOT":
                    if event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                        self.state = "MENU"

                # REPASSA EVENTOS PARA O MENU QUANDO ESTIVER NO ESTADO "MENU"
                elif self.state == "MENU":
                    action = self.menu.handle_event(event)
                    if action == "PLAYING":
                        self.state = "PLAYING"
                        self.player.set_deck(self.generate_cards())
                        self.hud = Hud(player=self.player, enemy=None)
                        self.minimap.prepare(self.player)
                        self.play_music()

                    elif action == "QUIT":
                        self.running = False

            # UPDATE
            if self.state == "BOOT":
                self.boot_timer += dt
                if self.boot_timer >= self.boot_duration:
                    self.state = "MENU"

            elif self.state == "PLAYING":
                self.update_player(dt)

            # LIMPEZA E RENDERIZAÇÃO
            self.screen.fill(BLACK)

            if self.state == "BOOT":
                draw_boot_screen(self.screen)

            elif self.state == "MENU":
                self.menu.show(self.screen)

            elif self.state == "PLAYING":
                self.scenario.draw(self.screen)
                if self.player is not None:
                    self.player.draw(self.screen)
                    self.hud.draw(self.screen)
                    self.minimap.draw(self.screen, self.player)

                    if self.player.is_dead:
                        self.game_over()
                        self.counter_until_restart()
                        self.stop_music()

            if self.is_debug_mode:
                self.debug_mode()

            pg.display.flip()

        pg.quit()