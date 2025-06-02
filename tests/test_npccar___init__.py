import pytest
import pygame
from unittest.mock import patch, MagicMock

# Assuming car.py and settings.py are in locations accessible by PYTHONPATH
from car import NPCCar
import settings

# Minimal pygame setup for tests that need Surface or Mask capabilities
@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()

# Define test constants
VALID_NPC_IMAGE_PATH = settings.NPC_IMAGE_PATH # Use path from settings
INVALID_NPC_IMAGE_PATH = "assets/non_existent_npc_image.png"
TEST_X_POS = 250
TEST_Y_POS = 350
TEST_SPEED = 60

def test_npccar_init_valid_image():
    """Test NPCCar initialization with a valid image path, position, and speed"""
    # Mock pygame.image.load to return a controlled Surface object
    mock_surface = MagicMock(spec=pygame.Surface)
    # Define a plausible rect for the mock surface
    mock_rect = pygame.Rect(0, 0, settings.PLACEHOLDER_CAR_WIDTH, settings.PLACEHOLDER_CAR_HEIGHT)
    mock_surface.get_rect.return_value = mock_rect
    # convert_alpha usually returns the surface itself after an operation
    mock_surface.convert_alpha.return_value = mock_surface

    # Mock pygame.mask.from_surface to return a controlled Mask object
    mock_mask = MagicMock(spec=pygame.mask.Mask)

    with patch('pygame.image.load', return_value=mock_surface) as mock_image_load, \
         patch('pygame.mask.from_surface', return_value=mock_mask) as mock_mask_from_surface:

        # Initialize NPCCar
        npc_car = NPCCar(VALID_NPC_IMAGE_PATH, TEST_X_POS, TEST_Y_POS, TEST_SPEED)

        # Assert pygame.image.load was called correctly
        mock_image_load.assert_called_once_with(VALID_NPC_IMAGE_PATH)
        mock_surface.convert_alpha.assert_called_once() # Ensure image processing step

        # Assert attributes set by Car.__init__ are correct
        assert npc_car.image == mock_surface
        assert npc_car.rect.centerx == TEST_X_POS
        assert npc_car.rect.centery == TEST_Y_POS
        assert npc_car.speed == TEST_SPEED

        # Assert pygame.mask.from_surface was called with the loaded image
        mock_mask_from_surface.assert_called_once_with(mock_surface)
        assert npc_car.mask == mock_mask

def test_npccar_init_invalid_image_uses_blue_placeholder():
    """Test NPCCar initialization with an invalid image path uses a blue placeholder"""
    # Mock pygame.image.load to simulate a FileNotFoundError or pygame.error
    with patch('pygame.image.load', side_effect=pygame.error("Failed to load image")) as mock_image_load:
        # NPCCar initialization should trigger the fallback placeholder logic in Car.__init__
        npc_car = NPCCar(INVALID_NPC_IMAGE_PATH, TEST_X_POS, TEST_Y_POS, TEST_SPEED)

        # Assert pygame.image.load was called with the invalid path
        mock_image_load.assert_called_once_with(INVALID_NPC_IMAGE_PATH)

        # Verify that a placeholder Surface was created
        assert isinstance(npc_car.image, pygame.Surface)
        assert npc_car.image.get_width() == settings.PLACEHOLDER_CAR_WIDTH
        assert npc_car.image.get_height() == settings.PLACEHOLDER_CAR_HEIGHT

        # Verify the placeholder color is blue (as is_npc=True for NPCCar)
        # The Car class fills the SRCALPHA surface, resulting in (R,G,B,255)
        placeholder_color_at_pixel = npc_car.image.get_at((0, 0))
        expected_blue_color = pygame.Color(settings.BLUE) # pygame.Color(0,0,255,255)
        assert placeholder_color_at_pixel == expected_blue_color

        # Verify other attributes are set correctly
        assert npc_car.rect.centerx == TEST_X_POS
        assert npc_car.rect.centery == TEST_Y_POS
        assert npc_car.speed == TEST_SPEED

        # Verify a mask was created from the blue placeholder surface
        assert isinstance(npc_car.mask, pygame.mask.Mask)
        # Check if mask dimensions match the placeholder surface dimensions
        assert npc_car.mask.get_size() == (settings.PLACEHOLDER_CAR_WIDTH, settings.PLACEHOLDER_CAR_HEIGHT)