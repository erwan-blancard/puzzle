import pygame
import button

# Holds the current state ID of the game
state = 0
force_update = False

load_custom_ingame = False
board_size = 3
board_image: pygame.Surface = None


MENU = 0
INGAME = 1
CUSTOMIZE = 2
SCOREBOARD = 3


def set_state(newstate, force=False):
    global state
    global force_update
    state = newstate
    force_update = force


def set_custom_ingame_state(size, img: pygame.Surface):
    global load_custom_ingame
    global board_size
    global board_image
    board_size = size
    board_image = img
    load_custom_ingame = True
    set_state(INGAME, force=True)


# base class for states with basic button support
class GameState:
    def __init__(self):
        self.buttons: list[button.BaseButton] = []

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)

    def input(self, event: pygame.event.Event):
        for button in self.buttons:
            button.mouse_input(event)
