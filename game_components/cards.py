import pygame as pg

from abc import ABC, abstractmethod
from typing import override

from engine import draw

CARD_SIZE = (50, 100)
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}

sprites = {
    "AttackCard": {"front": "assets/ATTACK_CARD.png", "back": "assets/ATTACK_CARD_BACK_VIEW.png"},
    "MagicCard": {
        "front": {"Fire": "assets/FIRE_MAGIC_CARD.png",
                 "Thunder": "assets/THUNDER_MAGIC_CARD.png",
                 "Ice": "assets/ICE_MAGIC_CARD.png"},
        "back": "assets/MAGIC_CARD_BACK_VIEW.png"
    },
    "DefenseCard": {"front": "assets/GREEN_CARD.png", "back": "assets/GREEN_CARD_BACK_VIEW.png"}
}

range_types = {
    "straight_line": draw.Rasterizer.rectangle,
    "reuleaux": draw.Rasterizer.reuleaux_triangle
}

class Card(ABC):
    def __init__(
            self,
            color: str,
            value: int,
            range_type: str | None
    ) -> None:
        self.color = color
        self.value = value
        self.range_type = range_type
        self.surface = self.rasterize()

    @abstractmethod
    def play(self): ...

    def rasterize(self) -> pg.Surface:
        s = pg.Surface(CARD_SIZE)
        cx, cy = s.get_width()//2, s.get_height()//2

        draw.Rasterizer.rectangle(s, (cx, cy), CARD_SIZE[0], CARD_SIZE[1], colors[self.color])
        return s

    def draw(self, screen: pg.Surface, pos: tuple[int,int]) -> None:
        screen.blit(self.surface, pos)


class AttackCard(Card, ABC):
    def __init__(
            self,
            value: int,
    ) -> None:
        super().__init__('red', value)
        self.att_dmg = 10

    @override
    def play(self): ...


class MagicCard(Card, ABC):
    def __init__(
            self,
            value: int,
            range_type: str
    ) -> None:
        super().__init__('blue', value, range_type)

    @override
    def play(self): ...


class DefenseCard(Card, ABC):
    def __init__(
            self,
            value: int
    ) -> None:
        super().__init__('green', value)

    @override
    def play(self): ...


class CombinationCard(Card, ABC):
    def __init__(
            self,
            color: str,
            value: int,
            range_type: str | None
    ) -> None:
        super().__init__(color, value, range_type)

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
        next = self.current.next_card
        prev = self.current.prev_card
        next.prev_card = prev
        prev.next_card = next
        self.current = next

        self.total_cards -= 1

    def draw_visible(self, screen: pg.Surface) -> pg.Surface:
        ...