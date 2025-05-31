import pytest
import pygame
from unittest.mock import patch, MagicMock

# Assuming car.py and settings.py are in the same directory or accessible via PYTHONPATH
from car import Car
import settings

# Define constants for test inputs to avoid magic numbers
VALID_IMAGE_PATH = "assets/player_car_valid.png"  # A dummy path for a valid image
INVALID_IMAGE_PATH = "assets/non_existent_car.png"  # A dummy path for an invalid image
TEST_X_POS = 150
TEST_Y_POS = 300
TEST_HORIZONTAL_SPEED_CONSTANT = 0  # This parameter is not used by Car.__init__ itself


@pytest.fixture(scope="function", autouse=True)
def pygame_minimal_setup():
    # Minimal pygame setup required for Surface, Rect, mask, and pygame.error
    # This ensures pygame's internal state is ready for these operations
    pygame.init()
    yield
    pygame.quit()


def test_car_init_valid_image_load(mocker):
    # This test verifies correct initialization when a valid image path is provided

    # Mock pygame.image.load to return a mock Surface object
    mock_surface_instance = MagicMock(spec=pygame.Surface)
    # Mock the get_rect() method of the mock Surface to return a mock Rect
    mock_rect_instance = MagicMock(spec=pygame.Rect)
    # Arbitrary dimensions for the mock rect, actual dimensions depend on the image
    mock_rect_instance.width = 50
    mock_rect_instance.height = 100
    mock_surface_instance.get_rect.return_value = mock_rect_instance
    # Ensure convert_alpha() returns the same mock surface for method chaining
    mock_surface_instance.convert_alpha.return_value = mock_surface_instance

    mocker.patch('pygame.image.load', return_value=mock_surface_instance)

    # Mock pygame.mask.from_surface
    mock_mask_from_surface = mocker.patch('pygame.mask.from_surface')

    # Create a Car instance
    test_car = Car(VALID_IMAGE_PATH, TEST_X_POS, TEST_Y_POS, TEST_HORIZONTAL_SPEED_CONSTANT, is_npc=False)

    # Assert that pygame.image.load was called with the correct image path
    pygame.image.load.assert_called_once_with(VALID_IMAGE_PATH)
    # Assert that convert_alpha was called on the loaded image
    test_car.image.convert_alpha.assert_called_once()
    # Assert that self.image is the (mocked) loaded surface
    assert test_car.image == mock_surface_instance

    # Assert that get_rect was called on the surface to create self.rect
    mock_surface_instance.get_rect.assert_called_once()
    # Assert that self.rect is the (mocked) rect from the surface
    assert test_car.rect == mock_rect_instance
    # Assert that the rect's center was correctly set
    assert test_car.rect.centerx == TEST_X_POS
    assert test_car.rect.centery == TEST_Y_POS

    # Assert that pygame.mask.from_surface was called with the loaded image
    mock_mask_from_surface.assert_called_once_with(mock_surface_instance)
    # Assert that self.mask is the (mocked) mask object
    assert test_car.mask == mock_mask_from_surface.return_value


def test_car_init_invalid_image_is_npc_true(mocker):
    # This test verifies placeholder creation when image loading fails for an NPC car

    # Mock pygame.image.load to raise pygame.error, simulating a load failure
    mocker.patch('pygame.image.load', side_effect=pygame.error("Simulated image load failure"))

    # Mock the built-in print function to check if the warning is printed
    mock_print = mocker.patch('builtins.print')

    # Mock pygame.mask.from_surface
    mock_mask_from_surface = mocker.patch('pygame.mask.from_surface')

    # Create a Car instance with is_npc=True
    test_car = Car(INVALID_IMAGE_PATH, TEST_X_POS, TEST_Y_POS, TEST_HORIZONTAL_SPEED_CONSTANT, is_npc=True)

    # Assert that pygame.image.load was called
    pygame.image.load.assert_called_once_with(INVALID_IMAGE_PATH)

    # Assert that the correct warning message was printed
    expected_warning = f"Warning: Could not load image {INVALID_IMAGE_PATH}. Using placeholder."
    mock_print.assert_called_once_with(expected_warning)

    # Assert that self.image is a pygame.Surface instance (the placeholder)
    assert isinstance(test_car.image, pygame.Surface)
    # Assert placeholder dimensions
    assert test_car.image.get_width() == settings.PLACEHOLDER_NPC_WIDTH
    assert test_car.image.get_height() == settings.PLACEHOLDER_NPC_HEIGHT
    # Assert placeholder color is BLUE for NPC
    # We check the color of a pixel (e.g., at (0,0))
    # The placeholder surface is created with SRCALPHA, so get_at() returns (R,G,B,A)
    # We compare only the RGB components
    assert test_car.image.get_at((0, 0))[:3] == settings.BLUE

    # Assert self.rect properties are based on the placeholder
    assert test_car.rect.width == settings.PLACEHOLDER_NPC_WIDTH
    assert test_car.rect.height == settings.PLACEHOLDER_NPC_HEIGHT
    assert test_car.rect.centerx == TEST_X_POS
    assert test_car.rect.centery == TEST_Y_POS

    # Assert that pygame.mask.from_surface was called with the placeholder image
    mock_mask_from_surface.assert_called_once_with(test_car.image)
    assert test_car.mask == mock_mask_from_surface.return_value


def test_car_init_invalid_image_is_npc_false(mocker):
    # This test verifies placeholder creation when image loading fails for a non-NPC car

    # Mock pygame.image.load to raise pygame.error
    mocker.patch('pygame.image.load', side_effect=pygame.error("Simulated image load failure"))

    # Mock the built-in print function
    mock_print = mocker.patch('builtins.print')

    # Mock pygame.mask.from_surface
    mock_mask_from_surface = mocker.patch('pygame.mask.from_surface')

    # Create a Car instance with is_npc=False
    test_car = Car(INVALID_IMAGE_PATH, TEST_X_POS, TEST_Y_POS, TEST_HORIZONTAL_SPEED_CONSTANT, is_npc=False)

    # Assert that pygame.image.load was called
    pygame.image.load.assert_called_once_with(INVALID_IMAGE_PATH)

    # Assert that the correct warning message was printed
    expected_warning = f"Warning: Could not load image {INVALID_IMAGE_PATH}. Using placeholder."
    mock_print.assert_called_once_with(expected_warning)

    # Assert that self.image is a pygame.Surface instance (the placeholder)
    assert isinstance(test_car.image, pygame.Surface)
    # Assert placeholder dimensions (these are currently fixed to NPC placeholder sizes)
    assert test_car.image.get_width() == settings.PLACEHOLDER_NPC_WIDTH
    assert test_car.image.get_height() == settings.PLACEHOLDER_NPC_HEIGHT
    # Assert placeholder color is RED for non-NPC
    assert test_car.image.get_at((0, 0))[:3] == settings.RED

    # Assert self.rect properties are based on the placeholder
    assert test_car.rect.width == settings.PLACEHOLDER_NPC_WIDTH
    assert test_car.rect.height == settings.PLACEHOLDER_NPC_HEIGHT
    assert test_car.rect.centerx == TEST_X_POS
    assert test_car.rect.centery == TEST_Y_POS

    # Assert that pygame.mask.from_surface was called with the placeholder image
    mock_mask_from_surface.assert_called_once_with(test_car.image)
    assert test_car.mask == mock_mask_from_surface.return_value