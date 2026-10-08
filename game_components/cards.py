import pygame as pg
from abc import ABC, abstractmethod
from typing import override

BLACK = (0, 0, 0)
CARD_FONT_PATH: str = "assets/font/PressStart2P-Regular.ttf"
CARD_FONT_SIZE: int = 12  # Ajustado para caber perfeitamente no meio círculo

CARD_SIZE = (50, 100)
TEXTURE_CUT = 20

# Dicionário global que será preenchido SOMENTE após o pg.display.set_mode()
RASTERIZED_TEXTURES = {}
card_font: pg.font.Font | None = None


def init_card_system():
    """Deve ser chamado obrigatoriamente APÓS pg.display.set_mode()"""
    global RASTERIZED_TEXTURES, card_font
    card_font = pg.font.Font(CARD_FONT_PATH, CARD_FONT_SIZE)
    RASTERIZED_TEXTURES = _rasterize_cards_textures()


def _rasterize_texture(texture: pg.Surface) -> pg.Surface:
    from engine import draw

    card_w, card_h = CARD_SIZE
    tex_w, tex_h = texture.get_size()

    cx = card_w // 2
    cy = card_h // 2

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

    surface = pg.Surface(CARD_SIZE, pg.SRCALPHA)
    draw.Painter.scanline_texture(surface, card_p, uvs, texture)
    return surface


def _rasterize_cards_textures() -> dict:
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

    rasterized = {}
    for card_type, card_data in textures.items():
        rasterized[card_type] = {}
        for side, texture in card_data.items():
            if isinstance(texture, dict):
                rasterized[card_type][side] = {
                    name: _rasterize_texture(tex) for name, tex in texture.items()
                }
            else:
                rasterized[card_type][side] = _rasterize_texture(texture)

    return rasterized


