import pytest
import pygame
from unittest.mock import MagicMock, patch

# Assuming UIManager and settings are in the python path or same directory
from ui_manager import UIManager
import settings

# Initialize pygame font module, good practice for tests involving fonts
pygame.font.init()

@pytest.fixture
def mock_screen_fixture():
    """Provides a mock pygame screen surface"""
    screen = MagicMock(spec=pygame.Surface)
    screen.blit = MagicMock() # Mock the blit method
    return screen

def create_ui_manager_with_mocked_fonts(font_name=None, font_size=36, text_color=settings.WHITE):
    """
    Helper function to create a UIManager instance with pygame.font.Font
    and pygame.font.SysFont mocked to return a controllable mock font object
    Returns the UIManager instance and the mock font object assigned to default_font
    """
    # This mock_font_obj will be returned by pygame.font.Font() or pygame.font.SysFont()
    mock_font_obj = MagicMock(spec=pygame.font.Font)

    # Patch Font and SysFont within this context
    # UIManager's __init__ will use these patched versions
    with patch('pygame.font.Font', return_value=mock_font_obj) as _mock_font_class, \
         patch('pygame.font.SysFont', return_value=mock_font_obj) as _mock_sysfont_class:
        ui_manager = UIManager(font_name=font_name, font_size=font_size, text_color=text_color)

    # ui_manager.default_font (and medium/large) will now be mock_font_obj
    return ui_manager, mock_font_obj

def test_display_high_score_positive_value(mock_screen_fixture):
    # Test displaying a typical positive high score
    ui_manager, mock_default_font_instance = create_ui_manager_with_mocked_fonts()

    # Setup the mock font's render method and the surface it returns
    mock_rendered_surface = MagicMock(spec=pygame.Surface)
    # The rect returned by get_rect() is used for positioning
    mock_rect_from_render = pygame.Rect(0, 0, 150, 30) # Arbitrary size for the mock rect
    mock_rendered_surface.get_rect = MagicMock(return_value=mock_rect_from_render)
    mock_default_font_instance.render = MagicMock(return_value=mock_rendered_surface)

    high_score_to_display = 12345
    expected_text_output = f"High Score: {high_score_to_display}"

    # Call the method under test
    ui_manager.display_high_score(mock_screen_fixture, high_score_to_display)

    # Verify font.render was called with correct arguments
    mock_default_font_instance.render.assert_called_once_with(
        expected_text_output, True, ui_manager.text_color # Default color is WHITE
    )

    # Verify screen.blit was called correctly
    # The rect passed to blit should have its topright set
    expected_top_right_pos = (ui_manager.screen_width - 20, 20)

    args_call_blit, _ = mock_screen_fixture.blit.call_args
    blitted_surface_arg, blitted_rect_arg = args_call_blit

    assert blitted_surface_arg == mock_rendered_surface
    assert blitted_rect_arg.topright == expected_top_right_pos
    # Ensure the rect object whose topright was set is the one from get_rect()
    assert blitted_rect_arg is mock_rect_from_render
    # Corrected assertion: use .assert_called_once() method
    mock_rendered_surface.get_rect.assert_called_once() # Ensure get_rect was used

def test_display_high_score_zero_value(mock_screen_fixture):
    # Test displaying a high score of zero
    ui_manager, mock_default_font_instance = create_ui_manager_with_mocked_fonts()

    mock_rendered_surface = MagicMock(spec=pygame.Surface)
    mock_rect_from_render = pygame.Rect(0, 0, 100, 30)
    mock_rendered_surface.get_rect = MagicMock(return_value=mock_rect_from_render)
    mock_default_font_instance.render = MagicMock(return_value=mock_rendered_surface)

    high_score_to_display = 0
    expected_text_output = f"High Score: {high_score_to_display}"

    ui_manager.display_high_score(mock_screen_fixture, high_score_to_display)

    mock_default_font_instance.render.assert_called_once_with(
        expected_text_output, True, ui_manager.text_color
    )

    args_call_blit, _ = mock_screen_fixture.blit.call_args
    blitted_surface_arg, blitted_rect_arg = args_call_blit

    expected_top_right_pos = (ui_manager.screen_width - 20, 20)
    assert blitted_surface_arg == mock_rendered_surface
    assert blitted_rect_arg.topright == expected_top_right_pos
    assert blitted_rect_arg is mock_rect_from_render
    # Corrected assertion: use .assert_called_once() method
    mock_rendered_surface.get_rect.assert_called_once()

def test_display_high_score_negative_value(mock_screen_fixture):
    # Test displaying a negative high score (edge case)
    ui_manager, mock_default_font_instance = create_ui_manager_with_mocked_fonts()

    mock_rendered_surface = MagicMock(spec=pygame.Surface)
    mock_rect_from_render = pygame.Rect(0, 0, 110, 30)
    mock_rendered_surface.get_rect = MagicMock(return_value=mock_rect_from_render)
    mock_default_font_instance.render = MagicMock(return_value=mock_rendered_surface)

    high_score_to_display = -50
    expected_text_output = f"High Score: {high_score_to_display}"

    ui_manager.display_high_score(mock_screen_fixture, high_score_to_display)

    mock_default_font_instance.render.assert_called_once_with(
        expected_text_output, True, ui_manager.text_color
    )

    args_call_blit, _ = mock_screen_fixture.blit.call_args
    blitted_surface_arg, blitted_rect_arg = args_call_blit

    expected_top_right_pos = (ui_manager.screen_width - 20, 20)
    assert blitted_surface_arg == mock_rendered_surface
    assert blitted_rect_arg.topright == expected_top_right_pos
    assert blitted_rect_arg is mock_rect_from_render
    # Corrected assertion: use .assert_called_once() method
    mock_rendered_surface.get_rect.assert_called_once()