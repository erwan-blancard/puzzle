import pygame
import text
from game_state import GameState
from board import Board


class InGameState(GameState):

    def __init__(self, board_size=3, board_image: pygame.Surface = None):
        super().__init__()

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

        if self.board.is_resolved():
            text.draw_text("Puzzle résolu !", 0, 100, screen, pygame.font.Font(None, 24))

        super().render(screen)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
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
        super().input(event)










