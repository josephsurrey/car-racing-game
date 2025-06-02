---

kanban-plugin: board

---

## `__init__`

- [ ] Initialise Pygame.
- [ ] Initialise Pygame mixer.
- [ ] Set up the game window using screen dimensions from `settings`.
- [ ] Store screen width and height.
- [ ] Set the window title.
- [ ] Create a Pygame clock.
- [ ] Initialise `self.running` and `self.game_over` states.
- [ ] Create an instance of `Road`.
- [ ] Create an instance of `PlayerCar`.
- [ ] Create an instance of `UIManager`.
- [ ] Create `self.all_sprites` and `self.npc_cars` sprite groups.
- [ ] Create `self.lane_groups` list of sprite groups for lanes.
- [ ] Add player car to `self.all_sprites`.
- [ ] Initialise `self.score`.
- [ ] Initialise `self.high_score`.
- [ ] Call `_load_high_score`.
- [ ] Initialise `self.passed_npcs` set.
- [ ] Initialise `self.current_road_speed`.
- [ ] Define `self.NPC_SPAWN_EVENT` Pygame user event.
- [ ] Start a Pygame timer for `NPC_SPAWN_EVENT`.


## `run`

- [ ] Start the main game loop.
- [ ] Control game speed with `self.clock.tick`.
- [ ] Call `_handle_events`.
- [ ] If not `self.game_over`, call `_update_game_state`.
- [ ] Call `_draw_elements`.
- [ ] Update the display with `pygame.display.flip()`.
- [ ] Update window caption with FPS.
- [ ] After loop, call `pygame.quit()`.


## `_handle_events`

- [ ] Loop through Pygame events.
- [ ] If `QUIT` event, set `self.running = False`.
- [ ] If `self.game_over`:
	- [ ] If 'R' key pressed, call `_reset_game()`.
	- [ ] If 'ESC' key pressed, set `self.running = False`.
- [ ] If not `self.game_over`:
	- [ ] If `NPC_SPAWN_EVENT`, call `_spawn_npc_car()`.
- [ ] If not `self.game_over` (for player input):
	- [ ] Get pressed keys.
	- [ ] Handle UP/W for road acceleration.
	- [ ] Handle DOWN/S for road braking.
	- [ ] Clamp `self.current_road_speed`.
	- [ ] Handle LEFT/A for player left movement.
	- [ ] If moving left and key released, stop horizontal movement.
	- [ ] Handle RIGHT/D for player right movement.
	- [ ] If moving right and key released, stop horizontal movement.


## `_update_game_state`

- [ ] Call `self.road.update`.
- [ ] Call `self.player_car.update`.
- [ ] Call `self.npc_cars.update`.
- [ ] Call `_check_collisions`.
- [ ] Call `_update_score`.


## `_draw_elements`

- [ ] Fill screen with background color.
- [ ] Call `self.road.draw`.
- [ ] Call `self.all_sprites.draw`.
- [ ] Call `self.ui_manager.display_score`.
- [ ] Call `self.ui_manager.display_high_score`.
- [ ] If `self.game_over`, call `self.ui_manager.display_game_over`.


## `_spawn_npc_car`

- [ ] If NPC count is below max:
	- [ ] Loop to find a valid, clear lane for spawning.
	- [ ] Set NPC X-position based on chosen lane.
	- [ ] Set NPC initial Y-position above screen.
	- [ ] Assign a random speed to NPC.
	- [ ] Create a new `NPCCar` instance.
	- [ ] Add NPC to `self.all_sprites`, `self.npc_cars`, and its specific lane group.


## `_check_collisions`

- [ ] Use `pygame.sprite.spritecollideany` for player-NPC collision.
- [ ] If collision:
	- [ ] Set `self.game_over = True`.
	- [ ] Call `_save_high_score`.


## `_update_score`

- [ ] Iterate through NPC cars.
- [ ] If player passed an NPC not yet scored:
	- [ ] Increment `self.score`.
	- [ ] Add NPC to `self.passed_npcs`.
- [ ] If a passed NPC despawns:
	- [ ] Remove NPC from `self.passed_npcs`.


## `_load_high_score`

- [ ] Try to open and read high score file.
- [ ] Store integer value in `self.high_score`.
- [ ] Handle `FileNotFoundError` or `ValueError` by setting high score to 0.


## `_save_high_score`

- [ ] If current score is greater than high score:
	- [ ] Update `self.high_score`.
	- [ ] Try to open and write new high score to file.
	- [ ] Handle `IOError` by printing an error.


## `_reset_game`

- [ ] Set `self.game_over = False`.
- [ ] Reset `self.score`.
- [ ] Clear `self.passed_npcs`.
- [ ] Call `_load_high_score`.
- [ ] Call `self.player_car.reset_position()`.
- [ ] Reset `self.current_road_speed`.
- [ ] Call `npc.kill()` for all NPCs in `self.npc_cars`.
- [ ] Re-instantiate `self.road`.




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%