class Card(ABC):
    def __init__(self, color: str, value: int) -> None:
        self.color = color
        self.value = value
        self.active = False
        self.play_order = -1

        # Cache da superfície final com o número renderizado
        self._cached_front: pg.Surface | None = None
        self._cached_back: pg.Surface | None = None

    @abstractmethod
    def get_front_surface(self) -> pg.Surface:
        """Retorna a textura base limpa (sem o número)."""
        ...

    def get_back_surface(self) -> pg.Surface:
        return RASTERIZED_TEXTURES[self.__class__.__name__]["back"]

    def _build_card_surface(self, base_s: pg.Surface) -> pg.Surface:
        """Gera a imagem final combinando a textura com o valor impresso no meio círculo inferior."""
        s = base_s.copy()
        if card_font is not None:
            number = card_font.render(str(self.value), True, BLACK)
            # Posiciona o número centralizado no meio círculo na base da carta
            rect = number.get_rect(center=(CARD_SIZE[0] // 2, CARD_SIZE[1] - 14))
            s.blit(number, rect)
        return s

    def get_rendered_front(self) -> pg.Surface:
        if self._cached_front is None:
            self._cached_front = self._build_card_surface(self.get_front_surface())
        return self._cached_front

    def get_rendered_back(self) -> pg.Surface:
        if self._cached_back is None:
            self._cached_back = self._build_card_surface(self.get_back_surface())
        return self._cached_back

    @abstractmethod
    def play(self): ...

    def start(self, owner): ...
    def resolve(self, owner): ...
    def cancel(self, owner): ...

    def draw(self, screen: pg.Surface, pos: tuple[int, int], view: str = "front") -> None:
        s = self.get_rendered_front() if view == "front" else self.get_rendered_back()
        screen.blit(s, pos)


class AttackCard(Card):
    def __init__(self, value: int) -> None:
        super().__init__('red', value)
        self.att_dmg = 10

    @override
    def get_front_surface(self) -> pg.Surface:
        return RASTERIZED_TEXTURES["AttackCard"]["front"]

    @override
    def play(self): pass

    @override
    def start(self, owner):
        owner.state = "attacking"

    @override
    def resolve(self, owner):
        pass

    @override
    def cancel(self, owner):
        owner.state = "idle"


class MagicCard(Card):
    def __init__(self, value: int, magic: str) -> None:
        self.magic = magic
        super().__init__('blue', value)
        self.mg_dmg = 15

    @override
    def get_front_surface(self) -> pg.Surface:
        return RASTERIZED_TEXTURES["MagicCard"]["front"][self.magic]

    @override
    def play(self): pass

    @override
    def start(self, owner):
        owner.state = "casting"

    @override
    def resolve(self, owner):
        pass

    @override
    def cancel(self, owner):
        owner.state = "idle"


class DefenseCard(Card):
    def __init__(self, value: int) -> None:
        super().__init__('green', value)

    @override
    def get_front_surface(self) -> pg.Surface:
        return RASTERIZED_TEXTURES["DefenseCard"]["front"]

    @override
    def play(self): pass

    @override
    def start(self, owner):
        owner.state = "defending"

    @override
    def resolve(self, owner):
        pass

    @override
    def cancel(self, owner):
        owner.state = "idle"


class ActiveCard:
    def __init__(self, card: Card, owner, start_time: int):
        self.card = card
        self.owner = owner
        self.start_time = start_time
        self.active = True

    def interrupt(self):
        if not self.active:
            return
        self.active = False
        self.card.cancel(self.owner)
        if hasattr(self.owner, 'cancel_action'):
            self.owner.cancel_action()

    def finish(self):
        if not self.active:
            return
        self.active = False
        self.card.resolve(self.owner)
        if hasattr(self.owner, 'finish_action'):
            self.owner.finish_action()


class DeckNode:
    def __init__(
            self,
            card: Card,
            next_card: "DeckNode | None" = None,
            prev_card: "DeckNode | None" = None
    ) -> None:
        self.card = card
        self.next_card = next_card
        self.prev_card = prev_card
        self.active = True


def _construct_circular_list(cards: list[Card]) -> DeckNode:
    nodes = [DeckNode(card) for card in cards]
    n = len(cards)
    for i, node in enumerate(nodes):
        node.next_card = nodes[(i + 1) % n]
        node.prev_card = nodes[(i - 1) % n]
    return nodes[0]


class Deck:
    CARD_SPACING = 75  # Aumentado para dar mais espaçamento entre as cartas
    ELEVATION = 20     # Altura em pixels que a carta selecionada fica suspensa

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.current = _construct_circular_list(cards) if cards else None
        self.total_cards = len(cards)

    def reload(self) -> None:
        if self.cards:
            self.current = _construct_circular_list(self.cards)
            self.total_cards = len(self.cards)

    def next_card(self) -> None:
        if self.current:
            self.current = self.current.next_card

    def prev_card(self) -> None:
        if self.current:
            self.current = self.current.prev_card

    def remove_current(self) -> None:
        if self.total_cards > 2 and self.current:
            next_node = self.current.next_card
            prev_node = self.current.prev_card
            next_node.prev_card = prev_node
            prev_node.next_card = next_node
            self.current = next_node
            self.total_cards -= 1
        elif self.total_cards == 1:
            next_node = self.current.next_card
            next_node.prev_card = None
            next_node.next_card = None
            self.current = next_node
            self.total_cards -= 1
        else:
            self.current = None
            self.total_cards = 0

    def draw_visible(self, screen: pg.Surface, center: tuple[int, int]) -> None:
        if not self.current:
            return

        cx, cy = center
        half_w = CARD_SIZE[0] // 2
        half_h = CARD_SIZE[1] // 2

        # A carta atual (do meio) é desenhada subtraindo self.ELEVATION no eixo Y
        positions = [
            (cx - self.CARD_SPACING - half_w, cy - half_h),
            (cx - half_w, cy - half_h - self.ELEVATION),
            (cx + self.CARD_SPACING - half_w, cy - half_h)
        ]

        if self.current.prev_card:
            self.current.prev_card.card.draw(screen, positions[0])

        # Renderiza a carta ativa no centro com elevação
        self.current.card.draw(screen, positions[1])

        if self.current.next_card:
            self.current.next_card.card.draw(screen, positions[2])