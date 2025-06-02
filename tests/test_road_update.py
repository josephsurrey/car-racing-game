import pytest
from unittest.mock import patch, MagicMock
import pygame  # Required for pygame.Rect

# Assuming road.py is in the same directory or accessible via PYTHONPATH
from road import Road

# settings.py might be implicitly needed if road.py imports it,
# but our mocks should prevent direct reliance for these specific tests

# Constants for mocking
MOCK_SCREEN_WIDTH = 840
MOCK_SCREEN_HEIGHT = 650
MOCK_IMAGE_ASPECT_RATIO = 2  # Example: original_height = original_width / 2
MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING = MOCK_SCREEN_WIDTH * MOCK_IMAGE_ASPECT_RATIO  # This is road.image_height


@pytest.fixture
def mock_pygame_dependencies():
    # Mock for pygame.image.load().convert()
    mock_original_surface = MagicMock(spec=pygame.Surface)
    original_width = MOCK_SCREEN_WIDTH  # Assume original width matches screen for simplicity
    original_height = original_width / MOCK_IMAGE_ASPECT_RATIO
    mock_original_surface.get_size.return_value = (original_width, original_height)
    mock_original_surface.convert.return_value = mock_original_surface

    # Mock for pygame.transform.scale()
    mock_scaled_surface = MagicMock(spec=pygame.Surface)
    mock_scaled_surface.get_height.return_value = MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING

    # Define a side_effect function for get_rect to return actual pygame.Rect
    def get_rect_side_effect(**kwargs):
        topleft = kwargs.get('topleft', (0, 0))
        # Use a fixed width for the rect, height is the MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING
        return pygame.Rect(topleft[0], topleft[1], MOCK_SCREEN_WIDTH, MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING)

    mock_scaled_surface.get_rect.side_effect = get_rect_side_effect

    with patch('road.pygame.image.load', return_value=mock_original_surface) as mock_load, \
            patch('road.pygame.transform.scale', return_value=mock_scaled_surface) as mock_scale:
        yield mock_load, mock_scale, mock_original_surface, mock_scaled_surface


@pytest.fixture
def road_instance(mock_pygame_dependencies):
    # The road_image path is a dummy because pygame.image.load is mocked
    road = Road("assets/background.png", MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
    # Ensure image_height is set as expected by the mock
    assert road.image_height == MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING
    # Check initial positions based on Road.__init__
    assert road.rect1.topleft == (0, 0)
    assert road.rect2.topleft == (0, -MOCK_ROAD_IMAGE_HEIGHT_AFTER_SCALING)
    return road


def test_road_update_positive_speed_no_scroll(road_instance):
    # Test road segments move down correctly with positive speed
    initial_rect1_y = road_instance.rect1.y
    initial_rect2_y = road_instance.rect2.y
    speed = 10

    road_instance.update(speed)

    assert road_instance.rect1.y == initial_rect1_y + speed
    assert road_instance.rect2.y == initial_rect2_y + speed
    # Ensure no scrolling happened if not expected
    assert road_instance.rect1.y < road_instance.image_height
    assert road_instance.rect2.y < road_instance.image_height


def test_road_update_rect1_scrolls(road_instance):
    # Test rect1 scrolls correctly when it moves beyond the image height
    speed = 10
    # Position rect1 just before scrolling threshold
    road_instance.rect1.y = road_instance.image_height - (speed // 2)
    # Position rect2 relative to rect1
    road_instance.rect2.y = road_instance.rect1.y - road_instance.image_height

    initial_rect2_y = road_instance.rect2.y  # Store before rect1's scroll potentially affects it indirectly

    road_instance.update(speed)

    # rect1.y should have moved down by speed, then scrolled
    # rect2.y should have moved down by speed
    expected_rect2_y_after_move = initial_rect2_y + speed
    assert road_instance.rect2.y == expected_rect2_y_after_move
    assert road_instance.rect1.y == expected_rect2_y_after_move - road_instance.image_height


def test_road_update_rect2_scrolls(road_instance):
    # Test rect2 scrolls correctly when it moves beyond the image height
    speed = 10
    # Position rect2 just before scrolling threshold
    road_instance.rect2.y = road_instance.image_height - (speed // 2)
    # Position rect1 relative to rect2
    road_instance.rect1.y = road_instance.rect2.y - road_instance.image_height

    initial_rect1_y = road_instance.rect1.y  # Store before rect2's scroll affects it

    road_instance.update(speed)

    # rect2.y should have moved down by speed, then scrolled
    # rect1.y should have moved down by speed
    expected_rect1_y_after_move = initial_rect1_y + speed
    assert road_instance.rect1.y == expected_rect1_y_after_move
    assert road_instance.rect2.y == expected_rect1_y_after_move - road_instance.image_height


def test_road_update_zero_speed(road_instance):
    # Test road segments remain stationary with zero speed
    initial_rect1_y = road_instance.rect1.y
    initial_rect2_y = road_instance.rect2.y
    speed = 0

    road_instance.update(speed)

    assert road_instance.rect1.y == initial_rect1_y
    assert road_instance.rect2.y == initial_rect2_y


def test_road_update_negative_speed_no_scroll(road_instance):
    # Test road segments move up correctly with negative speed
    # Start rects at a position where negative speed won't cause scrolling
    road_instance.rect1.y = 50
    road_instance.rect2.y = 50 - road_instance.image_height

    initial_rect1_y = road_instance.rect1.y
    initial_rect2_y = road_instance.rect2.y
    speed = -10

    road_instance.update(speed)

    assert road_instance.rect1.y == initial_rect1_y + speed  # speed is negative
    assert road_instance.rect2.y == initial_rect2_y + speed  # speed is negative
    # Ensure no scrolling happened (y values decrease, so top won't exceed image_height)
    assert road_instance.rect1.top < road_instance.image_height
    assert road_instance.rect2.top < road_instance.image_height