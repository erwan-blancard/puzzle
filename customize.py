import os

import game_state
from game_state import GameState
from button import *
from board import Board
import pygame
import tkinter.filedialog


MAX_ALLOWED_BOARD_SIZE = 9
MAX_BOARD_WIDTH = 164


class CustomizeState(GameState):

    def __init__(self):
        super().__init__()

        self.custom_board_size = 3
        self.preview_board = Board(164, 184, board_size=self.custom_board_size, piece_size=int(MAX_BOARD_WIDTH/self.custom_board_size), shuffle=False)
        self.custom_board_image: pygame.Surface = None
        self.buttons = [
            ButtonIcon(164-64, 256+32, 32, pygame.image.load("res/remove.png"), command=lambda: self.decrement()),
            ButtonIcon(164+32, 256+32, 32, pygame.image.load("res/add.png"), command=lambda: self.increment()),
            ButtonLabel("Choisir une image...", 256 + 56, 256+40, 156, 24, pygame.font.Font(None, 24), command=lambda: self.ask_new_image()),
            ButtonLabel("Jouer avec ces paramètres", 256 - 82, 512-92, 164, 32, pygame.font.Font(None, 32), command=lambda: game_state.set_custom_ingame_state(size=self.custom_board_size, img=self.custom_board_image))
        ]

    def increment(self):
        if self.custom_board_size + 1 <= MAX_ALLOWED_BOARD_SIZE:
            self.custom_board_size += 1
            self.preview_board = Board(164, 184, board_size=self.custom_board_size, piece_size=int(MAX_BOARD_WIDTH/self.custom_board_size), shuffle=False, board_image=self.custom_board_image)

    def decrement(self):
        if self.custom_board_size - 1 >= 3:
            self.custom_board_size -= 1
            self.preview_board = Board(164, 184, board_size=self.custom_board_size, piece_size=int(MAX_BOARD_WIDTH/self.custom_board_size), shuffle=False, board_image=self.custom_board_image)

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        self.preview_board.render(screen)
        if self.custom_board_image is not None:
            custom_image = pygame.transform.scale(self.custom_board_image, (MAX_BOARD_WIDTH, MAX_BOARD_WIDTH))
            screen.blit(custom_image, (256+48, 184-MAX_BOARD_WIDTH/2))
        else:
            text.draw_centered_text("Pas d'image", 256+48+MAX_BOARD_WIDTH/2, 92+MAX_BOARD_WIDTH/2, screen, pygame.font.Font(None, 32))
        text.draw_centered_text(str(self.custom_board_size) + "x" + str(self.custom_board_size), 164, 256+32+16, screen, font=pygame.font.Font(None, 32))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)

    def ask_new_image(self):
        filepath = tkinter.filedialog.askopenfilename()
        if os.path.splitext(filepath)[1][1:].lower() == "png" or os.path.splitext(filepath)[1][1:].lower() == "jpg" or os.path.splitext(filepath)[1][1:].lower() == "jpeg":
            self.custom_board_image = pygame.image.load(filepath)
            self.preview_board = Board(164, 184, board_size=self.custom_board_size, piece_size=int(MAX_BOARD_WIDTH/self.custom_board_size), shuffle=False, board_image=self.custom_board_image)