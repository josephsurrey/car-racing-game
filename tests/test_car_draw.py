import pygame
import pytest
from unittest.mock import Mock, patch

# Ensure car and settings modules can be imported by test runner
from car import Car
import settings

# Minimal Pygame initialization for tests that need it
# This is for operations like Surface creation
pygame.init()

# TestCarDraw class contains tests for the Car.draw() method
class TestCarDraw:

    # setup_method runs before each test in this class
    def setup_method(self):
        # Mock for pygame.image.load
        self.mock_loaded_image = Mock(spec=pygame.Surface)
        # Define a generic rect for the mock image
        self.mock_image_rect = pygame.Rect(0, 0, 50, 100)
        self.mock_loaded_image.get_rect = Mock(return_value=self.mock_image_rect.copy())
        # convert_alpha often returns self or a new surface, mock it to return the same mock image
        self.mock_loaded_image.convert_alpha = Mock(return_value=self.mock_loaded_image)

        # Mock for pygame.mask.from_surface
        self.mock_mask_object = Mock(spec=pygame.mask.Mask)

    @patch('car.pygame.mask.from_surface')
    @patch('car.pygame.image.load')
    @patch('car.screen', create=True) # MODIFIED: Added create=True
    def test_draw_blits_loaded_image_to_screen(self, mock_screen_in_car_module, mock_pygame_image_load, mock_pygame_mask_from_surface):
        # Test Car.draw correctly blits a successfully loaded image

        # Arrange
        # Configure mocks for Car constructor dependencies
        mock_pygame_image_load.return_value = self.mock_loaded_image
        mock_pygame_mask_from_surface.return_value = self.mock_mask_object

        # Create a Car instance with specific positions
        car_x_pos = 150
        car_y_pos = 250
        test_car = Car(
            car_image="assets/any_image.png", # Path does not matter due to mock
            x_pos=car_x_pos,
            y_pos=car_y_pos,
            horizontal_speed_constant=0, # Not used by base Car constructor
            is_npc=False
        )

        # Check attributes set by constructor are as expected
        assert test_car.image == self.mock_loaded_image
        assert test_car.rect.centerx == car_x_pos
        assert test_car.rect.centery == car_y_pos

        # Act
        # Call the draw method to be tested
        test_car.draw()

        # Assert
        # Verify screen.blit was called with the car's image and rect
        mock_screen_in_car_module.blit.assert_called_once_with(test_car.image, test_car.rect)

    @patch('car.pygame.mask.from_surface')
    @patch('car.pygame.image.load') # Mock image loading to simulate failure
    @patch('car.screen', create=True) # MODIFIED: Added create=True
    def test_draw_blits_placeholder_image_to_screen(self, mock_screen_in_car_module, mock_pygame_image_load, mock_pygame_mask_from_surface):
        # Test Car.draw correctly blits a placeholder image if image loading fails

        # Arrange
        # Configure mock_pygame_image_load to raise an error, triggering placeholder creation
        mock_pygame_image_load.side_effect = pygame.error("Simulated image load failure")
        # Mask creation is still attempted for the placeholder surface
        mock_pygame_mask_from_surface.return_value = self.mock_mask_object

        # Create a Car instance, expecting it to use a placeholder
        car_x_pos = 100
        car_y_pos = 200
        test_car_with_placeholder = Car(
            car_image="assets/non_existent.png", # Path does not matter
            x_pos=car_x_pos,
            y_pos=car_y_pos,
            horizontal_speed_constant=0, # Not used by base Car constructor
            is_npc=True # Using is_npc=True to test the blue placeholder branch
        )

        # Check that a placeholder image (pygame.Surface) was created
        assert isinstance(test_car_with_placeholder.image, pygame.Surface)
        # Check placeholder dimensions (these come from settings.py)
        assert test_car_with_placeholder.image.get_width() == settings.PLACEHOLDER_CAR_WIDTH
        assert test_car_with_placeholder.image.get_height() == settings.PLACEHOLDER_CAR_HEIGHT
        # Check rect center is set correctly even with placeholder
        assert test_car_with_placeholder.rect.centerx == car_x_pos
        assert test_car_with_placeholder.rect.centery == car_y_pos

        # Act
        # Call the draw method
        test_car_with_placeholder.draw()

        # Assert
        # Verify screen.blit was called with the placeholder image and its rect
        mock_screen_in_car_module.blit.assert_called_once_with(test_car_with_placeholder.image, test_car_with_placeholder.rect)