import pygame
import game_state
from game_state import GameState
from button import ButtonLabel


class MenuState(GameState):

    def __init__(self):
        super().__init__()
        self.buttons += [
            ButtonLabel("Jouer", 64, 512 / 2 + 60, 128, 48, command=lambda: game_state.set_state(game_state.INGAME)),
            ButtonLabel("Personnaliser...", 512/2+24, 512 / 2 + 64, 220, 40, font=pygame.font.Font(None, 40), command=lambda: game_state.set_state(game_state.CUSTOMIZE)),
            ButtonLabel("Scoreboard", 512/2 - 80, 512 / 2 + 148, 160, 48, command=lambda: game_state.set_state(game_state.SCOREBOARD))
        ]

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def input(self, event: pygame.event.Event):
        super().input(event)
