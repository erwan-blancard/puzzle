import pygame
import text


class Piece:

    def __init__(self, size, ID, image: pygame.Surface = None, empty=None):
        self.size = size
        self.ID = ID
        if image is not None and (image.get_width() != size or image.get_height() != size):
            image = pygame.transform.scale(image, (size, size))
        self.image = image
        self.empty = empty

    def render(self, x, y, screen: pygame.Surface):
        if self.image is not None:
            screen.blit(self.image, (x, y))
            # draw outlines
            pygame.draw.rect(screen, (0, 0, 0), (x, y, self.size, self.size), width=1)
            if self.empty:
                rect_over = pygame.Surface((self.size, self.size))
                rect_over.set_alpha(180)
                rect_over.fill((150, 150, 150))
                screen.blit(rect_over, (x, y))

        elif not self.empty:
            piece_surface = pygame.Surface((self.size, self.size), flags=pygame.SRCALPHA)
            pygame.draw.rect(piece_surface, (255, 255, 255), (1, 1, self.size-2, self.size-2), border_radius=2)
            pygame.draw.rect(piece_surface, (20, 20, 20), (0, 0, self.size, self.size), width=2, border_radius=4)
            text.draw_centered_text(str(self.ID+1), self.size / 2, self.size / 2, piece_surface, pygame.font.Font(None, self.size))
            screen.blit(piece_surface, (x, y))

    def get_ID(self):
        return self.ID

    def is_empty(self):
        return self.empty
