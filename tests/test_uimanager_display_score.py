import pytest
from unittest.mock import MagicMock
# pygame needs to be importable, but its methods will be mocked
import pygame
# settings is needed for UIManager's default text_color
import settings
# The class to be tested
from ui_manager import UIManager


# It's good practice to initialize pygame.font if SysFont is used,
# though heavy mocking might make it optional
# pygame.font.init() # Uncomment if tests fail due to font system not being ready

@pytest.fixture
def mock_font_setup(mocker):
    """
    Mocks pygame.font.Font and pygame.font.SysFont constructors
    Ensures that UIManager instances use a MagicMock for font operations
    """
    # Create a mock font object that will be returned by pygame.font.Font() or pygame.font.SysFont()
    mock_font_instance = MagicMock(spec=pygame.font.Font)

    # Create a mock surface that font.render() will return
    mock_surface_instance = MagicMock(spec=pygame.Surface)

    # Create a mock rect that surface.get_rect() will return
    mock_rect_instance = MagicMock(spec=pygame.Rect)
    # Initialize topleft, as it will be modified by the SUT
    mock_rect_instance.topleft = (0, 0)

    # Configure the mock surface's get_rect() method to return our mock rect
    mock_surface_instance.get_rect.return_value = mock_rect_instance

    # Configure the mock font's render() method to return our mock surface
    mock_font_instance.render.return_value = mock_surface_instance

    # Patch the actual pygame.font.Font and pygame.font.SysFont constructors
    # UIManager uses Font first, then SysFont in an except block
    mocker.patch('pygame.font.Font', return_value=mock_font_instance)
    mocker.patch('pygame.font.SysFont', return_value=mock_font_instance)  # For the fallback path

    # The fixture doesn't need to return these as they are accessed via UIManager instance
    # or through the mocked constructors if direct checks are needed,
    # but returning them can be useful for direct assertions on the mocks if preferred.
    # For this test, we'll access them via ui_manager.default_font.
    return mock_font_instance  # ui_manager.default_font will be this mock


def test_display_score_positive_value(mock_font_setup):
    # Arrange
    # mock_font_setup fixture ensures UIManager uses a mock font
    ui_manager = UIManager()  # Initializes with default font_name=None, font_size=36

    # The default_font in ui_manager is now our mock_font_instance from the fixture
    mock_default_font = ui_manager.default_font

    mock_screen = MagicMock(spec=pygame.Surface)  # Mock the screen object
    test_score = 100
    expected_text = f"Score: {test_score}"
    expected_topleft_position = (20, 20)

    # Act
    ui_manager.display_score(mock_screen, test_score)

    # Assert
    # Check that font.render was called correctly on the default font
    mock_default_font.render.assert_called_once_with(expected_text, True, ui_manager.text_color)

    # Get the mock surface that render() returned
    rendered_mock_surface = mock_default_font.render.return_value

    # Check that get_rect was called on this surface
    rendered_mock_surface.get_rect.assert_called_once_with()

    # Get the mock rect that get_rect() returned
    returned_mock_rect = rendered_mock_surface.get_rect.return_value

    # Check that the rect's topleft was set to the expected position
    assert returned_mock_rect.topleft == expected_topleft_position

    # Check that screen.blit was called with the rendered surface and the positioned rect
    mock_screen.blit.assert_called_once_with(rendered_mock_surface, returned_mock_rect)


def test_display_score_zero_value(mock_font_setup):
    # Arrange
    ui_manager = UIManager()
    mock_default_font = ui_manager.default_font

    mock_screen = MagicMock(spec=pygame.Surface)
    test_score = 0
    expected_text = f"Score: {test_score}"  # This will be "Score: 0"
    expected_topleft_position = (20, 20)

    # Act
    ui_manager.display_score(mock_screen, test_score)

    # Assert
    # Check font.render call
    mock_default_font.render.assert_called_once_with(expected_text, True, ui_manager.text_color)

    # Get rendered surface and check get_rect call
    rendered_mock_surface = mock_default_font.render.return_value
    rendered_mock_surface.get_rect.assert_called_once_with()

    # Get returned rect and check topleft assignment
    returned_mock_rect = rendered_mock_surface.get_rect.return_value
    assert returned_mock_rect.topleft == expected_topleft_position

    # Check screen.blit call
    mock_screen.blit.assert_called_once_with(rendered_mock_surface, returned_mock_rect)