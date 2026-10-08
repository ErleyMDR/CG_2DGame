import math
import pygame as pg

from game_components.cards import Deck, ActiveCard, Card
from engine.matrix_operations import scale_surface, flip_surface_horizontal

PLAYER_SPRITE = "assets/sprites/GLADIATOR.png"
PLAYER_WALK_SPRITESHEET = "assets/sprites/GLADIATOR_WALK.png"

PLAYER_SIZE = (102, 150)

WALK_ROWS = 2
WALK_COLUMNS = 1
WALK_ANIMATION_TIME = 0.15


def _crop_and_scale_to_height(
        surface: pg.Surface,
        rect: pg.Rect,
        height: int
) -> pg.Surface:

    cropped = surface.subsurface(rect).copy()

    width = max(1, round(rect.width * height / rect.height))

    return scale_surface(cropped, (width, height))


def _load_sprite(path: str, height: int) -> pg.Surface:

    sprite = pg.image.load(path).convert_alpha()

    rect = sprite.get_bounding_rect(min_alpha=1)

    return _crop_and_scale_to_height(sprite, rect, height)


def _load_walk_spritesheet(
        path: str,
        rows: int,
        columns: int,
        height: int
) -> list[pg.Surface]:

    sheet = pg.image.load(path).convert_alpha()

    frame_width = sheet.get_width() // columns
    frame_height = sheet.get_height() // rows

    frames = []

    for row in range(rows):
        for column in range(columns):
            frame_rect = pg.Rect(
                column * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            )
            frames.append(sheet.subsurface(frame_rect).copy())

    bounds = [f.get_bounding_rect(min_alpha=1) for f in frames]

    common_rect = pg.Rect(
        min(r.left for r in bounds),
        min(r.top for r in bounds),
        max(r.right for r in bounds) - min(r.left for r in bounds),
        max(r.bottom for r in bounds) - min(r.top for r in bounds)
    )

    return [
        _crop_and_scale_to_height(frame, common_rect, height)
        for frame in frames
    ]

class Player:

    def __init__(self, hp, dmg_s, def_s, deck):

        self.HP = hp
        self.DMG_S = dmg_s
        self.DEF_S = def_s

        self.deck = Deck(deck) if deck is not None else None
        self.stack = []

        self.state = "idle"
        self.active_card = None

        # ==========================================
        # MOVIMENTO
        # ==========================================

        self.position = [500.0, 700.0]
        self.speed = 300.0

        # ==========================================
        # SPRITES & ANIMAÇÃO
        # ==========================================
        self.facing_left = False

        self.idle_right = _load_sprite(PLAYER_SPRITE, PLAYER_SIZE[1])
        self.walk_right = _load_walk_spritesheet(
            PLAYER_WALK_SPRITESHEET,
            WALK_ROWS,
            WALK_COLUMNS,
            PLAYER_SIZE[1]
        )

        # versões espelhadas, calculadas uma única vez
        self.idle_left = flip_surface_horizontal(self.idle_right)
        self.walk_left = [
            flip_surface_horizontal(f) for f in self.walk_right
        ]

        self.current_frame = 0
        self.animation_timer = 0.0
        self.sprite = self.idle_right

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

        if dx < 0:
            self.facing_left = True
        elif dx > 0:
            self.facing_left = False

        self.position[0] += dx * self.speed * dt
        self.position[1] += dy * self.speed * dt

    def update_animation(self, moving: bool, dt: float) -> None:
        idle = self.idle_left if self.facing_left else self.idle_right
        walk = self.walk_left if self.facing_left else self.walk_right

        if not moving:
            self.current_frame = 0
            self.animation_timer = 0.0
            self.sprite = idle
            return

        self.animation_timer += dt

        if self.animation_timer >= WALK_ANIMATION_TIME:
            self.animation_timer -= WALK_ANIMATION_TIME
            self.current_frame = (self.current_frame + 1) % len(walk)

        self.sprite = walk[self.current_frame]

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