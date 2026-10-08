import math
import pygame as pg

from game_components.cards import Deck, ActiveCard, Card
from engine.matrix_operations import scale_surface

PLAYER_SPRITE = "assets/sprites/GLADIATOR.png"
PLAYER_WALK_SPRITESHEET = "assets/sprites/GLADIATOR_WALK.png"

PLAYER_SIZE = (250, 335)

WALK_ROWS = 2
WALK_COLUMNS = 1
WALK_ANIMATION_TIME = 0.12


def _load_sprite(
        path: str,
        size: tuple[int, int]
) -> pg.Surface:

    sprite = pg.image.load(path).convert_alpha()

    return scale_surface(
        sprite,
        size
    )

def _load_walk_spritesheet(
        path: str,
        rows: int,
        columns: int,
        size: tuple[int, int]
) -> list[pg.Surface]:

    sheet = pg.image.load(path).convert_alpha()

    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()

    frame_width = sheet_width // columns
    frame_height = sheet_height // rows

    frames = []

    # ==========================================
    # 1. CORTA A SPRITESHEET EM FRAMES
    # ==========================================

    for row in range(rows):
        for column in range(columns):

            frame_rect = pg.Rect(
                column * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            )

            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)

    # ==========================================
    # 2. ENCONTRA UMA ÁREA COMUM A TODOS OS FRAMES
    # ==========================================

    bounds = [
        frame.get_bounding_rect(min_alpha=1)
        for frame in frames
    ]

    left = min(rect.left for rect in bounds)
    top = min(rect.top for rect in bounds)
    right = max(rect.right for rect in bounds)
    bottom = max(rect.bottom for rect in bounds)

    common_rect = pg.Rect(
        left,
        top,
        right - left,
        bottom - top
    )

    # ==========================================
    # 3. CORTA TODOS OS FRAMES COM A MESMA ÁREA
    # ==========================================

    cropped_frames = []

    for frame in frames:
        cropped = frame.subsurface(common_rect).copy()

        scaled = pg.transform.scale(
            cropped,
            size
        )

        cropped_frames.append(scaled)

    return cropped_frames

class Player:

    def __init__(self, hp, dmg_s, def_s, deck):

        self.HP = hp
        self.DMG_S = dmg_s
        self.DEF_S = def_s

        self.deck = Deck(deck)
        self.stack = []

        self.state = "idle"
        self.active_card = None

        # ==========================================
        # MOVIMENTO
        # ==========================================

        self.position = [900.0, 700.0]
        self.speed = 300.0

        # ==========================================
        # SPRITES
        # ==========================================

        self.idle_sprite = _load_sprite(
            PLAYER_SPRITE,
            PLAYER_SIZE
        )

        self.walk_frames = _load_walk_spritesheet(
            PLAYER_WALK_SPRITESHEET,
            WALK_ROWS,
            WALK_COLUMNS,
            PLAYER_SIZE
        )

        # ==========================================
        # ANIMAÇÃO
        # ==========================================

        self.current_frame = 0
        self.animation_timer = 0.0

        self.sprite = self.idle_sprite

    def move(
            self,
            dx: float,
            dy: float,
            dt: float
    ) -> None:

        magnitude = math.sqrt(dx * dx + dy * dy)

        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        self.position[0] += dx * self.speed * dt
        self.position[1] += dy * self.speed * dt

    def update_animation(
            self,
            moving: bool,
            dt: float
    ) -> None:

        if not moving:

            self.current_frame = 0
            self.animation_timer = 0.0
            self.sprite = self.idle_sprite

            return

        self.animation_timer += dt

        if self.animation_timer >= WALK_ANIMATION_TIME:

            self.animation_timer -= WALK_ANIMATION_TIME

            self.current_frame += 1

            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0

        self.sprite = self.walk_frames[self.current_frame]

    def draw(self, screen: pg.Surface) -> None:

        sprite_rect = self.sprite.get_rect(
            center=(
                round(self.position[0]),
                round(self.position[1])
            )
        )

        screen.blit(
            self.sprite,
            sprite_rect
        )

    # ==========================================
    # CARTAS
    # ==========================================

    def start_card(self):

        if self.active_card is not None:
            return

        if self.deck.current is None:
            return

        card = self.deck.current.card

        self.deck.remove_current()

        self.state = "playing"

        self.active_card = ActiveCard(
            card,
            self,
            pg.time.get_ticks()
        )

        card.start(self)

    def cancel_action(self):
        self.state = "idle"
        self.active_card = None

    def finish_action(self):
        self.state = "idle"
        self.active_card = None

    def play_stack(self):
        pass

    def stack_card(self):

        if self.deck.current is None:
            return

        if len(self.stack) >= 3:
            return

        self.stack.append(
            self.deck.current.card
        )

class Enemy:
    def __init__(
            self,
            hp,
            dmg_s,
            def_s,
            deck
    ) -> None:
        self.HP = hp
        self.DMG_s = dmg_s
        self.DEF_s = def_s
        self.deck = Deck(deck)

        self.state = "idle"
        self.active_card = None

    def start_card(self):
        if self.active_card is not None:
            return

        if self.deck.current is None:
            return

        card = self.deck.current.card

        self.deck.remove_current()

        self.state = "playing"
        self.active_card = ActiveCard(
            card,
            self,
            pg.time.get_ticks()
        )

        card.start(self)

    def cancel_action(self):
        self.state = "idle"
        self.active_card = None

    def finish_action(self):
        self.state = "idle"
        self.active_card = None

    def play_current_card(self):
        c = self.deck.current.card
        if c is not None:
            c.play()

    def draw(self): ...