import pytest
from unittest.mock import MagicMock, patch
import pygame  # Imported for type hinting and using pygame object specs in mocks

# Assuming 'road.py' and 'settings.py' are in a location where they can be imported
# For example, in the same directory or in PYTHONPATH
from road import Road


# settings.py is implicitly imported by road.py

@pytest.fixture
def mock_pygame_for_road_init():
    # This fixture mocks pygame functionalities used during Road.__init__

    # Mock for the original surface loaded by pygame.image.load
    mock_surface_original = MagicMock(spec=pygame.Surface)
    # Mock the convert() method, often returns self or a similar surface
    mock_surface_original.convert.return_value = mock_surface_original
    # Mock get_size() to return dimensions for aspect ratio calculation
    mock_surface_original.get_size.return_value = (100, 200)  # Example: original_width, original_height

    # Mock for the scaled surface returned by pygame.transform.scale
    mock_surface_scaled = MagicMock(spec=pygame.Surface)
    # Mock get_height() for the scaled image
    mock_surface_scaled.get_height.return_value = 400  # Example: image_height after scaling

    # Mock get_rect() called on the scaled surface
    # It's called twice, so it should return two distinct mock rects if needed for specific checks,
    # or just a generic MagicMock for each call. For these tests, generic mocks are fine.
    mock_rect_instance1 = MagicMock(spec=pygame.Rect)
    mock_rect_instance2 = MagicMock(spec=pygame.Rect)
    mock_surface_scaled.get_rect.side_effect = [mock_rect_instance1, mock_rect_instance2]

    # Patch pygame.image.load, pygame.transform.scale
    # These are the main pygame calls in Road.__init__ that need mocking for this unit test
    with patch('pygame.image.load', return_value=mock_surface_original) as mock_load, \
            patch('pygame.transform.scale', return_value=mock_surface_scaled) as mock_scale:
        yield {
            "load": mock_load,
            "scale": mock_scale,
            "surface_original": mock_surface_original,
            "surface_scaled": mock_surface_scaled,
            "rect1_created": mock_rect_instance1,
            "rect2_created": mock_rect_instance2,
        }


@pytest.fixture
def road_instance(mock_pygame_for_road_init):
    # Create an instance of the Road class
    # The road_image path string doesn't matter as pygame.image.load is mocked
    # Screen width and height are required by Road.__init__
    road = Road("assets/mock_road.png", 800, 600)

    # Verify that __init__ set up the instance correctly with mocked objects
    assert road.image is mock_pygame_for_road_init["surface_scaled"]
    assert road.rect1 is mock_pygame_for_road_init["rect1_created"]
    assert road.rect2 is mock_pygame_for_road_init["rect2_created"]
    return road


def test_draw_blits_twice(road_instance):
    # Create a mock screen object to pass to the draw method
    mock_screen = MagicMock(spec=pygame.Surface)

    # Call the draw method on the road instance
    road_instance.draw(mock_screen)

    # Assert that screen blit method was called exactly twice
    assert mock_screen.blit.call_count == 2


def test_draw_blits_correct_arguments(road_instance):
    # Create a mock screen object
    mock_screen = MagicMock(spec=pygame.Surface)

    # Call the draw method
    road_instance.draw(mock_screen)

    # Get the list of all calls made to the blit method
    blit_calls = mock_screen.blit.call_args_list

    # Check arguments of the first blit call
    # It should be called with road_instance.image and road_instance.rect1
    first_call_args, _ = blit_calls[0]  # Unpack args, ignore kwargs
    assert first_call_args[0] is road_instance.image  # Check image argument
    assert first_call_args[1] is road_instance.rect1  # Check rect argument

    # Check arguments of the second blit call
    # It should be called with road_instance.image and road_instance.rect2
    second_call_args, _ = blit_calls[1]  # Unpack args, ignore kwargs
    assert second_call_args[0] is road_instance.image  # Check image argument
    assert second_call_args[1] is road_instance.rect2  # Check rect argument