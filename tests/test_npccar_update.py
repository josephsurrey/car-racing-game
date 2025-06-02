import pygame
import pytest
from unittest.mock import Mock

# Ensure settings are available for NPCCar and tests
import settings
from car import NPCCar

# Constants from settings for convenience
SCREEN_HEIGHT = settings.SCREEN_HEIGHT
NPC_IMAGE_HEIGHT = settings.PLACEHOLDER_NPC_HEIGHT # Assuming image load fail for predictable size

@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    # Initialize Pygame and set a minimal display mode
    # This is necessary for operations like image loading and rect creation
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def npc_car():
    # Fixture to create a new NPCCar instance for each test
    # Using an invalid image path to ensure placeholder image is used for consistent height
    # Initial y_pos calculated to place npc_car.rect.top at a specific value if needed
    # Default y_pos places the car's center; rect.top will be y_pos - NPC_IMAGE_HEIGHT / 2
    # For these tests, precise initial y_pos will be set in each test or a helper
    car = NPCCar(npc_image_path="invalid_image.png", x_pos=100, y_pos=100, speed=10)
    # Mock the kill method to check if it's called
    car.kill = Mock()
    # Ensure car is part of a group to check car.alive() status,
    # as self.kill() typically removes it from groups
    # For simplicity in unit test, we'll rely on the mock and can also check a pseudo 'alive' status
    # or directly verify mock calls if 'alive' is complex to set up without real groups
    car._alive = True # Simple flag for testing, real alive() depends on groups
    original_kill = car.kill
    def kill_wrapper():
        original_kill()
        car._alive = False
    car.kill = kill_wrapper
    car.kill.called = False # For mock-like check if not using full MagicMock

    # Helper to re-assign the mock if needed, as car.kill is a method of Sprite
    # We are mocking the instance's method
    # If car.kill was a direct attribute, this would be simpler
    # Pygame's sprite.kill() removes from groups, affecting sprite.alive()
    # So, we mock it on the instance
    mock_kill = Mock(wraps=car.kill) # wraps the modified kill_wrapper
    car.kill = mock_kill

    return car

def set_npc_top_position(npc, top_y):
    # Helper to set the npc's rect.top to a specific y_coordinate
    npc.rect.centery = top_y + NPC_IMAGE_HEIGHT / 2
    # Ensure rect.y (which is rect.top) is updated after centery change
    npc.rect.y = npc.rect.top


# Test case 1: NPC moves down (road faster than NPC)
def test_npc_moves_down_on_screen(npc_car):
    initial_y = 100 # initial rect.top
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 10
    road_speed = 20 # Road is faster

    npc_car.update(road_speed, SCREEN_HEIGHT)

    # NPC should move down
    expected_y_change = road_speed - npc_car.speed
    assert npc_car.rect.top == initial_y + expected_y_change
    # Kill should not be called
    npc_car.kill.assert_not_called()
    assert npc_car._alive # Using our simple flag


# Test case 2: NPC moves up (NPC faster than road)
def test_npc_moves_up_on_screen(npc_car):
    initial_y = 200 # initial rect.top
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 30
    road_speed = 10 # NPC is faster

    npc_car.update(road_speed, SCREEN_HEIGHT)

    # NPC should move up
    expected_y_change = road_speed - npc_car.speed # This will be negative
    assert npc_car.rect.top == initial_y + expected_y_change
    # Kill should not be called
    npc_car.kill.assert_not_called()
    assert npc_car._alive


# Test case 3: NPC stationary (NPC speed equals road speed)
def test_npc_stationary_vertically(npc_car):
    initial_y = 150 # initial rect.top
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 25
    road_speed = 25 # Speeds are equal

    npc_car.update(road_speed, SCREEN_HEIGHT)

    # NPC should not move vertically
    assert npc_car.rect.top == initial_y
    # Kill should not be called
    npc_car.kill.assert_not_called()
    assert npc_car._alive


# Test case 4: NPC moves off bottom of screen and is killed
def test_npc_moves_off_bottom_and_killed(npc_car):
    # Position NPC so it will move off screen
    # SCREEN_HEIGHT = 650, NPC_IMAGE_HEIGHT = 100
    # If rect.top starts at 640 and moves by +20, new top is 660
    # 660 > 650, so kill
    initial_y = SCREEN_HEIGHT - 10 # rect.top is 640
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 10
    road_speed = 30 # Positive net movement (downwards) of 20

    npc_car.update(road_speed, SCREEN_HEIGHT)

    expected_y_change = road_speed - npc_car.speed
    assert npc_car.rect.top == initial_y + expected_y_change # New top is 660
    # Kill should be called
    npc_car.kill.assert_called_once()
    # The _alive flag should be False due to our wrapper
    # This test might need adjustment if car._alive isn't properly set by the mock
    # For now, primary check is on kill mock
    # assert not npc_car._alive # This depends on the mock setup for _alive


# Test case 5: NPC top reaches exactly screen bottom, not killed
def test_npc_top_reaches_screen_bottom_not_killed(npc_car):
    # Position NPC so its top will be exactly at screen_height
    # If rect.top starts at 630 and moves by +20, new top is 650
    # 650 > 650 is false, so not killed
    initial_y = SCREEN_HEIGHT - 20 # rect.top is 630
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 10
    road_speed = 30 # Positive net movement (downwards) of 20

    npc_car.update(road_speed, SCREEN_HEIGHT)

    expected_y_change = road_speed - npc_car.speed
    assert npc_car.rect.top == initial_y + expected_y_change # New top is 650
    # Kill should not be called
    npc_car.kill.assert_not_called()
    assert npc_car._alive


# Test case 6: NPC starts off-screen and is killed after moving
def test_npc_starts_off_screen_and_killed(npc_car):
    # Position NPC so its top is already off screen
    initial_y = SCREEN_HEIGHT + 10 # rect.top is 660 (already > 650)
    set_npc_top_position(npc_car, initial_y)
    npc_car.speed = 5
    road_speed = 15 # Positive net movement (downwards) of 10

    npc_car.update(road_speed, SCREEN_HEIGHT)

    expected_y_change = road_speed - npc_car.speed
    assert npc_car.rect.top == initial_y + expected_y_change # New top is 670
    # Kill should be called as 670 > 650
    npc_car.kill.assert_called_once()
    # assert not npc_car._alive