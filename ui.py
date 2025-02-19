import pygame
from config import FONT, DARKGREY, LIGHTGREY, BLACK, WHITE

class Button:
    # Interactive button.
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.background_color = DARKGREY
        self.hover_color = WHITE
        self.text = text
        self.text_color = BLACK
        self.text_surface = FONT.render(text, True, self.text_color)

    def handle_event(self, event):
        # Returns True if the button is clicked.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface, mouse_pos):
        # Draw the button with a hover effect.
        color = self.background_color if self.rect.collidepoint(mouse_pos) else self.hover_color
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))


class InputBox:
    # Input box for modifying parameters.
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = LIGHTGREY
        self.color_active = DARKGREY
        self.color = self.color_inactive
        self.text = text
        self.text_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        Handles events:
            - CLICK to activate/deactivate
            - KEYDOWN to update the text
        Returns the text when the Enter key is pressed.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activate if the click is inside the box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                text = self.text
                self.text = ''
                self.text_surface = FONT.render(self.text, True, self.color)
                return text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = FONT.render(self.text, True, self.color)
        return None

    def draw(self, surface):
        # Draw the input box and its text.
        surface.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)
