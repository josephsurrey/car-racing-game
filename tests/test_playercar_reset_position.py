import pygame
import pytest
from car import PlayerCar # Assuming car.py is in the same directory or PYTHONPATH
import settings # Assuming settings.py is accessible

# Minimal Pygame initialization for sprite loading/surface creation
pygame.init()

@pytest.fixture
def player_car_instance():
    # Provide dummy values required by PlayerCar constructor
    # Using a non-existent image path to trigger placeholder creation, simplifying test setup
    # Or provide a real path if an actual image is small and easy to include for tests
    car_image_path = "non_existent_player_car.png"
    initial_x = settings.PLAYER_START_X_POS
    initial_y = settings.PLAYER_Y_POS
    speed_constant = settings.HORIZONTAL_SPEED_CONSTANT
    car = PlayerCar(car_image_path, initial_x, initial_y, speed_constant)
    return car

def test_reset_position_after_move(player_car_instance):
    # Arrange: Get the car and its initial positions
    car = player_car_instance
    initial_x = car.initial_x_pos
    initial_y = car.initial_y_pos

    # Move the car to a new position
    car.rect.centerx = initial_x + 100
    car.rect.centery = initial_y - 50

    # Act: Reset the car's position
    car.reset_position()

    # Assert: Check if the car is back to its initial position
    assert car.rect.centerx == initial_x, "Car x position not reset correctly"
    assert car.rect.centery == initial_y, "Car y position not reset correctly"

def test_reset_position_when_at_initial(player_car_instance):
    # Arrange: Get the car, ensure it's at its initial position
    car = player_car_instance
    initial_x = car.initial_x_pos
    initial_y = car.initial_y_pos
    # Ensure it's at initial (should be by default after fixture creation)
    assert car.rect.centerx == initial_x
    assert car.rect.centery == initial_y

    # Act: Reset the car's position
    car.reset_position()

    # Assert: Check if the car remains at its initial position
    assert car.rect.centerx == initial_x, "Car x position changed from initial"
    assert car.rect.centery == initial_y, "Car y position changed from initial"