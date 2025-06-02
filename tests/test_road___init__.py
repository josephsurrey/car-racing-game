# test_road_init.py
import pygame
import pytest
from unittest.mock import patch, MagicMock

from road import Road  # assuming road.py is in the python path
import settings  # assuming settings.py is in the python path

# constants for testing
DUMMY_IMAGE_PATH = "assets/test_road.png"  # example path
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Test: Initialize Road with a valid image path
@patch('road.pygame.transform.scale')  # patch scale first due to order in decorator stack
@patch('road.pygame.image.load')
def test_road_init_valid_image(mock_image_load, mock_transform_scale):
    # arrange
    # mock the original image loaded by pygame.image.load
    original_img_mock = MagicMock(spec=pygame.Surface)
    original_img_mock.convert.return_value = original_img_mock
    original_width, original_height = 600, 1200  # w, h for an example image
    original_img_mock.get_size.return_value = (original_width, original_height)
    mock_image_load.return_value = original_img_mock

    # mock the scaled image returned by pygame.transform.scale
    scaled_img_mock = MagicMock(spec=pygame.Surface)
    # calculate expected scaled height based on the game's logic
    aspect_ratio = original_width / original_height
    expected_scaled_height = SCREEN_WIDTH * aspect_ratio

    scaled_img_mock.get_height.return_value = expected_scaled_height

    # mock rects for the scaled image
    mock_rect1 = MagicMock(spec=pygame.Rect)
    mock_rect1.topleft = (0, 0)  # set topleft for assertion clarity
    mock_rect2 = MagicMock(spec=pygame.Rect)
    mock_rect2.topleft = (0, -expected_scaled_height)  # set topleft for assertion clarity

    # configure scaled_img_mock.get_rect to return specific rects
    def get_rect_side_effect(**kwargs):
        if kwargs.get('topleft') == (0, 0):
            return mock_rect1
        if kwargs.get('topleft') == (0, -expected_scaled_height):
            return mock_rect2
        # fallback, though not expected to be hit in this test for rect1/rect2
        fallback_rect = MagicMock(spec=pygame.Rect)
        fallback_rect.topleft = kwargs.get('topleft', (0, 0))  # default topleft
        return fallback_rect

    scaled_img_mock.get_rect.side_effect = get_rect_side_effect
    mock_transform_scale.return_value = scaled_img_mock

    # act
    road = Road(DUMMY_IMAGE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT)

    # assert
    # check screen dimensions are set
    assert road.screen_width == SCREEN_WIDTH
    assert road.screen_height == SCREEN_HEIGHT

    # check pygame.image.load call
    mock_image_load.assert_called_once_with(DUMMY_IMAGE_PATH)
    original_img_mock.convert.assert_called_once()  # ensure convert was called
    original_img_mock.get_size.assert_called_once()  # ensure get_size was called

    # check pygame.transform.scale call
    # the target size for scaling is (SCREEN_WIDTH, SCREEN_WIDTH * aspect_ratio)
    mock_transform_scale.assert_called_once_with(
        original_img_mock,  # the surface returned by load().convert()
        (SCREEN_WIDTH, SCREEN_WIDTH * aspect_ratio)
    )

    # check attributes of the road instance
    assert road.image == scaled_img_mock  # image is the scaled image
    assert road.image_height == expected_scaled_height  # image_height from scaled image

    assert road.rect1 == mock_rect1  # check it's the correct mock object
    assert road.rect1.topleft == (0, 0)  # verify topleft attribute
    assert road.rect2 == mock_rect2  # check it's the correct mock object
    assert road.rect2.topleft == (0, -expected_scaled_height)  # verify topleft attribute

    # ensure placeholder was not created
    assert not hasattr(road, 'image_original')


# Test: Initialize Road with an invalid image path (FileNotFoundError)
@patch('road.pygame.Surface')  # This mock is injected as mock_pygame_surface_constructor
@patch('road.pygame.image.load')
def test_road_init_invalid_path_file_not_found(mock_image_load, mock_pygame_surface_constructor, capsys):
    # arrange
    # configure pygame.image.load to raise FileNotFoundError
    invalid_path = "invalid/path/to/image.png"
    mock_image_load.side_effect = FileNotFoundError("File not found for test")

    # This is the mock instance that pygame.Surface() will return inside Road.__init__
    mock_created_surface_instance = MagicMock(name="placeholder_surface_instance")
    mock_pygame_surface_constructor.return_value = mock_created_surface_instance

    # act
    road = Road(invalid_path, SCREEN_WIDTH, SCREEN_HEIGHT)

    # assert
    # check pygame.image.load was called
    mock_image_load.assert_called_once_with(invalid_path)

    # check warning was printed
    captured = capsys.readouterr()
    expected_warning = (
        f"Warning: Could not load road image '{invalid_path}'."
        f" Creating placeholder."
    )
    assert expected_warning in captured.out

    # check placeholder surface constructor was called
    mock_pygame_surface_constructor.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT))
    # check fill was called on the mock instance that was returned by the constructor
    mock_created_surface_instance.fill.assert_called_once_with(settings.BLACK)
    assert road.image_original == mock_created_surface_instance

    # ensure main image attributes are not set if load fails
    assert not hasattr(road, 'image')
    assert not hasattr(road, 'image_height')
    assert not hasattr(road, 'rect1')
    assert not hasattr(road, 'rect2')


