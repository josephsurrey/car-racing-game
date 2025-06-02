import pygame
import settings


class Road:
    def __init__(self, road_image, screen_width, screen_height):
        # Define screen width and height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Try to load road image
        try:
            # Load image and convert
            self.image = pygame.image.load(road_image).convert()

            # Get image dimensions
            original_width, original_height = self.image.get_size()

            # Calculate image aspect ratio
            aspect_ratio = original_width / original_height

            # Transform image to fit screen while maintaining aspect ratio
            self.image = pygame.transform.scale(
                self.image,
                (self.screen_width, self.screen_width * aspect_ratio),
            )

            self.image_height = self.image.get_height()

            # Create two rectangles for scrolling
            self.rect1 = self.image.get_rect(topleft=(0, 0))
            self.rect2 = self.image.get_rect(topleft=(0, -self.image_height))

        # If image fails to load
        except (pygame.error, FileNotFoundError):
            print(
                f"Warning: Could not load road image '{road_image}'."
                f" Creating placeholder."
            )

            # Create a placeholder surface
            self.image_original = pygame.Surface(
                (self.screen_width, self.screen_height)
            )
            self.image_original.fill(settings.BLACK)

    def update(self, current_road_speed):
        # Move rects based on road speed
        self.rect1.y += current_road_speed
        self.rect2.y += current_road_speed

        # Scrolling functionality
        if self.rect1.top >= self.image_height:
            self.rect1.top = self.rect2.top - self.image_height
        if self.rect2.top >= self.image_height:
            self.rect2.top = self.rect1.top - self.image_height

    def draw(self, screen):
        # Draw both rects to the screen
        screen.blit(self.image, self.rect1)
        screen.blit(self.image, self.rect2)
