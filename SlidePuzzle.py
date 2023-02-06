import pygame

import game_state
from menu import MenuState
from in_game import InGameState
from customize import CustomizeState
from scoreboard import ScoreBoardState

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Slide Puzzle")

game_state.state = 0
prev_state_id = 0
state = MenuState()


running = True

while running:

    # Update state
    if game_state.state != prev_state_id or game_state.force_update:
        if game_state.load_custom_ingame:
            game_state.load_custom_ingame = False
            prev_state_id = game_state.INGAME
            state = InGameState(board_size=game_state.board_size, board_image=game_state.board_image)
        elif game_state.state == game_state.MENU:
            prev_state_id = game_state.MENU
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            prev_state_id = game_state.INGAME
            state = InGameState()
        elif game_state.state == game_state.CUSTOMIZE:
            prev_state_id = game_state.CUSTOMIZE
            state = CustomizeState()
        elif game_state.state == game_state.SCOREBOARD:
            prev_state_id = game_state.SCOREBOARD
            state = ScoreBoardState()
        else:
            print("Invalid state id:", game_state.state)
        game_state.force_update = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        state.input(event)

    state.update()

    screen.fill((255, 255, 255))

    state.render(screen)

    pygame.display.flip()
