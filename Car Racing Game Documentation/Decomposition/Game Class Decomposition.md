---

kanban-plugin: board

---

## `__init__`

- [ ] Initialise Pygame.
- [ ] Set up the game window.
- [ ] Set the window title.
- [ ] Create a Pygame clock instance.
- [ ] Initialise game state variables.
- [ ] Load constants from `settings.py`.
- [ ] Create an instance of `Road`.
- [ ] Create an instance of `PlayerCar`.
- [ ] Create an instance of `UIManager`.
- [ ] Create Pygame sprite groups.
- [ ] Add player car to sprite groups.
- [ ] Initialise score.
- [ ] Call `_load_high_score`.
- [ ] Initialise current road speed.
- [ ] Define a Pygame event for NPC spawning.
- [ ] Start a Pygame timer for NPC spawning.
- [ ] Spawn an initial set of NPC cars.


## `run`

- [ ] Start the main game loop.
- [ ] Call `_handle_events`.
- [ ] If game is not over, call `_update_game_state`.
- [ ] Call `_draw_elements`.
- [ ] Flip the display.
- [ ] Tick the clock.
- [ ] After the loop, call `pygame.quit`.


## `_handle_events`

- [ ] Loop through Pygame events.
- [ ] Check for `QUIT` event.
- [ ] If game over, check for restart key.
- [ ] If game not over:
	- [ ] Check for NPC spawn event.
	- [ ] Get pressed keys.
	- [ ] Handle UP/DOWN arrow keys for road speed.
	- [ ] Handle LEFT/RIGHT arrow keys for player horizontal movement.


## `_update_game_state`

- [ ] Call `road.update`.
- [ ] Call `player_car.update`.
- [ ] Call `npc_cars.update`.
- [ ] Call `_check_collisions`.
- [ ] Call `_update_score`.
- [ ] Manage NPC car count.


## `_draw_elements`

- [ ] Fill the screen with a background colour.
- [ ] Call `road.draw`.
- [ ] Call `all_sprites.draw`.
- [ ] Call `ui_manager.display_score`.
- [ ] Call `ui_manager.display_high_score`.
- [ ] If game over, call `ui_manager.display_game_over`.


## `_spawn_npc_car`

- [ ] If NPC count is below max:
	- [ ] Select a random NPC car image.
	- [ ] Choose a random X-position (lane).
	- [ ] Set initial Y-position above screen.
	- [ ] Assign a random speed.
	- [ ] Create a new `NPCCar` instance.
	- [ ] Add NPC to sprite groups.


## `_check_collisions`

- [ ] Use `pygame.sprite.spritecollideany` with mask collision.
- [ ] If collision:
	- [ ] Set game over state to true.
	- [ ] Call `_save_high_score`.
	- [ ] Optional: Play crash sound.


## `_update_score`

- [ ] Iterate through NPC cars.
- [ ] If NPC car passed player and not yet scored:
	- [ ] Increment score.
	- [ ] Mark NPC as scored.


## `_load_high_score`

- [ ] Try to open and read high score file.
- [ ] Store integer value in `self.high_score`.
- [ ] Handle `FileNotFoundError` or `ValueError` by setting high score to 0.


## `_save_high_score`

- [ ] If current score is greater than high score:
	- [ ] Update `self.high_score`.
	- [ ] Try to open and write new high score to file.
	- [ ] Handle `IOError`.


## `_reset_game`

- [ ] Set game over state to false.
- [ ] Reset score to 0.
- [ ] Call `_load_high_score`.
- [ ] Reset player car's X position.
- [ ] Reset current road speed.
- [ ] Empty all existing NPC cars from sprite groups.
- [ ] Spawn an initial set of NPC cars.




%% kanban:settings
```
{"kanban-plugin":"board"}
```
%%