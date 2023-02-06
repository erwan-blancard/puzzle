import pygame
import game_state
import text
from game_state import GameState


class ScoreBoardState(GameState):

    def __init__(self):
        super().__init__()

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_centered_text("Pas implémenté !", screen.get_width()/2, screen.get_height()/2, screen, pygame.font.Font(None, 48))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)
