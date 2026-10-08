import math
import pygame as pg

from game_components.cards import (
    Deck,
    ActiveCard,
    Card
)
from engine.matrix_operations import (
    scale_surface, flip_surface_horizontal, surface_bounds, rotate_surface
)

DEATH_DURATION = 0.8    # segundos
DEATH_FRAMES = 8        # quantidade de ângulos pré-calculados

PLAYER_SPRITE = "assets/sprites/GLADIATOR.png"
PLAYER_WALK_SPRITESHEET = "assets/sprites/GLADIATOR_WALK.png"

PLAYER_SIZE = (102, 150)

WALK_ROWS = 2
WALK_COLUMNS = 1
WALK_ANIMATION_TIME = 0.15

# ==============================================================================
# LIMITES MATEMÁTICOS DO CHÃO CINZA (Sem uso de pg.Rect)
# ==============================================================================
# Limites verticais da arena (Y)
FLOOR_MIN_Y = 680.0  # Topo da grade cinza
FLOOR_MAX_Y = 880.0  # Base da grade cinza

# Limites horizontais no topo (Y = 680) e na base (Y = 880) para acompanhar a perspectiva
TOP_MIN_X = 380.0
TOP_MAX_X = 1440.0
BOTTOM_MIN_X = 210.0
BOTTOM_MAX_X = 1610.0


def _crop_and_scale_to_height(surface, box, height):
    # box = (x, y, w, h)
    cropped = surface.subsurface(box).copy()
    width = max(1, round(box[2] * height / box[3]))
    return scale_surface(cropped, (width, height))


def _load_sprite(path: str, height: int) -> pg.Surface:
    sprite = pg.image.load(path).convert_alpha()
    return _crop_and_scale_to_height(sprite, surface_bounds(sprite), height)


def _load_walk_spritesheet(path, rows, columns, height):
    sheet = pg.image.load(path).convert_alpha()

    fw = sheet.get_width() // columns
    fh = sheet.get_height() // rows

    frames = []
    for row in range(rows):
        for col in range(columns):
            frames.append(
                sheet.subsurface((col * fw, row * fh, fw, fh)).copy()
            )

    bounds = [surface_bounds(f) for f in frames]

    left = min(b[0] for b in bounds)
    top = min(b[1] for b in bounds)
    right = max(b[0] + b[2] for b in bounds)
    bottom = max(b[1] + b[3] for b in bounds)

    common = (left, top, right - left, bottom - top)

    return [_crop_and_scale_to_height(f, common, height) for f in frames]


class Player:

    def __init__(self, hp, dmg_s, def_s):
        self.HP = hp
        self.MAX_HP = hp
        self.DMG_S = dmg_s
        self.DEF_S = def_s

        self.deck = None
        self.stack = []

        self.state = "idle"
        self.active_card = None

        # ==========================================
        # MOVIMENTO (Inicia dentro do chão)
        # ==========================================
        self.position = [500, 780.0]
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

        self.is_dead = False
        self.death_timer = 0.0
        self.death_frames = []
        self.death_canvas = 0
        self.death_start_cy = 0.0
        self.death_end_cy = 0.0
        self.death_index = 0

    def set_deck(self, deck):
        self.deck = Deck(deck)

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

        # 1. Posição pretendida
        next_x = self.position[0] + dx * self.speed * dt
        next_y = self.position[1] + dy * self.speed * dt

        # 2. Restringe Y aos limites do chão
        next_y = max(FLOOR_MIN_Y, min(next_y, FLOOR_MAX_Y))

        # 3. Interpolação linear para os limites horizontais da perspectiva (Trapézio)
        t = (next_y - FLOOR_MIN_Y) / (FLOOR_MAX_Y - FLOOR_MIN_Y) if FLOOR_MAX_Y != FLOOR_MIN_Y else 0.0
        current_min_x = TOP_MIN_X + (BOTTOM_MIN_X - TOP_MIN_X) * t
        current_max_x = TOP_MAX_X + (BOTTOM_MAX_X - TOP_MAX_X) * t

        # 4. Restringe X de acordo com a altura Y atual
        next_x = max(current_min_x, min(next_x, current_max_x))

        self.position[0] = next_x
        self.position[1] = next_y

    def update_animation(self, moving: bool, dt: float) -> None:
        if self.is_dead:
            self._update_death(dt)
            return

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
        if self.is_dead:
            t = self._death_progress
            cy = self.death_start_cy + (self.death_end_cy - self.death_start_cy) * t
            half = self.death_canvas // 2

            screen.blit(
                self.death_frames[self.death_index],
                (round(self.position[0]) - half, round(cy) - half)
            )
            return

        w, h = self.sprite.get_size()
        screen.blit(
            self.sprite,
            (round(self.position[0]) - w // 2, round(self.position[1]) - h)
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

    def take_damage(self, amount: int) -> None:
        if self.is_dead:
            return
        self.HP = max(0, self.HP - amount)
        if self.HP == 0:
            self.die()

    def die(self) -> None:
        self.is_dead = True
        self.state = "dead"
        self.active_card = None
        self.death_timer = 0.0
        self.death_index = 0

        base = self.idle_left if self.facing_left else self.idle_right
        w, h = base.get_size()

        # Virado para a direita -> cai para a esquerda (anti-horário, theta < 0).
        # Virado para a esquerda -> cai para a direita (horário, theta > 0).
        final_angle = math.pi / 2 if self.facing_left else -math.pi / 2

        self.death_canvas = math.ceil(math.sqrt(w * w + h * h)) + 2

        # as rotações são calculadas uma única vez, no momento da morte
        self.death_frames = [
            rotate_surface(
                base,
                final_angle * i / (DEATH_FRAMES - 1),
                self.death_canvas
            )
            for i in range(DEATH_FRAMES)
        ]

        # Centro do sprite em pé -> centro do sprite deitado.
        # Deitado, a "espessura" vertical passa a ser a largura (w),
        # então o centro desce (h - w) / 2 pixels.
        self.death_start_cy = self.position[1] - h / 2
        self.death_end_cy = self.position[1] - w / 2

    def _update_death(self, dt: float) -> None:
        self.death_timer = min(DEATH_DURATION, self.death_timer + dt)
        p = self.death_timer / DEATH_DURATION
        self._death_progress = p * p        # acelera como uma queda
        self.death_index = round(self._death_progress * (DEATH_FRAMES - 1))


class Enemy:
    def __init__(
            self,
            hp,
            dmg_s,
            def_s,
            deck
    ) -> None:
        self.HP = hp
        self.MAX_HP = hp
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

    def take_damage(self, amount: int) -> None:
        self.HP = max(0, self.HP - amount)