import pygame
import settings


class Car(pygame.sprite.Sprite):
    def __init__(
        self, car_image, x_pos, y_pos, is_npc
    ):
        super().__init__()
        try:
            # Load the image for the car
            self.image = pygame.image.load(car_image).convert_alpha()
        # If there is an error loading the image, fall back to a placeholder
        except pygame.error:
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
    def __init__(self, car_image, x_pos, y_pos, horizontal_speed_constant):
        super().__init__(car_image, x_pos, y_pos, is_npc=False)
        # Setup Class variables
        self.initial_x_pos = x_pos
        self.initial_y_pos = y_pos
        self.horizontal_speed_constant = horizontal_speed_constant


    def update(self):
        super().update()
        pass

    def move_horizontal(self, horizontal_speed):
        pass

    def reset_position(self):
        pass


class NPCCar(Car):
    def __init__(self, npc_image_path, x_pos, y_pos, speed):
        super().__init__()
        pass

    def update(self):
        super().update()
        pass
