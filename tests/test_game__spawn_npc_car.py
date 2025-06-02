import pytest
from unittest.mock import patch, MagicMock
import pygame  # Pygame needs to be importable

# game, car, and settings modules need to be in PYTHONPATH
from game import Game
from car import NPCCar  # For spec in MagicMock
import settings

# Assign a dummy value for pygame.USEREVENT for tests if pygame is not fully initialized
# This is used in Game.__init__
if not hasattr(pygame, 'USEREVENT'):
    pygame.USEREVENT = 24  # A common default starting value for USEREVENT


@pytest.fixture
def game_instance_for_spawn_test():
    """
    Fixture for Game instance, specifically for _spawn_npc_car tests
    Mocks external dependencies of Game.__init__ and _spawn_npc_car
    """
    with patch('pygame.init'), \
            patch('pygame.mixer.init'), \
            patch('pygame.display.set_mode'), \
            patch('pygame.display.set_caption'), \
            patch('pygame.time.Clock'), \
            patch('pygame.time.set_timer'), \
            patch('game.Road'), \
            patch('game.PlayerCar') as MockPlayerCar, \
            patch('game.UIManager'), \
            patch.object(Game, '_load_high_score'):  # Mock methods that might have side effects

        # Setup the mock player car that Game.__init__ creates and adds to all_sprites
        mock_player_sprite = MagicMock(spec=pygame.sprite.Sprite)
        MockPlayerCar.return_value = mock_player_sprite

        game = Game()  # This will call the actual __init__
        # self.player_car will be mock_player_sprite
        # self.all_sprites will contain mock_player_sprite
        # self.npc_cars will be an empty Group
        return game


# Test for spawning an NPC when the count is below the maximum
@patch('game.NPCCar')  # Mock the NPCCar class where it's imported in game.py
@patch('random.choice')  # Mock random.choice used in _spawn_npc_car
@patch('random.randint')  # Mock random.randint used in _spawn_npc_car
def test_spawn_npc_car_when_below_max(mock_randint, mock_choice, MockNPCCar, game_instance_for_spawn_test):
    # Setup
    game = game_instance_for_spawn_test
    settings.MAX_NPCS = 5  # Ensure MAX_NPCS allows spawning

    # Initial state from fixture:
    # game.npc_cars is empty
    # game.all_sprites contains 1 item (the mocked player_car)
    assert len(game.npc_cars) == 0, "Initial NPC car count should be 0"
    initial_all_sprites_len = len(game.all_sprites)  # Should be 1 (player_car)
    assert initial_all_sprites_len == 1, "Initial all_sprites count should be 1 (player_car)"

    mock_created_npc_sprite = MagicMock(spec=NPCCar)  # This is what NPCCar() will return
    MockNPCCar.return_value = mock_created_npc_sprite

    # Configure random mocks to return deterministic values
    mock_choice.return_value = settings.LANE_POSITIONS[0]
    mock_randint.return_value = settings.NPC_MIN_SPEED

    # Execution
    game._spawn_npc_car()

    # Assertions
    # Check counts have increased
    assert len(game.npc_cars) == 1, "One NPC should be added to npc_cars group"
    assert len(game.all_sprites) == initial_all_sprites_len + 1, "One NPC should be added to all_sprites group"

    # Check if NPCCar was instantiated (once)
    MockNPCCar.assert_called_once()

    # Check if the created NPC instance was added to the sprite groups
    assert mock_created_npc_sprite in game.npc_cars, "Spawned NPC should be in npc_cars group"
    assert mock_created_npc_sprite in game.all_sprites, "Spawned NPC should be in all_sprites group"


# Test for attempting to spawn an NPC when the count is at maximum
@patch('game.NPCCar')  # Mock the NPCCar class
@patch('random.choice')  # Still need to mock these as they are called before the check
@patch('random.randint')
def test_spawn_npc_car_when_at_max(mock_randint, mock_choice, MockNPCCar, game_instance_for_spawn_test):
    # Setup
    game = game_instance_for_spawn_test
    settings.MAX_NPCS = 2  # Set a specific MAX_NPCS for this test

    initial_all_sprites_len = len(game.all_sprites)  # Should be 1 (player_car)

    # Manually fill npc_cars group up to MAX_NPCS
    # These manually added NPCs are *not* automatically added to all_sprites by this setup code
    # Only _spawn_npc_car would add them to all_sprites if it created them
    for _ in range(settings.MAX_NPCS):
        game.npc_cars.add(MagicMock(spec=pygame.sprite.Sprite))

    assert len(game.npc_cars) == settings.MAX_NPCS, "NPC car count should be at MAX_NPCS for this test"

    # Execution
    game._spawn_npc_car()  # Attempt to spawn another NPC

    # Assertions
    # Counts should not have changed from the setup state
    assert len(game.npc_cars) == settings.MAX_NPCS, "npc_cars count should remain at MAX_NPCS"
    assert len(
        game.all_sprites) == initial_all_sprites_len, "all_sprites count should not change as no new NPC was spawned"

    # NPCCar constructor should not have been called
    MockNPCCar.assert_not_called()


# Test for verifying the properties of a spawned NPC
@patch('game.NPCCar')  # Mock the NPCCar class
@patch('random.choice')  # Mock random.choice
@patch('random.randint')  # Mock random.randint
def test_spawn_npc_car_initializes_with_correct_parameters(mock_randint, mock_choice, MockNPCCar,
                                                           game_instance_for_spawn_test):
    # Setup
    game = game_instance_for_spawn_test
    settings.MAX_NPCS = 5  # Ensure spawning is allowed

    # Define expected properties for the new NPC
    expected_x_pos = settings.LANE_POSITIONS[2]  # Choose a specific lane for predictability
    expected_y_pos = -settings.PLACEHOLDER_CAR_HEIGHT
    expected_speed = settings.NPC_MIN_SPEED + 10  # A speed within the defined range
    expected_image_path = settings.NPC_IMAGE_PATH

    # Configure mocks to return these specific, expected values
    mock_choice.return_value = expected_x_pos
    mock_randint.return_value = expected_speed

    mock_created_npc_sprite = MagicMock(spec=NPCCar)  # Mock the instance returned by NPCCar()
    MockNPCCar.return_value = mock_created_npc_sprite

    initial_npc_cars_len = len(game.npc_cars)  # Should be 0
    initial_all_sprites_len = len(game.all_sprites)  # Should be 1 (player_car)

    # Execution
    game._spawn_npc_car()

    # Assertions
    # Check NPCCar was called once with the correct arguments
    MockNPCCar.assert_called_once_with(
        expected_image_path,
        expected_x_pos,
        expected_y_pos,
        expected_speed
    )

    # Check group additions as a side-effect confirmation
    assert len(game.npc_cars) == initial_npc_cars_len + 1, "NPC cars count should increment"
    assert len(game.all_sprites) == initial_all_sprites_len + 1, "All sprites count should increment"
    assert mock_created_npc_sprite in game.npc_cars, "The created NPC should be in the npc_cars group"
    assert mock_created_npc_sprite in game.all_sprites, "The created NPC should be in the all_sprites group"