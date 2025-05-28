import pytest
from unittest.mock import patch, mock_open

# Assume game.py and settings.py are in the same directory or Python path
# This is a simplified setup for demonstration
# In a real project, ensure your Python path is configured correctly
# or use relative imports if your test files are structured within a package
import sys
import os

# Add the parent directory to sys.path to find game, settings, etc
# This is a common way to handle imports for standalone test scripts
# Adjust if your project structure is different
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # Assuming tests are in a subdir
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from game import Game
import settings # settings.py should be accessible

# Define a decorator to apply a list of mocks common to Game.__init__
# This helps reduce boilerplate in each test function
def apply_common_game_init_mocks(func):
    mocks = [
        patch('pygame.init', return_value=None),
        patch('pygame.mixer.init', return_value=None),
        patch('pygame.display.set_mode', return_value=None),
        patch('pygame.display.set_caption', return_value=None),
        patch('pygame.time.Clock', autospec=True),
        patch('game.Road', autospec=True), # Mock objects within the game module
        patch('game.PlayerCar', autospec=True),
        patch('game.UIManager', autospec=True),
        patch('pygame.sprite.Group', autospec=True),
        patch('pygame.time.set_timer', return_value=None)
    ]
    for m in reversed(mocks): # Apply decorators from bottom up
        func = m(func)
    return func

@apply_common_game_init_mocks
def test_load_high_score_file_exists_valid_content(*mock_args):
    # Mocks for Game.__init__ are applied by the decorator
    # *mock_args captures the mock objects passed by the decorator, but they aren't used directly here

    # Mock 'open' for this specific test case
    # Simulates a highscore file with '123' as its content
    m_open = mock_open(read_data="123")
    with patch('builtins.open', m_open):
        # Game.__init__ calls _load_high_score internally
        game_instance = Game()

    # Check that 'open' was called with the correct file path and mode
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Verify the high_score attribute was set correctly
    assert game_instance.high_score == 123

@apply_common_game_init_mocks
def test_load_high_score_file_not_found(*mock_args):
    # Mock 'open' to simulate FileNotFoundError when the high score file is accessed
    m_open = mock_open()
    m_open.side_effect = FileNotFoundError
    with patch('builtins.open', m_open):
        game_instance = Game()

    # Verify 'open' was called
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Check high_score is set to 0 as per the except block in _load_high_score
    assert game_instance.high_score == 0

@apply_common_game_init_mocks
def test_load_high_score_invalid_content(*mock_args):
    # Mock 'open' to simulate a file containing non-integer content
    m_open = mock_open(read_data="not_a_number")
    with patch('builtins.open', m_open):
        game_instance = Game()

    # Verify 'open' was called
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Check high_score is set to 0 due to ValueError during int() conversion
    assert game_instance.high_score == 0

@apply_common_game_init_mocks
def test_load_high_score_empty_file(*mock_args):
    # Mock 'open' to simulate an empty file
    # int("") will raise a ValueError
    m_open = mock_open(read_data="")
    with patch('builtins.open', m_open):
        game_instance = Game()

    # Verify 'open' was called
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Check high_score is set to 0 due to ValueError
    assert game_instance.high_score == 0

@apply_common_game_init_mocks
def test_load_high_score_negative_integer_content(*mock_args):
    # Mock 'open' for a file containing a negative integer
    m_open = mock_open(read_data="-50")
    with patch('builtins.open', m_open):
        game_instance = Game()

    # Verify 'open' was called
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Check high_score is correctly set to the negative integer
    assert game_instance.high_score == -50

@apply_common_game_init_mocks
def test_load_high_score_zero_content(*mock_args):
    # Mock 'open' for a file containing '0'
    m_open = mock_open(read_data="0")
    with patch('builtins.open', m_open):
        game_instance = Game()

    # Verify 'open' was called
    m_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'r')
    # Check high_score is correctly set to 0
    assert game_instance.high_score == 0