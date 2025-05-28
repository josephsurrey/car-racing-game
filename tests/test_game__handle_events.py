import pytest
import pygame  # Make sure pygame is imported
from unittest.mock import Mock, patch

# Assuming game.py, car.py, settings.py are in paths accessible by pytest
from game import Game
import settings


# CORRECTED Helper to create a mock key_pressed state
# This returns an object that mimics the behavior of the sequence from pygame.key.get_pressed()
# It handles large key constants like pygame.K_UP by using a dictionary internally.
def mock_key_state(pressed_keys_tuple=None):
    _pressed_keys_map = {}
    if pressed_keys_tuple:
        for key_const in pressed_keys_tuple:
            _pressed_keys_map[key_const] = True

    class MockKeyArray:
        def __init__(self, pressed_map):
            self.pressed_map = pressed_map

        def __getitem__(self, key_code):
            # Return True if key_code is in our map of pressed keys, False otherwise
            return self.pressed_map.get(key_code, False)

        # The __len__ might not be strictly necessary if the game code (or Pygame internals
        # called by the game code) doesn't use len() on the key state array.
        # Pygame's K_LAST is 323. Some systems use 512 for scancode arrays.
        # Providing a common length like 512 is a reasonable default.
        def __len__(self):
            return 512  # Or pygame.K_LAST + 1 (which is 324)

    return MockKeyArray(_pressed_keys_map)


@pytest.fixture
def game_instance(mocker):
    # Mock pygame's core functionalities that are called in Game.__init__
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock')
    mocker.patch('pygame.time.set_timer')

    # Mock classes instantiated by Game and their methods
    # PlayerCar mock needs a move_horizontal method
    mock_player_car_instance = Mock(
        spec_set=['move_horizontal'])  # spec_set ensures only move_horizontal can be called/mocked
    mock_player_car_instance.move_horizontal = Mock()
    mocker.patch('car.PlayerCar', return_value=mock_player_car_instance)

    mocker.patch('road.Road')
    mocker.patch('ui_manager.UIManager')

    # Mock sprite group and its add method
    mock_sprite_group_instance = Mock()
    mock_sprite_group_instance.add = Mock()
    mocker.patch('pygame.sprite.Group', return_value=mock_sprite_group_instance)

    mocker.patch('game.Game._load_high_score')

    game = Game()
    # Ensure game.player_car is the mock we configured
    game.player_car = mock_player_car_instance

    # Mock methods that _handle_events might call on the game instance itself
    game._reset_game = Mock()
    game._spawn_npc_car = Mock()

    # Ensure NPC_SPAWN_EVENT is defined as it is in __init__
    game.NPC_SPAWN_EVENT = pygame.USEREVENT + 1

    # Set initial states
    game.running = True
    game.game_over = False
    game.current_road_speed = 0
    return game


# Test cases

def test_handle_event_quit(game_instance, mocker):
    # Arrange
    quit_event = pygame.event.Event(pygame.QUIT)
    mocker.patch('pygame.event.get', return_value=[quit_event])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state())  # No keys pressed

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.running is False


def test_handle_event_reset_game_when_over(game_instance, mocker):
    # Arrange
    game_instance.game_over = True
    reset_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
    mocker.patch('pygame.event.get', return_value=[reset_event])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state())

    # Act
    game_instance._handle_events()

    # Assert
    game_instance._reset_game.assert_called_once()
    assert game_instance.running is True  # Resetting does not quit


def test_handle_event_quit_via_escape_when_over(game_instance, mocker):
    # Arrange
    game_instance.game_over = True
    escape_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    mocker.patch('pygame.event.get', return_value=[escape_event])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state())

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.running is False


def test_handle_event_npc_spawn_when_not_over(game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    spawn_event = pygame.event.Event(game_instance.NPC_SPAWN_EVENT)
    mocker.patch('pygame.event.get', return_value=[spawn_event])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state())

    # Act
    game_instance._handle_events()

    # Assert
    game_instance._spawn_npc_car.assert_called_once()


