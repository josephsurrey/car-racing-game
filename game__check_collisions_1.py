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
        while self.running:
            # Runs the game at the desired FPS
            self.clock.tick(settings.TARGET_FPS)

            # Handles input evets (keypresses) and game events (spawning NPC cars)
            self._handle_events()

            # If game is still running, update the game states
            if not self.game_over:
                self._update_game_state()

            # Draws game elements to the screen
            self._draw_elements()

            # Updates the display
            pygame.display.flip()
            # Sets window caption to display FPS
            # (for testing purposes, to be changed later)
            pygame.display.set_caption(
                f"Car Racing Game - FPS: {self.clock.get_fps():.2f}"
            )

        # When self.running is False, quit the game
        pygame.quit()

    def _handle_events(self):
        # Check to see if user has quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Check to see if user wants to play again/quit
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._reset_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            else:
                # Check for spawning NPC's
                if event.type == self.NPC_SPAWN_EVENT:
                    self._spawn_npc_car()

        # If game is being played
        if not self.game_over:
            # Get keypress
            keys = pygame.key.get_pressed()
            # Accelerate or brake if correct keys are pressed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.current_road_speed += settings.ACCELERATION_CONSTANT
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.current_road_speed -= settings.BRAKING_CONSTANT

            # If current speed is >= max speed, set speed to max speed
            self.current_road_speed = max(
                0, min(self.current_road_speed, settings.MAX_SPEED)
            )

            # Move horizontally if correct keys are pressed
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_car.move_horizontal(
                    -settings.HORIZONTAL_SPEED_CONSTANT
                )
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_car.move_horizontal(
                    settings.HORIZONTAL_SPEED_CONSTANT
                )

    def _update_game_state(self):
        # Call function to update the road
        self.road.update(self.current_road_speed)

        # Call function to update player and NPC cars
        self.player_car.update()
        self.npc_cars.update()

        # Check for collisions
        self._check_collisions()
        # Update score
        self._update_score()

    def _draw_elements(self):
        # Set screen colour to black
        self.screen.fill(settings.BLACK)
        # Draw the road on the screen
        self.road.draw(self.screen)
        # Draw all sprites on the screen
        self.all_sprites.draw(self.screen)

        # Display score and high score
        self.ui_manager.display_score(self.screen, self.score)
        self.ui_manager.display_high_score(self.screen, self.high_score)

        # Display game over screen
        if self.game_over:
            self.ui_manager.display_game_over(
                self.screen, self.score, self.high_score
            )

    def _spawn_npc_car(self, initial_spawn=False):
        # If there are fewer cars than the maximum on screen
        if len(self.npc_cars) < settings.MAX_NPCS:
            # Set x pos to random choice of lane positions
            npc_x_pos = random.choice(settings.LANE_POSITIONS)
            # Set y pos based on height of car
            npc_y_pos = -settings.PLACEHOLDER_NPC_HEIGHT
            # Set random speed in between defined min and max speed
            npc_speed = random.randint(
                settings.NPC_MIN_SPEED, settings.NPC_MAX_SPEED
            )

            # Create a new instance of NPCCar
            npc = NPCCar(
                settings.NPC_IMAGE_PATH, npc_x_pos, npc_y_pos, npc_speed
            )

            # Add new npc instance to sprite groups
            self.all_sprites.add(npc)
            self.npc_cars.add(npc)

    def _check_collisions(self):
        # If player collides with an NPC car
        if pygame.sprite.spritecollideany(self.player_car, self.npc_cars):
            # Set game over to true
            self.game_over = True
            # Save high score
            self._save_high_score()

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
