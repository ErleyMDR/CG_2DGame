import pygame as pg

import engine.draw as draw

WIDTH: int = 1280
HEIGHT: int = 720

RED: tuple[int, int, int] = (200, 0, 0)
GREEN: tuple[int, int, int] = (0, 200, 0)
BLUE: tuple[int, int, int] = (0, 0, 200)

class Game:
    def __init__(self):
        # pygame setup
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

    def __repr__(self):
        return "RTCB - Real Time Card Battle. Made by Erley Monteiro"

    def run(self):
        own = True
        pygames = True
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        own = not own
                    elif event.key == pg.K_2:
                        pygames = not pygames

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER YOUR GAME HERE
            if own: draw.polygon(self.screen, [(100, 200), (300, 450), (450, 300)], color=RED)
            if pygames: pg.draw.polygon(self.screen, points=[(100, 200), (300, 450), (450, 300)], color=GREEN)
            # flip() the display to put your work on screen
            pg.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pg.quit()

if __name__ == '__main__':
    game = Game()
    print("Starting game... ")
    game.run()