@pytest.mark.parametrize("key", [pygame.K_UP, pygame.K_w])
def test_handle_keys_accelerate(key, game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    game_instance.current_road_speed = 10
    mocker.patch('pygame.event.get', return_value=[])  # No quit/spawn events
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((key,)))

    expected_speed = min(settings.MAX_SPEED, 10 + settings.ACCELERATION_CONSTANT)

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.current_road_speed == expected_speed


@pytest.mark.parametrize("key", [pygame.K_DOWN, pygame.K_s])
def test_handle_keys_brake(key, game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    game_instance.current_road_speed = 20
    mocker.patch('pygame.event.get', return_value=[])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((key,)))

    expected_speed = max(0, 20 - settings.BRAKING_CONSTANT)

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.current_road_speed == expected_speed


@pytest.mark.parametrize("key, expected_arg", [
    (pygame.K_LEFT, -settings.HORIZONTAL_SPEED_CONSTANT),
    (pygame.K_a, -settings.HORIZONTAL_SPEED_CONSTANT)
])
def test_handle_keys_move_left(key, expected_arg, game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    mocker.patch('pygame.event.get', return_value=[])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((key,)))

    # Act
    game_instance._handle_events()

    # Assert
    game_instance.player_car.move_horizontal.assert_called_once_with(expected_arg)


@pytest.mark.parametrize("key, expected_arg", [
    (pygame.K_RIGHT, settings.HORIZONTAL_SPEED_CONSTANT),
    (pygame.K_d, settings.HORIZONTAL_SPEED_CONSTANT)
])
def test_handle_keys_move_right(key, expected_arg, game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    mocker.patch('pygame.event.get', return_value=[])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((key,)))

    # Act
    game_instance._handle_events()

    # Assert
    game_instance.player_car.move_horizontal.assert_called_once_with(expected_arg)


def test_accelerate_at_max_speed(game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    game_instance.current_road_speed = settings.MAX_SPEED
    mocker.patch('pygame.event.get', return_value=[])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((pygame.K_UP,)))

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.current_road_speed == settings.MAX_SPEED


def test_brake_at_zero_speed(game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    game_instance.current_road_speed = 0
    mocker.patch('pygame.event.get', return_value=[])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((pygame.K_DOWN,)))

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.current_road_speed == 0


def test_no_relevant_events_or_keys(game_instance, mocker):
    # Arrange
    game_instance.game_over = False
    initial_speed = 50
    game_instance.current_road_speed = initial_speed
    initial_running_state = game_instance.running  # Should be True
    mocker.patch('pygame.event.get', return_value=[])  # No events
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state())  # No keys

    # Act
    game_instance._handle_events()

    # Assert
    assert game_instance.running == initial_running_state
    assert game_instance.current_road_speed == initial_speed
    game_instance._reset_game.assert_not_called()
    game_instance._spawn_npc_car.assert_not_called()
    game_instance.player_car.move_horizontal.assert_not_called()


def test_game_over_key_r_when_not_game_over(game_instance, mocker):
    # Arrange
    game_instance.game_over = False  # Game is NOT over
    key_r_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
    # Simulate pressing UP key as well to see if normal key handling proceeds
    mocker.patch('pygame.event.get', return_value=[key_r_event])
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((pygame.K_UP,)))

    initial_speed = game_instance.current_road_speed

    # Act
    game_instance._handle_events()

    # Assert
    game_instance._reset_game.assert_not_called()  # R key event does nothing if not game over
    # Check that acceleration still happened
    assert game_instance.current_road_speed == initial_speed + settings.ACCELERATION_CONSTANT


def test_gameplay_keys_when_game_over(game_instance, mocker):
    # Arrange
    game_instance.game_over = True  # Game IS over
    initial_speed = game_instance.current_road_speed
    mocker.patch('pygame.event.get', return_value=[])
    # Simulate pressing UP and LEFT keys
    mocker.patch('pygame.key.get_pressed', return_value=mock_key_state((pygame.K_UP, pygame.K_LEFT)))

    # Act
    game_instance._handle_events()

    # Assert
    # Speed should not change
    assert game_instance.current_road_speed == initial_speed
    # Movement method should not be called
    game_instance.player_car.move_horizontal.assert_not_called()
    # Ensure game is still running (unless ESC was pressed, which it wasn't here)
    assert game_instance.running is True