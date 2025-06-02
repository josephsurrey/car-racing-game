import pygame
import settings


class UIManager:
    def __init__(
        self, font_name=None, font_size=36, text_color=settings.WHITE
    ):
        # Setup fonts
        try:
            self.default_font = pygame.font.Font(font_name, font_size)
            self.medium_font = pygame.font.Font(font_name, 48)
            self.large_font = pygame.font.Font(font_name, 72)
        except (pygame.error, FileNotFoundError):
            # Fallback to system font if custom font fails
            print(
                f"Warning: Font '{font_name}' not found or error loading."
                f" Using system 'arial'."
            )
            self.default_font = pygame.font.SysFont("arial", font_size)
            self.large_font = pygame.font.SysFont("arial", 72)
            self.medium_font = pygame.font.SysFont("arial", 48)

        # Set text colour, and setup screen dimensions
        self.text_color = text_color
        self.screen_width = settings.SCREEN_WIDTH
        self.screen_height = settings.SCREEN_HEIGHT

    def display_score(self, screen, score):
        score_text = f"Score: {score}"
        # Create score text surface
        surface = self.default_font.render(score_text, True, self.text_color)
        # Set score position
        rect = surface.get_rect()
        rect.topleft = (20, 20)
        # Draw to screen
        screen.blit(surface, rect)

    def display_high_score(self, screen, high_score):
        pass

    def display_game_over(self, screen, score, high_score):
        pass

    def display_message(self):
        pass
