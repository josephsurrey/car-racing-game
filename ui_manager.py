import pygame
import settings


class UIManager:
    def __init__(
        self, font_name=None, font_size=36, text_colour=settings.WHITE
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
        self.text_colour = text_colour
        self.screen_width = settings.SCREEN_WIDTH
        self.screen_height = settings.SCREEN_HEIGHT

    def display_score(self, screen, score):
        score_text = f"Score: {score}"
        # Create score text surface
        surface = self.default_font.render(score_text, True, self.text_colour)
        # Set score position
        rect = surface.get_rect()
        rect.topleft = (40, 20)
        # Draw to screen
        screen.blit(surface, rect)

    def display_high_score(self, screen, high_score):
        high_score_text = f"High Score: {high_score}"
        # Create high score text surface
        surface = self.default_font.render(
            high_score_text, True, self.text_colour
        )
        # Set high score position
        rect = surface.get_rect()
        rect.topright = (self.screen_width - 40, 20)
        # Draw to screen
        screen.blit(surface, rect)

    def display_game_over(self, screen, score, high_score):
        # Translucent overlay to make text easier to read
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Render "GMAE OVER" text
        game_over_text = "GAME OVER"
        game_over_surface = self.large_font.render(
            game_over_text, True, settings.RED
        )
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (
            int(self.screen_width / 2),
            int(self.screen_height / 2 - 100),
        )
        screen.blit(game_over_surface, game_over_rect)

        # Render "Final Score: " text
        final_score_text = f"Final Score: {score}"
        final_score_surface = self.medium_font.render(
            final_score_text, True, self.text_colour
        )
        final_score_rect = final_score_surface.get_rect()
        final_score_rect.center = (
            int(self.screen_width / 2),
            int(self.screen_height / 2),
        )
        screen.blit(final_score_surface, final_score_rect)

        # Render "High Score: " text
        high_score_display_text = f"High Score: {high_score}"
        high_score_surface = self.medium_font.render(
            high_score_display_text, True, self.text_colour
        )
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.center = (
            int(self.screen_width / 2),
            int(self.screen_height / 2 + 60),
        )
        screen.blit(high_score_surface, high_score_rect)

        # Render "Press R to Restart" text
        restart_text = "Press R to Restart"
        restart_surface = self.default_font.render(
            restart_text, True, settings.GREEN
        )
        restart_rect = restart_surface.get_rect()
        restart_rect.center = (
            int(self.screen_width / 2),
            int(self.screen_height / 2 + 130),
        )
        screen.blit(restart_surface, restart_rect)
