import pygame as pg


from engine import draw
from game_components.hud import Hud
from game_components.entities import *
from menu import Menu
from game_components.scenario import Scenario

FPS: int = 60
WIDTH: int = 1820
HEIGHT: int = 920
FONT: str = 'Serif'
FONT_SIZE: int = 12

BLACK: tuple[int,int,int] = (0,0,0)
WHITE: tuple[int,int,int] = (255,255,255)
RED: tuple[int, int, int] = (200, 0, 0)
GREEN: tuple[int, int, int] = (0, 200, 0)
BLUE: tuple[int, int, int] = (0, 0, 200)
YELLOW: tuple[int,int,int] = (215, 215, 40)

class Game:
    def __init__(self):
        # pygame setup
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.SysFont(FONT, FONT_SIZE)
        pg.display.set_caption(self.__repr__())

        # Estado do Jogo
        self.state = "TEST"

        self.is_debug_mode = True
        self.player = None
        self.enemy = None
        # self.hud = Hud(self.player, self.enemy)
        self.scenario = Scenario()

    def __repr__(self):
        return "RTCB - Real Time Card Battle"

    def generate_cards(self):
        cards = []

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
            if self.state == "MENU":
                Menu.show(self.screen)

            elif self.state == "PLAYING":
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
            self.screen.fill(BLACK)

            # RENDER YOUR GAME HERE
            self.scenario.draw(self.screen)
            # self.hud.draw(self.screen)
            # draw.half_ellipse(self.screen, (WIDTH//2, HEIGHT//2),200, 150, WHITE, direction='east')
            # Calls debug_mode() if active
            if self.is_debug_mode: self.debug_mode()

            # flip() the display to put your work on screen
            pg.display.flip()

            self.clock.tick(FPS)  # limits FPS to 60

        pg.quit()