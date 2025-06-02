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

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        pygame.display.set_caption("Car Racing Game")
        self.clock = pygame.time.Clock()

        # Set game states
        self.running = True
        self.game_over = False
        self.show_instructions = True  # Show instructions at the start

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
            settings.HORIZONTAL_ACCELERATION_CONSTANT,
        )
        self.ui_manager = UIManager()

        # Assign sprite to Pygame groups
        self.all_sprites = pygame.sprite.Group()
        self.npc_cars = pygame.sprite.Group()

        # Create Pygame groups for each lane
        self.lane_groups = []
        for n in range(len(settings.LANE_POSITIONS)):
            self.lane_groups.append(pygame.sprite.Group())

        self.all_sprites.add(self.player_car)

        # Set score and load high score
        self.score = 0
        self.high_score = 0
        self._load_high_score()

        # Set to hold passed NPC cars
        self.passed_npcs = set()

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

            # Handles input evets (keypresses)
            # and game events (spawning NPC cars)
            self._handle_events()

            # Update game state (only if game is active)
            self._update_game_state()

            # Draw elements based on current game state
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
                return  # Exit immediately if quitting

            # Handle instruction screen dismissal
            if self.show_instructions:
                if event.type == pygame.KEYDOWN:
                    self.show_instructions = False
                continue

            # Handle game_over screen inputs
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                # Don't process other game events if game is over
                continue

            else:
                if event.type == self.NPC_SPAWN_EVENT:
                    self._spawn_npc_car()

        # Handle continuous key presses for player movement
        if not self.show_instructions and not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.current_road_speed += settings.ACCELERATION_CONSTANT
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.current_road_speed -= settings.BRAKING_CONSTANT

            self.current_road_speed = max(
                0, min(self.current_road_speed, settings.MAX_SPEED)
            )

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_car.move_horizontal(-1)
            # If the player is moving left and not pressing left arrow,
            # set horizontal speed to 0
            elif self.player_car.horizontal_speed < 0:
                self.player_car.horizontal_speed = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_car.move_horizontal(1)
            # If the player is moving right and not pressing right arrow,
            # set horizontal speed to 0
            elif self.player_car.horizontal_speed > 0:
                self.player_car.horizontal_speed = 0

    def _update_game_state(self):
        # Only update game state if game is active
        if not self.game_over and not self.show_instructions:
            self.road.update(self.current_road_speed)
            self.player_car.update(self.screen_width)
            self.npc_cars.update(self.current_road_speed, self.screen_height)
            self._check_collisions()
            self._update_score()

    def _draw_elements(self):
        # Set screen colour to black
        self.screen.fill(settings.BLACK)
        # Draw the road on the screen
        self.road.draw(self.screen)
        # Draw all sprites on the screen
        self.all_sprites.draw(self.screen)

        if self.show_instructions:
            self.ui_manager.display_instructions(self.screen)
        elif self.game_over:
            # Display score and high score typically part of game over screen
            # or can be shown underneath
            self.ui_manager.display_score(self.screen, self.score)
            self.ui_manager.display_high_score(self.screen, self.high_score)
            self.ui_manager.display_game_over(
                self.screen, self.score, self.high_score
            )
        else:  # Game is running
            self.ui_manager.display_score(self.screen, self.score)
            self.ui_manager.display_high_score(self.screen, self.high_score)

    def _spawn_npc_car(self):
        # If there are fewer cars than the maximum on screen
        if len(self.npc_cars) < settings.MAX_NPCS:
            while True:
                # Set x pos to random choice of lane positions
                lane_id = random.randint(0, (len(settings.LANE_POSITIONS) - 1))
                # Assume the lane is valid for spawning
                valid_lane = True
                # Loop through all NPC's in selected lane
                for npc in self.lane_groups[lane_id]:
                    # If NPC is too close to top of screen,
                    # flag lane as not valid and run loop again
                    if npc.rect.top < (self.screen_height // 2):
                        valid_lane = False
                        break

                # If lane hasn't been flagged as invalid, break the loop
                if valid_lane:
                    break

            # Set NPC x position based on the selected lane
            npc_x_pos = settings.LANE_POSITIONS[lane_id]

            # Set y pos based on height of car
            npc_y_pos = -settings.PLACEHOLDER_CAR_HEIGHT
            # Set random speed in between defined min and max speed
            npc_speed = random.randint(
                settings.NPC_MIN_SPEED, settings.NPC_MAX_SPEED
            )

            # Create a new instance of NPCCar
            npc = NPCCar(
                settings.NPC_IMAGE_PATH,
                npc_x_pos,
                npc_y_pos,
                npc_speed,
                lane_id,
            )

            # Add new npc instance to sprite groups
            self.all_sprites.add(npc)
            self.npc_cars.add(npc)
            self.lane_groups[lane_id].add(npc)

    def _check_collisions(self):
        # If player collides with an NPC car
        if pygame.sprite.spritecollideany(self.player_car, self.npc_cars):
            # Set game over to true
            self.game_over = True
            # Save high score
            self._save_high_score()

    def _update_score(self):
        # Iterate through all spawned NPCs
        for npc in list(self.npc_cars):
            # If player has passed npc
            if (
                npc.rect.top > self.player_car.rect.bottom
                and npc not in self.passed_npcs
            ):
                # Increase score
                self.score += 10
                # Add npc to list of passed NPCs
                self.passed_npcs.add(npc)

            # Remove despawned NPCs from passed_npc list
            if not npc.alive() and npc in self.passed_npcs:
                self.passed_npcs.remove(npc)

    def _load_high_score(self):
        try:
            # Open high score file
            with open(settings.HIGH_SCORE_FILE_PATH, "r") as high_score:
                # Read high score
                self.high_score = int(high_score.read())
        # If file not found, or error with converting file to integer
        except (FileNotFoundError, ValueError):
            # Set high score to 0
            self.high_score = 0

    def _save_high_score(self):
        # If score is greater than high score
        if self.score > self.high_score:
            # Update high score
            self.high_score = self.score
            try:
                # Open file and write high score
                with open(settings.HIGH_SCORE_FILE_PATH, "w") as high_score:
                    high_score.write(str(self.high_score))
            # If write fails, print error message
            except IOError:
                print("Error: Could not save high score to file.")

    def _reset_game(self):
        # Reset variables back to starting values
        self.game_over = False
        self.score = 0
        self.passed_npcs.clear()
        self._load_high_score()

        # Reset player position and road speed
        self.player_car.reset_position()
        self.player_car.horizontal_speed = 0
        self.current_road_speed = 0

        # Clear NPC cars
        for npc in self.npc_cars:
            npc.kill()

        # Reset road
        self.road = Road(
            settings.ROAD_IMAGE_PATH,
            settings.SCREEN_WIDTH,
            settings.SCREEN_HEIGHT,
        )

        # Show instructions for the new game
        self.show_instructions = True
