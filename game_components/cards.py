from abc import ABC, abstractmethod
from typing import override

from engine import draw

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

    @abstractmethod
    def play(self): ...

    def draw(self) -> None:
        ...


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

class Deck:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.current = self._construct_circular_list(cards)
        self.total_cards = len(cards)

    def _construct_circular_list(self, cards: list[Card]) -> DeckNode:
        nodes = [DeckNode(card) for card in cards]

        n = len(cards)
        for i, node in enumerate(nodes):
            node.next_card = nodes[(i + 1) % n]
            node.prev_card = nodes[(i - 1) % n]

        return nodes[0]

    def reload(self) -> None:
        self.current = self._construct_circular_list(self.cards)

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