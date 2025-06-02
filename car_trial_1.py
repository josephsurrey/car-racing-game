import pygame
import settings


class Car(pygame.sprite.Sprite):
    def __init__(self, car_image, x_pos, y_pos, speed=0, is_npc=False):
        super().__init__()

        # Set speed variable
        self.speed = speed

        try:
            # Load the image for the car
            self.image = pygame.image.load(car_image).convert_alpha()

            original_width, original_height = self.image.get_size()

            # Calculate image aspect ratio
            aspect_ratio = original_height / original_width

            # Transform image to fit screen while maintaining aspect ratio
            self.image = pygame.transform.scale(
                self.image,
                (
                    settings.PLACEHOLDER_CAR_WIDTH,
                    settings.PLACEHOLDER_CAR_WIDTH * aspect_ratio,
                ),
            )

        # If there is an error loading the image, fall back to a placeholder
        except (pygame.error, FileNotFoundError):
            print(
                f"Warning: Could not load image {car_image}."
                f" Using placeholder."
            )
            colour = settings.BLUE if is_npc else settings.RED
            self.image = pygame.Surface(
                (
                    settings.PLACEHOLDER_CAR_WIDTH,
                    settings.PLACEHOLDER_CAR_HEIGHT,
                ),
                pygame.SRCALPHA,
            )
            self.image.fill(colour)

        # Set variables for the rect and create image mask
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        """
        Placeholder function. Actual code will be in subclasses
        """
        pass

    def draw(self):
        # Draw the car sprite onto the screen
        screen.blit(self.image, self.rect)


class PlayerCar(Car):
    def __init__(
        self, car_image, x_pos, y_pos, horizontal_acceleration_constant
    ):
        super().__init__(car_image, x_pos, y_pos, is_npc=False)
        # Setup Class variables
        self.initial_x_pos = x_pos
        self.initial_y_pos = y_pos
        self.horizontal_acceleration_constant = (
            horizontal_acceleration_constant
        )
        self.horizontal_speed = 0

    def update(self, screen_width):
        # If player is off the edge of the screen,
        # move back onto the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def move_horizontal(self, direction):
        # Moves the player horizontally (direction == -1 for left, 1 for right)
        self.horizontal_speed += (
            direction * self.horizontal_acceleration_constant
        )
        if self.horizontal_speed > settings.MAX_HORIZONTAL_SPEED:
            self.horizontal_speed = settings.MAX_HORIZONTAL_SPEED
        if self.horizontal_speed < -settings.MAX_HORIZONTAL_SPEED:
            self.horizontal_speed = -settings.MAX_HORIZONTAL_SPEED
        self.rect.centerx += self.horizontal_speed

    def reset_position(self):
        # Reset cars position to initial settings
        self.rect.centerx = self.initial_x_pos
        self.rect.centery = self.initial_y_pos


class NPCCar(Car):
    def __init__(self, npc_image_path, x_pos, y_pos, speed):
        super().__init__(npc_image_path, x_pos, y_pos, speed, is_npc=True)
        pass

    def update(self, road_speed, screen_height):
        # Change Y position by road speed - car speed
        self.rect.y += road_speed - self.speed

        # Kill NPC once it has left the screen
        if self.rect.top > screen_height:
            self.kill()
