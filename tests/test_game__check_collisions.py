import pytest
from unittest.mock import patch, MagicMock

# --- Mocks for modules and classes ---
# Mock settings module
mock_settings = MagicMock()
mock_settings.SCREEN_WIDTH = 840
mock_settings.SCREEN_HEIGHT = 650
mock_settings.PLAYER_IMAGE_PATH = "assets/player-image.png"
mock_settings.PLAYER_START_X_POS = mock_settings.SCREEN_WIDTH / 2
mock_settings.PLAYER_Y_POS = 400
mock_settings.HORIZONTAL_SPEED_CONSTANT = 100
mock_settings.NPC_IMAGE_PATH = "assets/npc-image.png"
mock_settings.ROAD_IMAGE_PATH = "assets/background.png"
mock_settings.BLACK = (0, 0, 0)
mock_settings.NPC_SPAWN_INTERVAL = 1.0 # Used in Game.__init__
mock_settings.MAX_NPCS = 10
mock_settings.LANE_POSITIONS = [270, 370, 470, 570]
mock_settings.PLACEHOLDER_NPC_HEIGHT = 100
mock_settings.NPC_MIN_SPEED = 20
mock_settings.NPC_MAX_SPEED = 100
mock_settings.TARGET_FPS = 60
mock_settings.ACCELERATION_CONSTANT = 5
mock_settings.BRAKING_CONSTANT = 10
mock_settings.MAX_SPEED = 100

# Mock pygame module and its submodules/functions
mock_pygame = MagicMock()
mock_pygame.sprite = MagicMock()
# Define a mock Sprite base that can be used for isinstance checks or subclassing by mocks
mock_pygame.sprite.Sprite = type('Sprite', (object,), {'__init__': MagicMock()})
# Mock Group constructor to return a mock group instance with necessary methods/attributes
mock_pygame.sprite.Group = MagicMock(return_value=MagicMock(spec_set=['add', 'update', 'draw', 'empty', 'sprites']))
mock_pygame.display = MagicMock()
mock_pygame.time = MagicMock()
mock_pygame.event = MagicMock()
mock_pygame.mixer = MagicMock()
mock_pygame.image = MagicMock()
mock_pygame.transform = MagicMock()
mock_pygame.USEREVENT = 24 # A common starting value for USEREVENT

# Mock classes from other game files imported by game.py
MockPlayerCarClass = MagicMock(spec_set=['update', 'move_horizontal'])
MockNPCCarClass = MagicMock(spec_set=['update'])
MockRoadClass = MagicMock(spec_set=['update', 'draw'])
MockUIManagerClass = MagicMock(spec_set=['display_score', 'display_high_score', 'display_game_over'])


# --- Pytest Fixture for Game instance ---
@pytest.fixture
@patch.dict('sys.modules', {
    'pygame': mock_pygame,
    'settings': mock_settings,
    'car': MagicMock(PlayerCar=MockPlayerCarClass, NPCCar=MockNPCCarClass),
    'road': MagicMock(Road=MockRoadClass),
    'ui_manager': MagicMock(UIManager=MockUIManagerClass)
})
def game_instance_fixture():
    # Reset mocks called during Game.__init__ for a clean state per test
    mock_pygame.init.reset_mock()
    mock_pygame.mixer.init.reset_mock()
    mock_pygame.display.set_mode.reset_mock()
    mock_pygame.display.set_caption.reset_mock()
    mock_pygame.time.Clock.reset_mock()
    mock_pygame.time.set_timer.reset_mock()

    # Ensure the Group mock constructor and its return value are reset
    mock_pygame.sprite.Group.reset_mock(return_value=MagicMock(spec_set=['add', 'update', 'draw', 'empty', 'sprites']))

    MockPlayerCarClass.reset_mock()
    MockRoadClass.reset_mock()
    MockUIManagerClass.reset_mock()
    # NPCCarClass is not directly instantiated in __init__ but good practice if it were
    MockNPCCarClass.reset_mock()


    # Import Game class *inside* the fixture, after patches are applied
    from game import Game
    game = Game()

    # Directly mock attributes relevant to _check_collisions
    # game.player_car is an instance of MockPlayerCarClass due to patching Game's import of car.PlayerCar
    # For clarity, we can re-assign or ensure it's a simple mock if specific PlayerCar methods aren't called by _check_collisions
    game.player_car = MagicMock() # A simple mock for the player_car instance
    game.npc_cars = mock_pygame.sprite.Group() # Get a fresh mock group instance
    game.game_over = False # Set initial state
    game._save_high_score = MagicMock() # Mock the _save_high_score method

    # Reset the mock for pygame.sprite.spritecollideany for each test
    mock_pygame.sprite.spritecollideany = MagicMock()
    return game

# --- Test Class for _check_collisions ---
class TestGameCheckCollisions:

    def test_no_collision_detected(self, game_instance_fixture):
        # Arrange
        game = game_instance_fixture
        # game.game_over is already False from fixture setup
        # Configure spritecollideany to return None, simulating no collision
        mock_pygame.sprite.spritecollideany.return_value = None

        # Act
        game._check_collisions()

        # Assert
        # game_over state should remain False
        assert game.game_over is False
        # _save_high_score method should not have been called
        game._save_high_score.assert_not_called()
        # Verify spritecollideany was called with the player car and npc car group
        mock_pygame.sprite.spritecollideany.assert_called_once_with(game.player_car, game.npc_cars)

    def test_collision_detected(self, game_instance_fixture):
        # Arrange
        game = game_instance_fixture
        # game.game_over is already False from fixture setup
        # Create a mock object to be returned by spritecollideany, simulating a collided NPC
        mock_collided_npc = MagicMock()
        mock_pygame.sprite.spritecollideany.return_value = mock_collided_npc

        # Act
        game._check_collisions()

        # Assert
        # game_over state should become True
        assert game.game_over is True
        # _save_high_score method should have been called once
        game._save_high_score.assert_called_once()
        # Verify spritecollideany was called with the player car and npc car group
        mock_pygame.sprite.spritecollideany.assert_called_once_with(game.player_car, game.npc_cars)