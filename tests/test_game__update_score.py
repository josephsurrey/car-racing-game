import pytest
import pygame  # Required for pygame.Rect and pygame.sprite.Group
from game import Game  # The class we are testing
from car import PlayerCar, NPCCar  # For type hinting and mocker.patch spec
import settings  # game.py imports settings

# Pygame needs to be initialized for some components like Rect, sprite.Group
# We do this once, or ensure our mocks handle it
pygame.init()


@pytest.fixture
def game_instance(mocker):
    # Mock Pygame's core functionalities that Game.__init__ calls
    mocker.patch("pygame.init")
    mocker.patch("pygame.mixer.init")
    mocker.patch("pygame.display.set_mode")
    mocker.patch("pygame.display.set_caption")
    mocker.patch("pygame.time.Clock")
    mocker.patch("pygame.time.set_timer")

    # Mock dependencies that Game.__init__ instantiates
    # This prevents their actual constructors from running
    mocker.patch("game.Road")
    # PlayerCar needs to be a mock object we can control, especially its rect
    mock_player_car_class = mocker.patch("game.PlayerCar")
    mock_player_car_instance = mocker.Mock(spec=PlayerCar)
    mock_player_car_instance.rect = pygame.Rect(0, 0, 50, 100)  # x, y, width, height
    mock_player_car_class.return_value = mock_player_car_instance

    mocker.patch("game.UIManager")
    # NPCCar is not directly instantiated by _update_score but by _spawn_npc_car
    # However, Game.__init__ might interact with it or settings related to it
    # For _update_score, we'll add mock NPCCars to the npc_cars group

    # Mock file operations
    mocker.patch("game.Game._load_high_score")

    game = Game()
    # Reset score and passed NPCs for clean test state
    game.score = 0
    game.passed_npcs = set()
    # Set a consistent player car bottom position for calculations
    game.player_car.rect.bottom = 400
    # Ensure npc_cars is a Group, ready to accept mock NPCs
    game.npc_cars = pygame.sprite.Group()
    return game


def create_mock_npc(mocker, top_pos, is_alive=True):
    # Helper to create a mock NPC with a rect and alive status
    npc = mocker.Mock(spec=NPCCar)  # Using spec for better mock
    npc.rect = pygame.Rect(0, 0, 30, 60)  # x, y, width, height
    npc.rect.top = top_pos
    # The alive() method is crucial for the second part of _update_score
    npc.alive = mocker.Mock(return_value=is_alive)
    return npc


def test_npc_passed_first_time(game_instance, mocker):
    # Test case 1: NPC is passed by player for the first time
    # Player car bottom is at y=400
    # NPC top is at y=410 (meaning it's "below" or "further down" than player, hence passed)
    npc1 = create_mock_npc(mocker, top_pos=game_instance.player_car.rect.bottom + 10)
    game_instance.npc_cars.add(npc1)

    game_instance._update_score()

    assert game_instance.score == 10
    assert npc1 in game_instance.passed_npcs


def test_npc_already_passed(game_instance, mocker):
    # Test case 2: NPC has already been passed and is checked again
    npc1 = create_mock_npc(mocker, top_pos=game_instance.player_car.rect.bottom + 10)
    game_instance.npc_cars.add(npc1)
    game_instance.passed_npcs.add(npc1)  # Pre-add to passed_npcs
    game_instance.score = 10  # Score already reflects this pass

    game_instance._update_score()

    assert game_instance.score == 10  # Score should not change
    assert npc1 in game_instance.passed_npcs


def test_npc_not_yet_passed(game_instance, mocker):
    # Test case 3: NPC has not yet been passed by the player
    # NPC top is at y=390 (meaning it's "above" or "less far down" than player)
    npc1 = create_mock_npc(mocker, top_pos=game_instance.player_car.rect.bottom - 10)
    game_instance.npc_cars.add(npc1)

    game_instance._update_score()

    assert game_instance.score == 0
    assert npc1 not in game_instance.passed_npcs


def test_no_npc_cars(game_instance):
    # Test case 4: There are no NPC cars on screen
    # npc_cars group is empty by default in fixture for this test

    game_instance._update_score()

    assert game_instance.score == 0
    assert len(game_instance.passed_npcs) == 0


def test_passed_npc_despawns(game_instance, mocker):
    # Test case 5: A previously passed NPC despawns (is not alive)
    # NPC is passed
    npc1 = create_mock_npc(mocker, top_pos=game_instance.player_car.rect.bottom + 10, is_alive=True)
    game_instance.npc_cars.add(npc1)
    game_instance._update_score()  # NPC1 is now passed, score is 10

    assert game_instance.score == 10
    assert npc1 in game_instance.passed_npcs

    # Now npc1 despawns
    npc1.alive.return_value = False  # Simulate despawn
    game_instance._update_score()  # Call again to process despawn

    assert game_instance.score == 10  # Score should remain from the initial pass
    assert npc1 not in game_instance.passed_npcs  # Should be removed from passed_npcs


def test_unpassed_npc_despawns(game_instance, mocker):
    # Test case 6: An NPC that was never passed despawns
    # NPC is not passed
    npc1 = create_mock_npc(mocker, top_pos=game_instance.player_car.rect.bottom - 10, is_alive=True)
    game_instance.npc_cars.add(npc1)
    game_instance._update_score()  # NPC1 is not passed, score is 0

    assert game_instance.score == 0
    assert npc1 not in game_instance.passed_npcs

    # Now npc1 despawns
    npc1.alive.return_value = False  # Simulate despawn
    game_instance._update_score()  # Call again to process despawn

    assert game_instance.score == 0  # Score remains 0
    assert npc1 not in game_instance.passed_npcs  # Still not in passed_npcs