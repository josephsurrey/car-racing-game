import pygame
import settings


class Car(pygame.sprite.Sprite):
    def __init__(
        self, car_image, x_pos, y_pos, horizontal_speed_constant, is_npc
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
                    settings.PLACEHOLDER_NPC_WIDTH,
                    settings.PLACEHOLDER_NPC_HEIGHT,
                ),
                pygame.SRCALPHA,
            )
            self.image.fill(colour)

        # Set variables for the rect and create image mask
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def draw(self):
        pass


class PlayerCar(Car):
    def __init__(self, car_image, x_pos, y_pos, horizontal_speed_constant):
        super().__init__()
        pass

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
