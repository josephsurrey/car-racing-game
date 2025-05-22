import pygame
import random
import settings
from car import PlayerCar, NPCCar
from road import Road
from ui_manager import UIManager


class Game:
    """
    Manages the main game loop/game states
    """

    def __init__(self):
        # Initialise the game and sound
        pygame.init()
        pygame.mixer.init()

        # Setup the screen, caption, and clock
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Car Racing Game")
        self.clock = pygame.time.Clock()

        # Set game states
        self.running = True
        self.game_over = False

        # Initialise Road, Car, and UI classes
        self.road = Road(
            settings.ROAD_IMAGE_PATH,
            settings.SCREEN_WIDTH,
            settings.SCREEN_HEIGHT,
        )
        self.player_car = PlayerCar(
            settings.PLAYER_IMAGE_PATH,
            settings.PLAYER_START_X_POS,
            settings.PLAYER_Y_POS,
            settings.HORIZONTAL_SPEED_CONSTANT,
        )
        self.ui_manager = UIManager()

        # Assign sprite to Pygame groups
        self.all_sprites = pygame.sprite.Group()
        self.npc_cars = pygame.sprite.Group()

        self.all_sprites.add(self.player_car)

        # Set score and load high score
        self.score = 0
        self.high_score = 0
        self._load_high_score()

        # Set road speed
        self.current_road_speed = 0

        # Define the NPC spawning event
        self.NPC_SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(
            self.NPC_SPAWN_EVENT, int(settings.NPC_SPAWN_INTERVAL * 1000)
        )

    def run(self):
        pass

    def _handle_events(self):
        pass

    def _update_game_state(self):
        pass

    def _draw_elements(self):
        pass

    def _spawn_npc_car(self):
        pass

    def _check_collisions(self):
        pass

    def _update_score(self):
        pass

    def _load_high_score(self):
        pass

    def _save_high_score(self):
        pass

    def _reset_game(self):
        pass

    def _show_game_over_screen(self):
        pass
