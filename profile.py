import game_state
from game_state import GameState
from button import *
import pygame
import text


class ProfileState(GameState):

    def __init__(self):
        super().__init__()
        self.buttons = [
            ButtonLabel("Valider le nom", 512/2 - 64, 512/2 + 128, 128, 48, pygame.font.Font(None, 32), command=lambda: self.validate_name())
        ]
        self.profile_name_in = game_state.profile_name
        self.warning_text = ""

    def validate_name(self):
        if len(self.profile_name_in) > 16:
            self.warning_text = "Le nom doit contenir au plus 16 charactères !"
        elif len(self.profile_name_in) >= 3:
            game_state.profile_name = self.profile_name_in
            game_state.set_state(game_state.MENU)
        else:
            self.warning_text = "Le nom doit contenir au moins 3 charactères !"
            
    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_centered_text("Profil", screen.get_width()/2, 64, screen, pygame.font.Font(None, 64))
        text.draw_centered_text(self.profile_name_in, screen.get_width()/2, screen.get_height()/2, screen, pygame.font.Font(None, 40))
        text.draw_centered_text(self.warning_text, screen.get_width()/2, screen.get_height()/2+72, screen, pygame.font.Font(None, 28), color=(255, 20, 20))
        
    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            inputed_letter = pygame.key.name(event.key)
            if inputed_letter == "escape":
                game_state.set_state(game_state.MENU)
            elif inputed_letter == "return":
                self.validate_name()
            elif inputed_letter == "backspace":
                self.profile_name_in = self.profile_name_in[:-1]
            else:
                if not len(self.profile_name_in) > 16:
                    is_letter = False
                    for letter in "abcdefghijklmnopqrstuvwxyz":
                        if inputed_letter == letter:
                            is_letter = True
                            break
                    if is_letter:
                        self.profile_name_in += inputed_letter
        super().input(event)
