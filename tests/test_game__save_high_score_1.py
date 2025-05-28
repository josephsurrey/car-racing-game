# test_game__save_high_score.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from game import Game
import settings # Import settings to access HIGH_SCORE_FILE_PATH

@pytest.fixture
def game_instance(monkeypatch):
    # Mock pygame functionalities called in Game.__init__ to avoid side effects
    monkeypatch.setattr("pygame.init", MagicMock(name="pygame.init_mock"))
    monkeypatch.setattr("pygame.mixer.init", MagicMock(name="pygame.mixer.init_mock"))
    monkeypatch.setattr("pygame.display.set_mode", MagicMock(name="pygame.display.set_mode_mock"))
    monkeypatch.setattr("pygame.display.set_caption", MagicMock(name="pygame.display.set_caption_mock"))
    monkeypatch.setattr("pygame.time.Clock", MagicMock(name="pygame.time.Clock_mock"))
    # Provide a dummy value for pygame.USEREVENT if Game.__init__ uses it directly
    # game.py uses pygame.USEREVENT + 1, so pygame.USEREVENT itself needs to be an int
    monkeypatch.setattr("pygame.USEREVENT", 1000)
    monkeypatch.setattr("pygame.time.set_timer", MagicMock(name="pygame.time.set_timer_mock"))

    # Mock game-specific class instantiations in Game.__init__
    monkeypatch.setattr("game.Road", MagicMock(name="Road_mock"))
    monkeypatch.setattr("game.PlayerCar", MagicMock(name="PlayerCar_mock"))
    monkeypatch.setattr("game.UIManager", MagicMock(name="UIManager_mock"))

    # Mock pygame.sprite.Group as its methods might be called
    mock_sprite_group_instance = MagicMock()
    mock_sprite_group_class = MagicMock(return_value=mock_sprite_group_instance)
    monkeypatch.setattr("pygame.sprite.Group", mock_sprite_group_class)

    # Mock _load_high_score to prevent file access during Game.__init__
    # and ensure a predictable state for self.high_score
    with patch.object(Game, '_load_high_score', MagicMock(name="_load_high_score_mock")):
        game = Game()
        # Explicitly set initial high_score for tests after Game object is created
        game.high_score = 50 # Default initial high score for these tests
        game.score = 0      # Default initial score
        return game

def test_save_new_high_score_successful(game_instance):
    # Set current score to be higher than the initial high score
    game_instance.score = 100
    game_instance.high_score = 50 # Explicitly set for clarity, matches fixture default

    # Mock builtins.open for file writing
    mock_file_open = mock_open()
    with patch('builtins.open', mock_file_open):
        game_instance._save_high_score()

    # Assert high score in memory is updated
    assert game_instance.high_score == 100
    # Assert file was opened correctly for writing
    mock_file_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'w')
    # Assert new high score was written to the file
    # Access the mock for the file handle via .return_value
    mock_file_open.return_value.write.assert_called_once_with("100")

def test_save_score_not_higher_than_high_score(game_instance):
    # Set current score to be less than the initial high score
    game_instance.score = 30
    game_instance.high_score = 50 # Explicitly set for clarity

    # Mock builtins.open to ensure it's not called for writing
    mock_file_open = mock_open()
    with patch('builtins.open', mock_file_open):
        game_instance._save_high_score()

    # Assert high score in memory remains unchanged
    assert game_instance.high_score == 50
    # Assert file was not opened for writing
    mock_file_open.assert_not_called()

    # Test case for score equal to high score
    game_instance.score = 50
    # Reset mock_file_open call count if it persists across calls (it shouldn't for a new 'with' block, but good practice)
    mock_file_open = mock_open() # Re-initialize mock for a clean state in this part of the test
    with patch('builtins.open', mock_file_open):
        game_instance._save_high_score()

    # Assert high score in memory remains unchanged
    assert game_instance.high_score == 50
    # Assert file was not opened for writing
    mock_file_open.assert_not_called()

def test_save_new_high_score_io_error_on_write(game_instance):
    # Set current score to be higher than the initial high score
    game_instance.score = 100
    game_instance.high_score = 50 # Explicitly set for clarity

    # Mock builtins.open to simulate an IOError during file write
    mock_file_open = mock_open()
    # Configure the .write method on the mock *returned by* mock_file_open
    mock_file_open.return_value.write.side_effect = IOError("Simulated write error")

    # Patch builtins.print to capture its output
    with patch('builtins.open', mock_file_open), \
         patch('builtins.print') as mock_print:
        game_instance._save_high_score()

    # Assert high score in memory is updated (this happens before the try-except for file write)
    assert game_instance.high_score == 100
    # Assert attempt was made to open the file
    mock_file_open.assert_called_once_with(settings.HIGH_SCORE_FILE_PATH, 'w')
    # Assert attempt was made to write the new score, via the .return_value
    mock_file_open.return_value.write.assert_called_once_with("100")
    # Assert the specific error message was printed
    mock_print.assert_called_once_with("Error: Could not save high score to file.")