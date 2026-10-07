import pygame as pg

from abc import ABC, abstractmethod
from typing import override

from engine import draw

BLACK = (0, 0, 0)
CARD_FONT: str = "assets/font/PressStart2P-Regular.ttf"
CARD_FONT_SIZE:int = 80
card_font = pg.font.Font(CARD_FONT, CARD_FONT_SIZE)

CARD_SIZE = (50, 100)
TEXTURE_SIZE = (372, 670)
w, h = TEXTURE_SIZE[0]//2, TEXTURE_SIZE[1]//2

TEXTURE_CUT = 20

def _rasterize_texture(texture: pg.Surface) -> pg.Surface:
    card_w, card_h = CARD_SIZE
    tex_w, tex_h = texture.get_size()

    cx = card_w // 2
    cy = card_h // 2

    # Converte o corte da textura para o tamanho da carta
    cut_x = card_w * TEXTURE_CUT / tex_w
    cut_y = card_h * TEXTURE_CUT / tex_h

    card_p = [
        (cx - card_w/2 + cut_x, cy - card_h/2),
        (cx + card_w/2 - cut_x, cy - card_h/2),

        (cx + card_w/2, cy - card_h/2 + cut_y),
        (cx + card_w/2, cy + card_h/2 - cut_y),

        (cx + card_w/2 - cut_x, cy + card_h/2),
        (cx - card_w/2 + cut_x, cy + card_h/2),

        (cx - card_w/2, cy + card_h/2 - cut_y),
        (cx - card_w/2, cy - card_h/2 + cut_y),
    ]

    uvs = [
        (TEXTURE_CUT / tex_w, 0.01),
        ((tex_w - TEXTURE_CUT) / tex_w, 0.01),

        (0.99, TEXTURE_CUT / tex_h),
        (0.99, (tex_h - TEXTURE_CUT) / tex_h),

        ((tex_w - TEXTURE_CUT) / tex_w, 0.99),
        (TEXTURE_CUT / tex_w, 0.99),

        (0.01, (tex_h - TEXTURE_CUT) / tex_h),
        (0.01, TEXTURE_CUT / tex_h),
    ]

    surface = pg.Surface(CARD_SIZE)

    draw.Painter.scanline_texture(
        surface,
        card_p,
        uvs,
        texture
    )

    return surface

textures = {
    "AttackCard": {
        "front": pg.image.load("assets/textures/ATTACK_CARD.jpeg").convert_alpha(),
        "back": pg.image.load("assets/textures/ATTACK_CARD_BACK_VIEW.png").convert_alpha()
    },
    "MagicCard": {
        "front": {
            "Fire": pg.image.load("assets/textures/FIRE_MAGIC_CARD.png").convert_alpha(),
            "Thunder": pg.image.load("assets/textures/THUNDER_MAGIC_CARD.png").convert_alpha(),
            "Ice": pg.image.load("assets/textures/ICE_MAGIC_CARD.png").convert_alpha()
        },
        "back": pg.image.load("assets/textures/MAGIC_CARD_BACK_VIEW.png").convert_alpha()
    },
    "DefenseCard": {
        "front": pg.image.load("assets/textures/GREEN_CARD.png").convert_alpha(),
        "back": pg.image.load("assets/textures/GREEN_CARD_BACK_VIEW.png").convert_alpha()
    }
}

def _rasterize_cards_textures():
    rasterized = {}
    for card_type, card_data in textures.items():
        rasterized[card_type] = {}

        for side, texture in card_data.items():
            if isinstance(texture, dict):
                rasterized[card_type][side] = {}

                for name, tex in texture.items():
                    rasterized[card_type][side][name] = \
                        _rasterize_texture(tex)
            else:
                rasterized[card_type][side] = \
                    _rasterize_texture(texture)

    return rasterized

rasterized = _rasterize_cards_textures()

class Card(ABC):
    def __init__(
            self,
            color: str,
            value: int
    ) -> None:
        self.color = color
        self.value = value
        self.active = False
        self.play_order = -1

        if isinstance(self, MagicCard):
            self.front_surface = rasterized["MagicCard"]["front"][self.magic]
        else:
            self.front_surface = rasterized[self.__class__.__name__]["front"]
        self.back_surface = rasterized[self.__class__.__name__]["back"]

    @abstractmethod
    def play(self): ...

    def draw(self, screen: pg.Surface, pos: tuple[int,int], view: str="front") -> None:
        s = self.front_surface if view == "front" else self.back_surface
        number = card_font.render('9', True, BLACK)
        s.blit(number, (w//2 - 30, h - 130))
        screen.blit(s, pos)

class AttackCard(Card, ABC):
    def __init__(
            self,
            value: int
    ) -> None:
        super().__init__('red', value)
        self.att_dmg = 10

    @override
    def play(self):
        pass


class MagicCard(Card, ABC):
    def __init__(
            self,
            value: int,
            magic
    ) -> None:
        self.magic = magic
        super().__init__('blue', value)
        self.mg_dmg = 15

    @override
    def play(self):
        pass


class DefenseCard(Card, ABC):
    def __init__(
            self,
            value: int
    ) -> None:
        super().__init__('green', value)

    @override
    def play(self):
        pass


class CombinationCard(Card, ABC):
    def __init__(
            self,
            color: str,
            value: int
    ) -> None:
        super().__init__(color, value)

    @override
    def play(self): ...


class DeckNode:
    def __init__(
            self,
            card: Card,
            next_card: "DeckNode | None"=None,
            prev_card: "DeckNode | None"=None
    ) -> None:
        self.card = card
        self.next_card = next_card
        self.prev_card = prev_card
        self.active = True
        self.removed = True


def _construct_circular_list(cards: list[Card]) -> DeckNode:
    nodes = [DeckNode(card) for card in cards]

    n = len(cards)
    for i, node in enumerate(nodes):
        node.next_card = nodes[(i + 1) % n]
        node.prev_card = nodes[(i - 1) % n]

    return nodes[0]


class Deck:
    CARD_SPACING = 60

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.current = _construct_circular_list(cards)
        self.total_cards = len(cards)

    def reload(self) -> None:
        self.current = _construct_circular_list(self.cards)
        self.total_cards = len(self.cards)

    def next_card(self) -> None:
        self.current = self.current.next_card

    def prev_card(self) -> None:
        self.current = self.current.prev_card

    def remove_current(self) -> None:
        if self.total_cards > 1:
            next = self.current.next_card
            prev = self.current.prev_card
            next.prev_card = prev
            prev.next_card = next
            self.current = next

            self.total_cards -= 1
        else:
            self.current = None
            self.total_cards = 0

    def draw_visible(
            self,
            screen: pg.Surface,
            center: tuple[int, int]
    ) -> None:

        cx, cy = center

        half_w = CARD_SIZE[0] // 2
        half_h = CARD_SIZE[1] // 2

        positions = [
            (cx - self.CARD_SPACING - half_w, cy - half_h),
            (cx - half_w,                    cy - half_h),
            (cx + self.CARD_SPACING - half_w, cy - half_h)
        ]

        if self.current.prev_card is not None:
            self.current.prev_card.card.draw(
                screen,
                positions[0]
            )

        if self.current is not None:
            self.current.card.draw(
                screen,
                positions[1]
            )

        if self.current.next_card is not None:
            self.current.next_card.card.draw(
                screen,
                positions[2]
            )