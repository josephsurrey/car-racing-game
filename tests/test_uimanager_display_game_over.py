import pytest
import pygame
from unittest.mock import Mock, patch, call
import settings  # Assuming settings.py is accessible
from ui_manager import UIManager  # Assuming ui_manager.py is accessible

# Mock Pygame initialization globally if UIManager or its dependencies call it at import time
# For UIManager, pygame.font.Font/SysFont is the main concern at init
pygame.font.init = Mock()  # Prevent actual font init


@pytest.fixture
def mock_pygame_settings(monkeypatch):
    # Mock settings used by UIManager and display_game_over
    monkeypatch.setattr(settings, 'SCREEN_WIDTH', 800)
    monkeypatch.setattr(settings, 'SCREEN_HEIGHT', 600)
    monkeypatch.setattr(settings, 'RED', (255, 0, 0))
    monkeypatch.setattr(settings, 'WHITE', (255, 255, 255))  # Used as default text_colour in UIManager
    monkeypatch.setattr(settings, 'GREEN', (0, 255, 0))
    # pygame.SRCALPHA is a Pygame constant, not from settings


@pytest.fixture
def ui_manager_instance(mock_pygame_settings):
    # Create distinct mock font objects that will be assigned during UIManager init
    mock_default_font_obj = Mock()
    mock_medium_font_obj = Mock()
    mock_large_font_obj = Mock()

    # Patch pygame.font.Font to return these mocks in the order they are called in UIManager.__init__
    with patch('pygame.font.Font',
               side_effect=[mock_default_font_obj, mock_medium_font_obj, mock_large_font_obj]) as mock_font_constructor, \
            patch('pygame.font.SysFont') as mock_sysfont_constructor:  # Patch SysFont in case Font fails

        # Instantiate UIManager, this will use the patched Font constructor
        # The UIManager __init__ parameter is 'text_colour' (as per provided ui_manager.py),
        # which defaults to settings.WHITE. It then assigns this to self.text_colour.
        ui = UIManager(font_name="dummy_font.ttf")

        # Verify fonts were assigned as expected by the side_effect
        assert ui.default_font is mock_default_font_obj
        assert ui.medium_font is mock_medium_font_obj
        assert ui.large_font is mock_large_font_obj

        return ui


@pytest.fixture
def mock_screen():
    # Mock for the screen surface
    screen = Mock(spec=pygame.Surface)
    screen.blit = Mock()
    return screen


def test_display_game_over_typical_scores_all_elements(ui_manager_instance, mock_screen, mock_pygame_settings):
    # Test Number 1: Display game over screen with typical scores
    # Expected Outcome: All elements are blitted to the screen with correct content, fonts, colours, and positions

    # Arrange
    score = 100  # Typical score
    high_score = 200  # Typical high score

    # Mock surfaces and rects that render methods would create
    # Each font's render method will be mocked to return a specific surface
    mock_surface_game_over = Mock(spec=pygame.Surface)
    mock_rect_game_over = pygame.Rect(0, 0, 100, 50)  # Arbitrary size
    mock_surface_game_over.get_rect = Mock(return_value=mock_rect_game_over)

    mock_surface_final_score = Mock(spec=pygame.Surface)
    mock_rect_final_score = pygame.Rect(0, 0, 80, 40)
    mock_surface_final_score.get_rect = Mock(return_value=mock_rect_final_score)

    mock_surface_high_score = Mock(spec=pygame.Surface)
    mock_rect_high_score = pygame.Rect(0, 0, 80, 40)
    mock_surface_high_score.get_rect = Mock(return_value=mock_rect_high_score)

    mock_surface_restart = Mock(spec=pygame.Surface)
    mock_rect_restart = pygame.Rect(0, 0, 70, 30)
    mock_surface_restart.get_rect = Mock(return_value=mock_rect_restart)

    # Configure the render methods of the mocked font objects
    # This checks that the correct font objects (large, medium, default) are used for rendering
    ui_manager_instance.large_font.render = Mock(return_value=mock_surface_game_over)
    ui_manager_instance.medium_font.render = Mock(side_effect=[mock_surface_final_score, mock_surface_high_score])
    ui_manager_instance.default_font.render = Mock(return_value=mock_surface_restart)

    # Mock pygame.Surface constructor for the overlay
    mock_overlay_surface = Mock(spec=pygame.Surface)
    mock_overlay_surface.fill = Mock()

    # Act
    with patch('pygame.Surface', return_value=mock_overlay_surface) as mock_pygame_surface_constructor:
        ui_manager_instance.display_game_over(mock_screen, score, high_score)

    # Assert overlay creation and blit
    # This checks the overlay's properties
    mock_pygame_surface_constructor.assert_called_once_with(
        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA
    )
    mock_overlay_surface.fill.assert_called_once_with((0, 0, 0, 180))  # Checks overlay color

    # Assert font render calls (checks content and colors)
    ui_manager_instance.large_font.render.assert_called_once_with("GAME OVER", True, settings.RED)

    # Uses .text_colour which matches the provided ui_manager.py
    expected_medium_font_calls = [
        call(f"Final Score: {score}", True, ui_manager_instance.text_colour),
        call(f"High Score: {high_score}", True, ui_manager_instance.text_colour)
    ]
    ui_manager_instance.medium_font.render.assert_has_calls(expected_medium_font_calls)
    assert ui_manager_instance.medium_font.render.call_count == 2

    ui_manager_instance.default_font.render.assert_called_once_with("Press R to Restart", True, settings.GREEN)

    # Assert rect centering (checks positions)
    assert mock_rect_game_over.center == (int(settings.SCREEN_WIDTH / 2), int(settings.SCREEN_HEIGHT / 2 - 100))
    assert mock_rect_final_score.center == (int(settings.SCREEN_WIDTH / 2), int(settings.SCREEN_HEIGHT / 2))
    assert mock_rect_high_score.center == (int(settings.SCREEN_WIDTH / 2), int(settings.SCREEN_HEIGHT / 2 + 60))
    assert mock_rect_restart.center == (int(settings.SCREEN_WIDTH / 2), int(settings.SCREEN_HEIGHT / 2 + 130))

    # Assert blit calls in order (checks all elements are drawn in sequence)
    expected_blit_calls = [
        call(mock_overlay_surface, (0, 0)),
        call(mock_surface_game_over, mock_rect_game_over),
        call(mock_surface_final_score, mock_rect_final_score),
        call(mock_surface_high_score, mock_rect_high_score),
        call(mock_surface_restart, mock_rect_restart),
    ]
    mock_screen.blit.assert_has_calls(expected_blit_calls, any_order=False)
    assert mock_screen.blit.call_count == 5