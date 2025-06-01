import pygame
import pytest

# Assuming car.py and settings.py are in the python path or same directory
from car import PlayerCar
import settings

# Initialize Pygame as Car class and its derivatives use pygame features
# like Sprites, Surface, and Mask, which require pygame to be initialized
pygame.init()


@pytest.fixture
def player_car_instance():
    # Use a non-existent image path to trigger placeholder image creation in Car.__init__
    # This avoids dependency on actual asset files for this unit test
    # The placeholder image is sufficient as we are testing movement logic, not rendering
    img_path = "non_existent_player_car_for_test.png"

    # Set an initial position for the test car using values from settings
    start_x = settings.SCREEN_WIDTH // 2
    start_y = settings.PLAYER_Y_POS

    # Initialize the car with the horizontal speed constant from settings
    # This value is stored in the PlayerCar instance as self.horizontal_speed_constant
    speed_const = settings.HORIZONTAL_SPEED_CONSTANT

    car = PlayerCar(img_path, start_x, start_y, speed_const)
    return car


def test_move_horizontal_left(player_car_instance):
    # Record the car's initial x position
    initial_x = player_car_instance.rect.x
    # Calculate the expected change in x position for a leftward move
    # The change is negative and scaled by the car's horizontal_speed_constant
    expected_change = -1 * player_car_instance.horizontal_speed_constant

    # Call the method to move the car left (direction = -1)
    player_car_instance.move_horizontal(-1)

    # Assert that the car's x position has changed by the expected amount
    assert player_car_instance.rect.x == initial_x + expected_change


def test_move_horizontal_right(player_car_instance):
    # Record the car's initial x position
    initial_x = player_car_instance.rect.x
    # Calculate the expected change in x position for a rightward move
    # The change is positive and scaled by the car's horizontal_speed_constant
    expected_change = 1 * player_car_instance.horizontal_speed_constant

    # Call the method to move the car right (direction = 1)
    player_car_instance.move_horizontal(1)

    # Assert that the car's x position has changed by the expected amount
    assert player_car_instance.rect.x == initial_x + expected_change


def test_move_horizontal_no_movement(player_car_instance):
    # Record the car's initial x position
    initial_x = player_car_instance.rect.x

    # Call the method with zero direction, indicating no movement
    player_car_instance.move_horizontal(0)

    # Assert that the car's x position has not changed
    assert player_car_instance.rect.x == initial_x