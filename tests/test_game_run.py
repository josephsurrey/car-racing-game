import pytest
from unittest.mock import MagicMock, patch
import pygame  # Import for Pygame constants if used directly, and for type hinting

# Assuming 'game.py' and 'settings.py' are in the python path
from game import Game
import settings


@pytest.fixture
def mock_pygame_essentials(mocker):
    """Mocks essential pygame components needed for Game instantiation and run"""
    mocker.patch('pygame.init', return_value=None)
    mocker.patch('pygame.mixer.init', return_value=None)
    mocker.patch('pygame.display.set_mode', return_value=MagicMock())  # Return a mock surface
    mocker.patch('pygame.display.set_caption', return_value=None)
    mocker.patch('pygame.display.flip', return_value=None)

    mock_clock_instance = MagicMock()
    # Ensure get_fps returns a value for the caption update
    mock_clock_instance.get_fps.return_value = settings.TARGET_FPS
    mocker.patch('pygame.time.Clock', return_value=mock_clock_instance)

    mocker.patch('pygame.time.set_timer', return_value=None)
    mocker.patch('pygame.quit', return_value=None)

    # Mock sprite group functionality minimally
    mock_sprite_group_instance = MagicMock()
    mock_sprite_group_instance.add = MagicMock()
    mock_sprite_group_instance.empty = MagicMock()
    mocker.patch('pygame.sprite.Group', return_value=mock_sprite_group_instance)

    # Mock classes instantiated by Game.__init__
    mocker.patch('car.PlayerCar', autospec=True)
    mocker.patch('road.Road', autospec=True)
    mocker.patch('ui_manager.UIManager', autospec=True)

    # Prevent file operations during tests
    mocker.patch('game.Game._load_high_score', return_value=None)

    return mock_clock_instance  # Return clock mock for assertions


@pytest.fixture
def game_instance(mock_pygame_essentials, mocker):
    """Creates a Game instance with mocked dependencies and methods for run()"""
    game = Game()
    # Mock internal methods called by run() to control their behavior and check calls
    game._handle_events = MagicMock()
    game._update_game_state = MagicMock()
    game._draw_elements = MagicMock()
    return game


def test_run_loop_single_iteration_and_termination(game_instance, mock_pygame_essentials, mocker):
    # This test covers GR01 (core calls, termination) and implicitly part of GR03 (quit on exit)

    # mock_pygame_essentials already returns the clock mock
    mock_clock = mock_pygame_essentials

    # Make _handle_events stop the loop after the first iteration
    def side_effect_handle_events_single_run():
        game_instance.running = False

    game_instance._handle_events.side_effect = side_effect_handle_events_single_run

    game_instance.run()

    # Check clock ticked once with target FPS
    mock_clock.tick.assert_called_once_with(settings.TARGET_FPS)
    # Check internal methods were called once
    game_instance._handle_events.assert_called_once()
    game_instance._update_game_state.assert_called_once()  # game_over is False by default
    game_instance._draw_elements.assert_called_once()
    # Check display flip was called (using the globally patched pygame.display.flip)
    pygame.display.flip.assert_called_once()
    # Check pygame quit was called (using the globally patched pygame.quit)
    pygame.quit.assert_called_once()
    # Check caption was updated in the loop (specific FPS content tested separately)
    # pygame.display.set_caption would have been called by __init__ and then by run()
    # For this test, ensuring it was called at least by run() is sufficient via checking total calls.
    # The initial call in __init__ + 1 call in the loop
    assert pygame.display.set_caption.call_count >= 1  # Simplified check for this test


def test_run_skips_update_game_state_when_game_over(game_instance, mock_pygame_essentials, mocker):
    # This test covers GR02

    # Set game_over to True
    game_instance.game_over = True

    # Make _handle_events stop the loop after the first iteration
    def side_effect_handle_events_game_over():
        game_instance.running = False

    game_instance._handle_events.side_effect = side_effect_handle_events_game_over

    game_instance.run()

    # Check _handle_events and _draw_elements were called
    game_instance._handle_events.assert_called_once()
    game_instance._draw_elements.assert_called_once()
    # Crucially, check _update_game_state was NOT called
    game_instance._update_game_state.assert_not_called()
    # Check other loop components still ran
    mock_pygame_essentials.tick.assert_called_once_with(settings.TARGET_FPS)
    pygame.display.flip.assert_called_once()
    pygame.quit.assert_called_once()


def test_run_loop_multiple_iterations(game_instance, mock_pygame_essentials, mocker):
    # This test covers GR03 (multiple iterations)

    mock_clock = mock_pygame_essentials
    loop_iterations = 3
    current_iteration = 0

    # Make _handle_events control the loop for a set number of iterations
    def side_effect_handle_events_multiple_runs():
        nonlocal current_iteration
        current_iteration += 1
        if current_iteration >= loop_iterations:
            game_instance.running = False

    game_instance._handle_events.side_effect = side_effect_handle_events_multiple_runs

    game_instance.run()

    # Check methods were called for each iteration
    assert mock_clock.tick.call_count == loop_iterations
    assert game_instance._handle_events.call_count == loop_iterations
    assert game_instance._update_game_state.call_count == loop_iterations  # game_over is False
    assert game_instance._draw_elements.call_count == loop_iterations
    assert pygame.display.flip.call_count == loop_iterations
    # Check pygame quit was called once at the end
    pygame.quit.assert_called_once()


def test_run_updates_caption_with_fps(game_instance, mock_pygame_essentials, mocker):
    # This test covers GR04

    # pygame.display.set_caption is mocked globally by mock_pygame_essentials
    # Reset mock to ignore the call from Game.__init__ for this specific assertion
    pygame.display.set_caption.reset_mock()

    # Define a specific FPS value for this test
    test_fps = 58.73
    mock_pygame_essentials.get_fps.return_value = test_fps  # mock_pygame_essentials is the clock mock

    # Make _handle_events stop the loop after the first iteration
    def side_effect_handle_events_caption_test():
        game_instance.running = False

    game_instance._handle_events.side_effect = side_effect_handle_events_caption_test

    game_instance.run()

    # Check set_caption was called once in the loop with the correct FPS string
    expected_caption = f"Car Racing Game - FPS: {test_fps:.2f}"
    pygame.display.set_caption.assert_called_once_with(expected_caption)