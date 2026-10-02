from cards import Deck

class Player:
    def __init__(self, hp, dmg_s, def_s, deck):
        self.HP = hp
        self.DMG_S = dmg_s
        self.DEF_S = def_s
        self.deck = Deck(deck)
        self.stack = []

    def draw(self): ...

    def play_current_card(self):
        c = self.deck.current.card
        if c is not None:
            c.play()
            self.deck.remove_current()

    def play_stack(self): ...

    def stack_card(self):
        c = self.deck.current.card
        if c is not None:
            self.stack.append(c)

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

    def play_current_card(self):
        c = self.deck.current.card
        if c is not None:
            c.play()

    def draw(self): ...