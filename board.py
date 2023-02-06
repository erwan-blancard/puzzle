import pygame
import random
from piece import Piece


class Board:

    def __init__(self, center_x, center_y, board_size=3, piece_size=64, board_image: pygame.Surface = None, shuffle=True):
        self.center_x = center_x
        self.center_y = center_y
        self.pieces: list[list[Piece]] = []
        self.create_board(board_size, piece_size, board_image, shuffle=shuffle)

    def render(self, screen: pygame.Surface):
        board_size = len(self.pieces)
        piece_size = self.pieces[0][0].size
        x = self.center_x - (piece_size * board_size)/2
        y = self.center_y - (piece_size * board_size)/2
        # render background
        stroke = 2
        pygame.draw.rect(
            screen, (0, 0, 0),
            (x - stroke, y - stroke, piece_size * board_size + (stroke * 2), piece_size * board_size + (stroke * 2)),
            width=stroke, border_radius=stroke*2
        )
        pygame.draw.rect(
            screen, (200, 200, 200),
            (x, y, piece_size * board_size, piece_size * board_size),
            border_radius=stroke
        )

        for row in range(board_size):
            for col in range(board_size):
                self.pieces[row][col].render(x + (col * piece_size), y + (row * piece_size), screen)

    def create_board(self, size, piece_size=32, board_image: pygame.Surface = None, shuffle=True):
        custom_image = board_image
        if board_image is not None:
            custom_image = pygame.transform.scale(board_image, (piece_size*size, piece_size*size))
        self.pieces = []
        for row in range(size):
            self.pieces.append([])
            for col in range(size):
                img = None
                if custom_image is not None:
                    img = pygame.Surface((piece_size, piece_size), flags=pygame.SRCALPHA)
                    img.blit(custom_image, (0, 0), (col*piece_size, row*piece_size, piece_size, piece_size))
                if (row + 1) ** (col + 1) != size ** size:
                    self.pieces[row].append(Piece(piece_size, col + row * size, image=img))
                else:
                    # leave empty tile at the end of the board
                    self.pieces[row].append(Piece(piece_size, col + row * size, image=img, empty=True))
        if shuffle:
            self.shuffle_board()

    def shuffle_board(self, already_shuffled=False):
        linear_board = []
        board_size = len(self.pieces)
        for row in range(board_size):
            for col in range(board_size):
                linear_board.append(self.pieces[row][col])
        random.shuffle(linear_board)
        for i in range(len(linear_board)):
            self.pieces[i // board_size][i % board_size] = linear_board[i]

        # if the board is resolved after being shuffled, it gets re-shuffled
        if self.is_resolved():
            # if resolved 2 times in a row, swaps 2 pieces
            if already_shuffled:
                self.swap_pieces((0, 0), (board_size - 1, board_size - 1))
            else:
                self.shuffle_board(already_shuffled=True)

    def swap_pieces(self, piece_pos1, piece_pos2):
        piece1 = self.pieces[piece_pos1[0]][piece_pos1[1]]
        piece2 = self.pieces[piece_pos2[0]][piece_pos2[1]]
        self.pieces[piece_pos1[0]][piece_pos1[1]] = piece2
        self.pieces[piece_pos2[0]][piece_pos2[1]] = piece1

    def get_empty_piece_pos(self):
        board_size = len(self.pieces)
        for row in range(board_size):
            for col in range(board_size):
                if self.pieces[row][col].is_empty():
                    return row, col

    def is_resolved(self):
        completed = True
        for row in range(len(self.pieces)):
            if not completed:
                break
            for col in range(len(self.pieces)):
                if col + (row * len(self.pieces)) != self.pieces[row][col].get_ID():
                    completed = False
                    break
        return completed
