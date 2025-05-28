import pytest
from unittest.mock import MagicMock, patch

# Define a dictionary for mocked settings values
# This helps in centralizing mock values and ensuring consistency
MOCK_SETTINGS_VALUES = {
    "SCREEN_WIDTH": 800,
    "SCREEN_HEIGHT": 600,
    "ROAD_IMAGE_PATH": "mock_assets/road.png",
    "PLAYER_IMAGE_PATH": "mock_assets/player.png",
    "PLAYER_START_X_POS": 400,
    "PLAYER_Y_POS": 500,
    "HORIZONTAL_SPEED_CONSTANT": 5,
    "NPC_SPAWN_INTERVAL": 1.5,
    "TARGET_FPS": 60,  # Used in Game.__init__ via clock.tick, though not directly tested here
    "BLACK": (10, 20, 30),  # A distinct color for testing fill
    "HIGH_SCORE_FILE_PATH": "dummy_highscore.txt"  # For _load_high_score if it were active
    # Add other settings if Game.__init__ requires them
}


@pytest.fixture
def mock_game_environment():
    """
    Provides a mocked environment for Game class instantiation
    Mocks pygame, dependent classes (Road, PlayerCar, UIManager), and the settings module
    """
    # Patch all external dependencies of the Game class constructor and _draw_elements method
    with patch('game.pygame') as mock_pygame, \
            patch('game.Road') as MockRoad, \
            patch('game.PlayerCar') as MockPlayerCar, \
            patch('game.UIManager') as MockUIManager, \
            patch('game.settings', MagicMock(**MOCK_SETTINGS_VALUES)) as mock_settings_module:
        # Configure mock_pygame attributes and methods called during Game.__init__
        mock_pygame.init = MagicMock(name="pygame_init_func")
        mock_pygame.mixer.init = MagicMock(name="pygame_mixer_init_func")

        # self.screen is set by pygame.display.set_mode
        mock_screen_surface = MagicMock(name="mock_screen_surface")
        mock_pygame.display.set_mode.return_value = mock_screen_surface
        mock_pygame.display.set_caption = MagicMock(name="pygame_set_caption_func")

        # self.clock
        mock_pygame.time.Clock.return_value = MagicMock(name="mock_pygame_clock")

        # self.NPC_SPAWN_EVENT and timer
        mock_pygame.USEREVENT = 100  # Define a base for USEREVENT for predictability
        mock_pygame.time.set_timer = MagicMock(name="pygame_set_timer_func")

        # Sprite groups: Game.__init__ creates two: self.all_sprites and self.npc_cars
        # We use side_effect to return distinct mocks for each call to pygame.sprite.Group()
        mock_all_sprites_group = MagicMock(name="all_sprites_pygame_group")
        mock_npc_cars_group = MagicMock(name="npc_cars_pygame_group")
        mock_pygame.sprite.Group.side_effect = [mock_all_sprites_group, mock_npc_cars_group]

        # Mock instances that Game creates internally
        mock_road_instance = MockRoad.return_value
        mock_player_car_instance = MockPlayerCar.return_value
        mock_ui_manager_instance = MockUIManager.return_value

        # The _load_high_score method is 'pass' in the provided code
        # If it performed I/O, it would need patching, e.g.,
        # with patch('game.Game._load_high_score', MagicMock()) as mock_load_high_score:
        # For now, no extra patch is needed for it specifically for these tests

        # Import Game class here, ensuring it uses the patched dependencies
        from game import Game

        # Yield a dictionary of the Game class and its key mocked components
        yield {
            "Game_class": Game,
            "mock_screen_surface": mock_screen_surface,
            "mock_road_instance": mock_road_instance,
            "mock_player_car_instance": mock_player_car_instance,
            # Not directly used by _draw_elements but part of setup
            "mock_ui_manager_instance": mock_ui_manager_instance,
            "mock_all_sprites_group": mock_all_sprites_group,
            "mock_settings_module": mock_settings_module  # Contains MOCK_SETTINGS_VALUES.BLACK
        }


def test_draw_elements_when_game_not_over(mock_game_environment):
    # Arrange
    # Retrieve the Game class and necessary mocks from the fixture
    Game = mock_game_environment["Game_class"]
    mock_ui_manager = mock_game_environment["mock_ui_manager_instance"]
    mock_road = mock_game_environment["mock_road_instance"]
    mock_all_sprites = mock_game_environment["mock_all_sprites_group"]
    # game_instance.screen will be this mock object
    mock_screen = mock_game_environment["mock_screen_surface"]

    # Instantiate the game using the mocked environment
    game_instance = Game()

    # Configure game state for this specific test case
    game_instance.game_over = False
    game_instance.score = 150
    game_instance.high_score = 300

    # Ensure game_instance.screen.fill is a fresh MagicMock for this test call
    # This allows asserting calls specifically made by _draw_elements
    mock_screen.fill = MagicMock(name="screen_fill_method_mock")

    # Act
    # Call the _draw_elements method which is under test
    game_instance._draw_elements()

    # Assert
    # Verify screen is filled with the BLACK color from mocked settings
    mock_screen.fill.assert_called_once_with(MOCK_SETTINGS_VALUES["BLACK"])
    # Verify road is drawn onto the screen
    mock_road.draw.assert_called_once_with(mock_screen)
    # Verify all game sprites are drawn onto the screen
    mock_all_sprites.draw.assert_called_once_with(mock_screen)
    # Verify score is displayed
    mock_ui_manager.display_score.assert_called_once_with(mock_screen, game_instance.score)
    # Verify high score is displayed
    mock_ui_manager.display_high_score.assert_called_once_with(mock_screen, game_instance.high_score)
    # Verify game over screen is NOT displayed when game is not over
    mock_ui_manager.display_game_over.assert_not_called()


def test_draw_elements_when_game_is_over(mock_game_environment):
    # Arrange
    # Retrieve the Game class and necessary mocks
    Game = mock_game_environment["Game_class"]
    mock_ui_manager = mock_game_environment["mock_ui_manager_instance"]
    mock_road = mock_game_environment["mock_road_instance"]
    mock_all_sprites = mock_game_environment["mock_all_sprites_group"]
    mock_screen = mock_game_environment["mock_screen_surface"]

    # Instantiate the game
    game_instance = Game()

    # Configure game state for game over scenario
    game_instance.game_over = True
    game_instance.score = 50
    game_instance.high_score = 250  # Example high score

    # Ensure game_instance.screen.fill is a fresh MagicMock
    mock_screen.fill = MagicMock(name="screen_fill_method_mock")

    # Act
    # Call the _draw_elements method
    game_instance._draw_elements()

    # Assert
    # Verify screen fill, road draw, and sprite draw happen as usual
    mock_screen.fill.assert_called_once_with(MOCK_SETTINGS_VALUES["BLACK"])
    mock_road.draw.assert_called_once_with(mock_screen)
    mock_all_sprites.draw.assert_called_once_with(mock_screen)
    # Verify score and high score are still displayed
    mock_ui_manager.display_score.assert_called_once_with(mock_screen, game_instance.score)
    mock_ui_manager.display_high_score.assert_called_once_with(mock_screen, game_instance.high_score)
    # Verify game over screen IS displayed with correct current score and high score
    mock_ui_manager.display_game_over.assert_called_once_with(mock_screen, game_instance.score,
                                                              game_instance.high_score)