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

            # Setup floats for y position to make scrolling more accurate
            self.y1_float = 0.0
            self.y2_float = 0.0 - self.image_height

            # Create two rectangles for scrolling
            self.rect1 = self.image.get_rect(topleft=(0, int(self.y1_float)))
            self.rect2 = self.image.get_rect(topleft=(0, int(self.y2_float)))

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
        self.y1_float += current_road_speed
        self.y2_float += current_road_speed
        self.rect1.y = int(self.y1_float)
        self.rect2.y = int(self.y2_float)

        # Scrolling functionality
        if self.rect1.top >= self.screen_height:
            self.y1_float = self.y2_float - self.image_height
            self.rect1.y = int(self.y1_float)
        elif self.rect2.top >= self.screen_height:
            self.y2_float = self.y1_float - self.image_height
            self.rect2.y = int(self.y2_float)

    def draw(self, screen):
        # Draw both rects to the screen
        screen.blit(self.image, self.rect1)
        screen.blit(self.image, self.rect2)
