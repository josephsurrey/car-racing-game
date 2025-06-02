import pytest
from unittest.mock import patch, MagicMock
import pygame  # Required for pygame.error and pygame.SRCALPHA constants

# --- FIX: Store original pygame types before they might be altered by patching ---
_OriginalPygameSurface = pygame.Surface
# If you were also patching car.pygame.Rect or car.pygame.mask.Mask, you'd store their originals too:
# _OriginalPygameRect = pygame.Rect
# _OriginalPygameMask = pygame.mask.Mask
# --- END FIX ---

# Assuming car.py and settings.py are accessible in the PYTHONPATH
from car import PlayerCar
import settings  # Ensure this module is available and contains necessary constants

# Define common test data using values from settings where appropriate
VALID_PLAYER_IMG_PATH = settings.PLAYER_IMAGE_PATH
INVALID_PLAYER_IMG_PATH = "assets/non_existent_player_image.png"
TEST_X_POS = settings.PLAYER_START_X_POS
TEST_Y_POS = settings.PLAYER_Y_POS
TEST_H_SPEED_CONSTANT = settings.HORIZONTAL_SPEED_CONSTANT


@patch('car.pygame.mask.from_surface')
@patch('car.pygame.image.load')  # Original order to match your arguments
@patch('car.pygame.Surface', spec=_OriginalPygameSurface)  # FIX: Use _OriginalPygameSurface for spec
def test_player_car_init_valid_image(mock_car_pygame_surface_cls, mock_image_load,
                                     mock_mask_from_surface):  # Adjusted arg order
    # Arrange
    mock_loaded_img_surface = MagicMock(spec=_OriginalPygameSurface)  # FIX: Use original for spec
    mock_rect_obj = MagicMock(spec=pygame.Rect)  # Assuming pygame.Rect is not patched similarly
    mock_rect_obj.centerx = 0
    mock_rect_obj.centery = 0
    mock_loaded_img_surface.get_rect.return_value = mock_rect_obj

    mock_image_load.return_value.convert_alpha.return_value = mock_loaded_img_surface

    mock_mask_created = MagicMock(spec=pygame.mask.Mask)  # Assuming pygame.mask.Mask is not patched
    mock_mask_from_surface.return_value = mock_mask_created

    # Act
    player_car = PlayerCar(VALID_PLAYER_IMG_PATH, TEST_X_POS, TEST_Y_POS, TEST_H_SPEED_CONSTANT)

    # Assert
    mock_image_load.assert_called_once_with(VALID_PLAYER_IMG_PATH)
    mock_image_load.return_value.convert_alpha.assert_called_once()
    assert player_car.image == mock_loaded_img_surface

    mock_loaded_img_surface.get_rect.assert_called_once()
    assert player_car.rect == mock_rect_obj
    assert player_car.rect.centerx == TEST_X_POS
    assert player_car.rect.centery == TEST_Y_POS

    mock_mask_from_surface.assert_called_once_with(mock_loaded_img_surface)
    assert player_car.mask == mock_mask_created

    assert player_car.initial_x_pos == TEST_X_POS
    assert player_car.initial_y_pos == TEST_Y_POS
    assert player_car.horizontal_speed_constant == TEST_H_SPEED_CONSTANT


@patch('car.pygame.mask.from_surface')
@patch('car.pygame.image.load')  # Original order from your code
@patch('car.pygame.Surface', spec=_OriginalPygameSurface)  # FIX: Use _OriginalPygameSurface for spec
def test_player_car_init_invalid_image(mock_car_pygame_surface_cls, mock_image_load,
                                       mock_mask_from_surface):  # Adjusted arg order
    # mock_car_pygame_surface_cls is the mock for car.pygame.Surface (the class)
    # mock_image_load is for car.pygame.image.load
    # mock_mask_from_surface is for car.pygame.mask.from_surface

    # Arrange
    mock_image_load.side_effect = pygame.error("Simulated image load failure")

    # This mock_placeholder_surface_instance should behave like an *original* pygame.Surface instance
    mock_placeholder_surface_instance = MagicMock(spec=_OriginalPygameSurface)  # FIX: Use the stored original

    # Mock for Rect. Assuming pygame.Rect itself is not being patched in 'car.pygame.Rect'.
    # If it were, you'd use _OriginalPygameRect here too.
    mock_rect_obj = MagicMock(spec=pygame.Rect)
    mock_rect_obj.centerx = 0
    mock_rect_obj.centery = 0
    mock_placeholder_surface_instance.get_rect.return_value = mock_rect_obj

    # Tell the mocked car.pygame.Surface class to return our placeholder instance when called
    mock_car_pygame_surface_cls.return_value = mock_placeholder_surface_instance

    # Mock for Mask. Assuming pygame.mask.Mask itself is not being patched.
    mock_mask_created = MagicMock(spec=pygame.mask.Mask)
    mock_mask_from_surface.return_value = mock_mask_created

    # Act
    player_car = PlayerCar(INVALID_PLAYER_IMG_PATH, TEST_X_POS, TEST_Y_POS, TEST_H_SPEED_CONSTANT)

    # Assert
    mock_image_load.assert_called_once_with(INVALID_PLAYER_IMG_PATH)

    # car.pygame.Surface(...) (which is now mock_car_pygame_surface_cls(...)) should have been called
    mock_car_pygame_surface_cls.assert_called_once_with(
        (settings.PLACEHOLDER_CAR_WIDTH, settings.PLACEHOLDER_CAR_HEIGHT),
        pygame.SRCALPHA  # pygame.SRCALPHA is a constant, should be fine
    )
    mock_placeholder_surface_instance.fill.assert_called_once_with(settings.RED)

    assert player_car.image == mock_placeholder_surface_instance

    mock_placeholder_surface_instance.get_rect.assert_called_once()
    assert player_car.rect == mock_rect_obj
    assert player_car.rect.centerx == TEST_X_POS
    assert player_car.rect.centery == TEST_Y_POS

    mock_mask_from_surface.assert_called_once_with(mock_placeholder_surface_instance)
    assert player_car.mask == mock_mask_created

    # Check PlayerCar specific attributes
    assert player_car.initial_x_pos == TEST_X_POS
    assert player_car.initial_y_pos == TEST_Y_POS
    assert player_car.horizontal_speed_constant == TEST_H_SPEED_CONSTANT