# Test: Initialize Road when pygame.image.load raises pygame.error
@patch('road.pygame.Surface')  # This mock is injected as mock_pygame_surface_constructor
@patch('road.pygame.image.load')
def test_road_init_pygame_error_on_load(mock_image_load, mock_pygame_surface_constructor, capsys):
    # arrange
    # configure pygame.image.load to raise pygame.error
    mock_image_load.side_effect = pygame.error("Pygame test error")

    # This is the mock instance that pygame.Surface() will return inside Road.__init__
    mock_created_surface_instance = MagicMock(name="placeholder_surface_instance_pyerror")
    mock_pygame_surface_constructor.return_value = mock_created_surface_instance

    # act
    road = Road(DUMMY_IMAGE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT)

    # assert
    # check pygame.image.load was called
    mock_image_load.assert_called_once_with(DUMMY_IMAGE_PATH)

    # check warning was printed
    captured = capsys.readouterr()
    expected_warning = (
        f"Warning: Could not load road image '{DUMMY_IMAGE_PATH}'."
        f" Creating placeholder."
    )
    assert expected_warning in captured.out

    # check placeholder surface constructor was called
    mock_pygame_surface_constructor.assert_called_once_with((SCREEN_WIDTH, SCREEN_HEIGHT))
    # check fill was called on the mock instance that was returned by the constructor
    mock_created_surface_instance.fill.assert_called_once_with(settings.BLACK)
    assert road.image_original == mock_created_surface_instance

    # ensure main image attributes are not set if load fails
    assert not hasattr(road, 'image')
    assert not hasattr(road, 'image_height')
    assert not hasattr(road, 'rect1')
    assert not hasattr(road, 'rect2')


# Test: Edge Case - Initialize Road with an image having an extreme aspect ratio (very wide)
@patch('road.pygame.transform.scale')
@patch('road.pygame.image.load')
def test_road_init_extreme_aspect_ratio_wide_image(mock_image_load, mock_transform_scale):
    # arrange
    # mock original image (very wide)
    original_img_mock = MagicMock(spec=pygame.Surface)
    original_img_mock.convert.return_value = original_img_mock
    original_width, original_height = 2000, 100  # w, h for a very wide image
    original_img_mock.get_size.return_value = (original_width, original_height)
    mock_image_load.return_value = original_img_mock

    # mock scaled image
    scaled_img_mock = MagicMock(spec=pygame.Surface)
    # calculate expected scaled height
    aspect_ratio = original_width / original_height  # 2000 / 100 = 20
    expected_scaled_height = SCREEN_WIDTH * aspect_ratio  # 800 * 20 = 16000 (very tall)

    scaled_img_mock.get_height.return_value = expected_scaled_height

    # mock rects
    mock_rect1 = MagicMock(spec=pygame.Rect)
    mock_rect1.topleft = (0, 0)  # set topleft for assertion clarity
    mock_rect2 = MagicMock(spec=pygame.Rect)
    mock_rect2.topleft = (0, -expected_scaled_height)  # set topleft for assertion clarity

    def get_rect_side_effect(**kwargs):
        if kwargs.get('topleft') == (0, 0):
            return mock_rect1
        if kwargs.get('topleft') == (0, -expected_scaled_height):
            return mock_rect2
        fallback_rect = MagicMock(spec=pygame.Rect)
        fallback_rect.topleft = kwargs.get('topleft', (0, 0))
        return fallback_rect

    scaled_img_mock.get_rect.side_effect = get_rect_side_effect
    mock_transform_scale.return_value = scaled_img_mock

    # act
    road = Road(DUMMY_IMAGE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT)

    # assert
    mock_image_load.assert_called_once_with(DUMMY_IMAGE_PATH)
    original_img_mock.convert.assert_called_once()
    original_img_mock.get_size.assert_called_once()

    mock_transform_scale.assert_called_once_with(
        original_img_mock,
        (SCREEN_WIDTH, SCREEN_WIDTH * aspect_ratio)  # target size for scale
    )

    assert road.image == scaled_img_mock
    assert road.image_height == expected_scaled_height
    assert road.rect1.topleft == (0, 0)  # verify topleft attribute
    assert road.rect2.topleft == (0, -expected_scaled_height)  # verify topleft attribute
    assert not hasattr(road, 'image_original')  # no placeholder