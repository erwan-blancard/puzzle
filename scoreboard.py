import pygame
import game_state
import text
from game_state import GameState
import score_utils
from scrolling_list import ScrollingList


class ScoreBoardState(GameState):

    def __init__(self):
        super().__init__()

        self.scrolling_list = ScrollingList(32, 128, 512-64, 360)
        self.score_list_formatted = []
        self.load_scores()

    def load_scores(self):
        profile_list = []
        profiles = score_utils.get_profiles()
        if profiles is not None:
            for profile_name in profiles:
                profile_list.append(profile_name)
        for profile in profile_list:
            scores = score_utils.get_scores(profile)
            string_formatted = profile
            for i in range(16 - len(profile)):
                string_formatted += " "
            for i in range(len(scores)):
                score_str = str(scores[i])
                for j in range(5-len(score_str)):
                    score_str += " "
                string_formatted += ("|" + score_str[0:5])
            self.score_list_formatted.append(string_formatted)

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_centered_text("Tableau des scores", screen.get_width()/2, 64, screen, pygame.font.Font(None, 64))
        text.draw_text_individual("Nom             "+"|"+"3x3  "+"|"+"4x4  "+"|"+"5x5  "+"|"+"6x6  "+"|"+"7x7  "+"|"+"8x8  "+"|"+"9x9  ", 34, 128-16, screen, pygame.font.Font(None, 20))
        self.scrolling_list.render(screen, self.score_list_formatted, pygame.font.Font(None, 20))

    def input(self, event: pygame.event.Event):
        super().input(event)
        self.scrolling_list.mouse_input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)
