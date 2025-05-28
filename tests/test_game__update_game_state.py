import pytest
import pygame
from unittest.mock import Mock, patch

# Assuming game.py, car.py, road.py, settings.py are in paths accessible by pytest
from game import Game
from car import PlayerCar  # Imported for spec
from road import Road  # Imported for spec


# import settings # Not directly used in this test file but good for context

@pytest.fixture
def game_instance_for_update(mocker):
    # Standard Pygame init mocks (called in Game.__init__)
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock')
    mocker.patch('pygame.time.set_timer')

    # Mock Road class and ensure its instance's update method is a mock
    mock_road_instance = Mock(spec=Road)
    mock_road_instance.update = Mock(name='road_update_mock')
    mocker.patch('game.Road', return_value=mock_road_instance)  # Patch where Road is looked up by game.py

    # Mock PlayerCar class and ensure its instance's update method is a mock
    mock_player_car_instance = Mock(spec=PlayerCar)
    mock_player_car_instance.update = Mock(name='player_car_update_mock')
    mocker.patch('game.PlayerCar', return_value=mock_player_car_instance)  # Patch where PlayerCar is looked up

    # Mock UIManager (as it's instantiated in Game.__init__)
    mocker.patch('game.UIManager')

    # Mock pygame.sprite.Group for self.all_sprites and self.npc_cars
    # We need self.npc_cars.update to be a mock
    mock_all_sprites_group = Mock(spec=pygame.sprite.Group)
    mock_all_sprites_group.add = Mock(name='all_sprites_add_mock')  # Called in __init__ for player_car

    mock_npc_cars_group = Mock(spec=pygame.sprite.Group)
    mock_npc_cars_group.update = Mock(name='npc_cars_update_mock')  # This is key for the test

    # Use side_effect to provide different mocks for the two Group creations in Game.__init__
    # The first Group() call is for self.all_sprites, the second for self.npc_cars
    group_creation_order = [mock_all_sprites_group, mock_npc_cars_group]

    # Define a side_effect function for patching pygame.sprite.Group
    # It will return mocks from group_creation_order in sequence
    def group_side_effect(*args, **kwargs):
        if group_creation_order:
            return group_creation_order.pop(0)
        # Fallback if more groups are created than expected (should not happen here)
        return Mock(spec=pygame.sprite.Group)

    mocker.patch('pygame.sprite.Group', side_effect=group_side_effect)

    # Mock _load_high_score as it's called in Game.__init__
    mocker.patch('game.Game._load_high_score')

    # Now, create the actual Game instance
    # Its .road, .player_car, .all_sprites, and .npc_cars attributes will be our pre-configured mocks
    game = Game()

    # Mock the internal methods of the Game instance that _update_game_state calls
    game._check_collisions = Mock(name='_check_collisions_mock')
    game._update_score = Mock(name='_update_score_mock')

    # Set a known road speed for the test
    game.current_road_speed = 75  # Example value

    return game


def test_update_game_state_calls_all_dependencies(game_instance_for_update):
    # Arrange
    game = game_instance_for_update
    expected_road_speed = game.current_road_speed

    # Act
    game._update_game_state()

    # Assert
    # Verify Road.update was called correctly
    game.road.update.assert_called_once_with(expected_road_speed)

    # Verify PlayerCar.update was called
    game.player_car.update.assert_called_once_with()

    # Verify NPCCars group's update was called
    game.npc_cars.update.assert_called_once_with()  # Sprite groups are updated with no args usually

    # Verify internal game methods were called
    game._check_collisions.assert_called_once_with()
    game._update_score.assert_called_once_with()