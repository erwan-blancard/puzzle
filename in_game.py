import pygame

import game_state
import score_utils
import text
from game_state import GameState
from board import Board
from button import *


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((screen.get_width(), screen.get_height()))
    rect_over.set_alpha(200)
    rect_over.fill((255, 255, 255))
    screen.blit(rect_over, (0, 0))


class InGameState(GameState):

    def __init__(self, board_size=3, board_image: pygame.Surface = None):
        super().__init__()
        self.paused = False
        # buttons for pause menu
        self.buttons = [
            ButtonLabel("Continuer", 512 / 2 - 82, 512 / 2, 164, 48, command=lambda: self.close_pause_menu()),
            ButtonLabel("Recommencer", 512 / 2 - 120, 512 / 2 + 84, 240, 48, command=lambda: game_state.set_custom_ingame_state(board_size, board_image)),
            ButtonLabel("Quitter", 512 / 2 - 64, 512 / 2 + 168, 128, 48, command=lambda: game_state.set_state(game_state.MENU))
        ]

        piece_size = 64
        if piece_size*board_size > 300:
            piece_size = int(300 / board_size)

        self.board = Board(256, 256-piece_size, board_size, piece_size, board_image)
        self.turns = 0

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        self.board.render(screen)

        text.draw_aligned_text("Nombre de coups: "+str(self.turns), screen.get_width()/2, self.board.center_y + (len(self.board.pieces)*self.board.pieces[0][0].size)/2 + self.board.pieces[0][0].size, screen, pygame.font.Font(None, 24))

        if self.paused:
            render_overlay(screen)
            text.draw_centered_text("Pause", screen.get_width()/2, 92, screen, pygame.font.Font(None, 92))
            super().render(screen)

        if self.board.is_resolved():
            render_overlay(screen)
            text.draw_centered_text("Gagné !", screen.get_width()/2, screen.get_height()/4, screen, pygame.font.Font(None, 64))
            text.draw_centered_text("Vous avez réussi en "+str(self.turns)+" coups !", screen.get_width()/2, screen.get_height()/2, screen, pygame.font.Font(None, 32))

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if self.board.is_resolved():
                if key_name == "return":
                    if score_utils.get_scores(game_state.profile_name)[len(self.board.pieces) - 3] > self.turns:
                        score_utils.add_score(game_state.profile_name, len(self.board.pieces), self.turns)
                    game_state.set_state(game_state.MENU)
            else:
                if key_name == "escape":
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                if key_name == "up":
                    pos = self.board.get_empty_piece_pos()
                    if 0 <= pos[0] + 1 < len(self.board.pieces):
                        self.board.swap_pieces(pos, (pos[0] + 1, pos[1]))
                        self.turns += 1
                elif key_name == "down":
                    pos = self.board.get_empty_piece_pos()
                    if 0 <= pos[0] - 1 < len(self.board.pieces) - 1:
                        self.board.swap_pieces(pos, (pos[0] - 1, pos[1]))
                        self.turns += 1
                elif key_name == "left":
                    pos = self.board.get_empty_piece_pos()
                    if 0 <= pos[1] + 1 < len(self.board.pieces):
                        self.board.swap_pieces(pos, (pos[0], pos[1] + 1))
                        self.turns += 1
                elif key_name == "right":
                    pos = self.board.get_empty_piece_pos()
                    if 0 <= pos[1] - 1 < len(self.board.pieces):
                        self.board.swap_pieces(pos, (pos[0], pos[1] - 1))
                        self.turns += 1
        if self.paused:
            super().input(event)

    def close_pause_menu(self):
        self.paused = False
