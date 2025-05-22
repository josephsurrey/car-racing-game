import pygame


class Car(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

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

    def accelerate(self):
        pass

    def brake(self):
        pass

    def move_horizontal(self):
        pass


class NPCCar(Car):
    def __init__(self, npc_image_path, x_pos, speed):
        super().__init__()
        pass

    def update(self):
        super().update()
        pass