# test_game__reset_game.py
import pytest
from unittest.mock import MagicMock, patch
import pygame  # Required for pygame.sprite.Group

from game import Game
from car import PlayerCar  # Import PlayerCar for spec if you choose that route


@pytest.fixture
def mock_dependencies(mocker):
    # Mock pygame functions and constants used in Game.__init__
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock')
    mocker.patch('pygame.time.set_timer')
    mocker.patch('pygame.USEREVENT', 1)

    # Mock game specific classes (constructors)
    player_car_spec_methods = list(pygame.sprite.Sprite.__dict__.keys()) + ['reset_position', 'move_horizontal']
    mock_player_car_instance = MagicMock(spec=player_car_spec_methods)

    mock_player_car_instance.rect = MagicMock()
    mock_player_car_instance.image = MagicMock()
    mock_player_car_instance._Sprite__g = {}
    mock_player_car_instance.reset_position = MagicMock()
    mock_player_car_instance.move_horizontal = MagicMock()

    mocker.patch('game.PlayerCar', return_value=mock_player_car_instance)

    mock_road_instance = MagicMock()
    mocker.patch('game.Road', return_value=mock_road_instance)
    mocker.patch('game.UIManager')

    settings_attrs = {
        'SCREEN_WIDTH': 840, 'SCREEN_HEIGHT': 650, 'ROAD_IMAGE_PATH': "assets/background.png",
        'PLAYER_IMAGE_PATH': "assets/player-image.png", 'PLAYER_START_X_POS': 420,
        'PLAYER_Y_POS': 400, 'HORIZONTAL_SPEED_CONSTANT': 100, 'NPC_SPAWN_INTERVAL': 1,
        'HIGH_SCORE_FILE_PATH': "highscore.txt",
    }
    mock_settings = MagicMock(**settings_attrs)
    for key, value in settings_attrs.items():
        setattr(mock_settings, key, value)
    mocker.patch('game.settings', new=mock_settings)

    return {
        "mock_player_car_instance": mock_player_car_instance,
        "mock_settings": mock_settings
    }


@pytest.fixture
def game_instance(mock_dependencies, mocker):
    mocker.patch.object(Game, '_load_high_score')
    game_obj = Game()
    game_obj._load_high_score = MagicMock()
    return game_obj


def test_reset_game_core_attributes(game_instance):
    # Arrange
    game_instance.game_over = True
    game_instance.score = 150
    dummy_npc_for_set = MagicMock()
    game_instance.passed_npcs = {dummy_npc_for_set}
    game_instance.current_road_speed = 75

    # Act
    game_instance._reset_game()

    # Assert
    assert not game_instance.game_over
    assert game_instance.score == 0
    assert not game_instance.passed_npcs
    assert game_instance.current_road_speed == 0


def test_reset_game_player_car_position_reset(game_instance):
    # Act
    game_instance._reset_game()

    # Assert
    game_instance.player_car.reset_position.assert_called_once()


def test_reset_game_reloads_high_score(game_instance):
    # Act
    game_instance._reset_game()

    # Assert
    game_instance._load_high_score.assert_called_once()


def test_reset_game_clears_npcs(game_instance, mocker):
    # Arrange
    mock_npc1 = MagicMock(spec=pygame.sprite.Sprite)
    mock_npc1._Sprite__g = {}
    mock_npc1.kill = MagicMock(
        side_effect=lambda: (game_instance.all_sprites.remove(mock_npc1), game_instance.npc_cars.remove(mock_npc1)))

    mock_npc2 = MagicMock(spec=pygame.sprite.Sprite)
    mock_npc2._Sprite__g = {}
    mock_npc2.kill = MagicMock(
        side_effect=lambda: (game_instance.all_sprites.remove(mock_npc2), game_instance.npc_cars.remove(mock_npc2)))

    game_instance.npc_cars.add(mock_npc1, mock_npc2)
    game_instance.all_sprites.add(mock_npc1, mock_npc2)

    assert len(game_instance.npc_cars) == 2
    expected_all_sprites_len = (1 if game_instance.player_car else 0) + 2
    assert len(game_instance.all_sprites) == expected_all_sprites_len

    # Act
    game_instance._reset_game()

    # Assert
    mock_npc1.kill.assert_called_once()
    mock_npc2.kill.assert_called_once()

    assert not game_instance.npc_cars
    expected_all_sprites_after_reset = 1 if game_instance.player_car else 0
    assert len(game_instance.all_sprites) == expected_all_sprites_after_reset
    if game_instance.player_car:
        assert game_instance.player_car in game_instance.all_sprites


def test_reset_game_reinitializes_road(game_instance, mocker, mock_dependencies):
    # Arrange
    reinitialized_road_mock_class = mocker.patch('game.Road')
    s = mock_dependencies["mock_settings"]

    # Act
    game_instance._reset_game()

    # Assert
    reinitialized_road_mock_class.assert_called_once_with(
        s.ROAD_IMAGE_PATH, s.SCREEN_WIDTH, s.SCREEN_HEIGHT
    )
    assert game_instance.road == reinitialized_road_mock_class.return_value


def test_reset_game_with_no_initial_npcs(game_instance, mocker, mock_dependencies):
    # Arrange
    assert not game_instance.npc_cars
    expected_all_sprites_len = 1 if game_instance.player_car else 0
    assert len(game_instance.all_sprites) == expected_all_sprites_len

    reinitialized_road_mock_class_edge = mocker.patch('game.Road')
    s = mock_dependencies["mock_settings"]
    game_instance.game_over = True
    game_instance.score = 70

    # Act
    game_instance._reset_game()

    # Assert
    assert not game_instance.game_over
    assert game_instance.score == 0
    assert not game_instance.npc_cars

    expected_all_sprites_after_reset = 1 if game_instance.player_car else 0
    assert len(game_instance.all_sprites) == expected_all_sprites_after_reset
    if game_instance.player_car:
        assert game_instance.player_car in game_instance.all_sprites

    if game_instance.player_car:
        game_instance.player_car.reset_position.assert_called_once()
    game_instance._load_high_score.assert_called_once()
    reinitialized_road_mock_class_edge.assert_called_once_with(
        s.ROAD_IMAGE_PATH, s.SCREEN_WIDTH, s.SCREEN_HEIGHT
    )
    assert game_instance.road == reinitialized_road_mock_class_edge.return_value