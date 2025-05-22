import pytest
import pygame
from unittest.mock import MagicMock, patch


from game import Game
from car import PlayerCar
from road import Road
from ui_manager import UIManager
import settings

@pytest.fixture
def game_instance(mocker):
    # Mock pygame functions that are called during Game.__init__
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.display.set_mode', return_value=MagicMock()) # Return a mock surface
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock', return_value=MagicMock()) # Return a mock clock
    mocker.patch('pygame.time.set_timer')

    # Mock methods of the Game class itself that are called in __init__
    mocker.patch.object(Game, '_load_high_score')

    # Create and return a Game instance
    game = Game()
    return game

# Test 1: Verify Pygame and mixer initialization
def test_pygame_and_mixer_initialization(game_instance):
    # Check pygame.init was called
    pygame.init.assert_called_once()
    # Check pygame.mixer.init was called
    pygame.mixer.init.assert_called_once()

# Test 2 & 3: Verify screen setup and clock creation
def test_screen_caption_and_clock_setup(game_instance):
    # Check screen was set with correct dimensions
    pygame.display.set_mode.assert_called_once_with(
        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    )
    # Check caption was set
    pygame.display.set_caption.assert_called_once_with("Car Racing Game")
    # Check clock was created
    pygame.time.Clock.assert_called_once()
    # Check screen and clock attributes are assigned
    assert game_instance.screen is not None
    assert game_instance.clock is not None

# Test 4 & 5: Verify initial game states
def test_initial_game_states(game_instance):
    # Check running state
    assert game_instance.running is True
    # Check game_over state
    assert game_instance.game_over is False

# Test 6: Verify Road object initialization
def test_road_object_initialization(game_instance):
    # Check road attribute is an instance of Road
    assert isinstance(game_instance.road, Road)

# Test 7: Verify PlayerCar object initialization
def test_player_car_object_initialization(game_instance):
    # Check player_car attribute is an instance of PlayerCar
    assert isinstance(game_instance.player_car, PlayerCar)

# Test 8: Verify UIManager object initialization
def test_ui_manager_object_initialization(game_instance):
    # Check ui_manager attribute is an instance of UIManager
    assert isinstance(game_instance.ui_manager, UIManager)

# Test 9: Verify sprite group initialization
def test_sprite_groups_initialization(game_instance):
    # Check all_sprites group type and content
    assert isinstance(game_instance.all_sprites, pygame.sprite.Group)
    assert game_instance.player_car in game_instance.all_sprites
    # Check npc_cars group type and initial emptiness
    assert isinstance(game_instance.npc_cars, pygame.sprite.Group)
    assert len(game_instance.npc_cars) == 0

# Test 10: Verify score initialization
def test_score_initialization(game_instance):
    # Check score is initialized to 0
    assert game_instance.score == 0

# Test 11: Verify high score initialization
def test_high_score_initialization_and_load_attempt(game_instance):
    # Check high_score is initialized to 0 before _load_high_score (mocked) would change it
    assert game_instance.high_score == 0
    # Check _load_high_score method was called
    game_instance._load_high_score.assert_called_once_with()

# Test 12: Verify current road speed initialization
def test_current_road_speed_initialization(game_instance):
    # Check current_road_speed is initialized to 0
    assert game_instance.current_road_speed == 0

# Test 13: Verify NPC spawn event setup
def test_npc_spawn_event_setup(game_instance):
    # Check NPC_SPAWN_EVENT constant value
    assert game_instance.NPC_SPAWN_EVENT == pygame.USEREVENT + 1
    # Check pygame.time.set_timer was called with correct arguments
    pygame.time.set_timer.assert_called_once_with(
        game_instance.NPC_SPAWN_EVENT,
        int(settings.NPC_SPAWN_INTERVAL * 1000)
    )