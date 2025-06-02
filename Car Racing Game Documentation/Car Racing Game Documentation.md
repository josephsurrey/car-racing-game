# Project Structure
```
|
|-- main.py
|
|-- game.py
|   |-- class Game:
|       |-- __init__
|       |-- run
|       |-- _handle_events
|       |-- _update_game_state
|       |-- _draw_elements
|       |-- _spawn_npc_car
|       |-- _check_collisions
|       |-- _update_score
|       |-- _load_high_score
|       |-- _save_high_score
|       |-- _reset_game
|       |-- _show_game_over_screen
|
|-- car.py
|   |-- class Car:
|   |   |-- __init__
|   |   |-- update
|   |   |-- draw
|   |
|   |-- class PlayerCar:
|   |   |-- __init__
|   |   |-- update
|   |   |-- accelerate
|   |   |-- brake
|   |   |-- move_horizontal
|   |
|   |-- class NPCCar:
|   |   |-- __init__
|   |   |-- update
|
|-- road.py
|   |-- class Road:
|   |   |-- __init__
|   |   |-- update
|   |   |-- draw
|
|-- ui_manager.py
|   |-- class UIManager:
|   |   |-- __init__
|   |   |-- display_score
|   |   |-- display_high_score
|   |   |-- display_game_over
|   |   |-- display_message
|
|-- settings.py
|
|-- assets/
```
# Component Development
## `main.py`
##### Component Planning
![[main.py Decomposition]]

##### Component Test Plan
##### Component Testing

## `game.py`
### Game Class
##### Component Planning
![[Game Class Decomposition]]
#### `__init__`

##### Component Test Plan
| Test Number | Test Description                                            | Expected Outcome                                                                                                                     |
| ----------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1           | Verify Pygame and mixer are initialized                     | `pygame.init()` and `pygame.mixer.init()` are called                                                                                 |
| 2           | Verify screen is set up with correct dimensions and caption | Screen is created with `settings.SCREEN_WIDTH`x`settings.SCREEN_HEIGHT`, caption is "Car Racing Game"                                |
| 3           | Verify game clock is created                                | `pygame.time.Clock()` is called and `self.clock` is assigned                                                                         |
| 4           | Verify initial game running state                           | `self.running` is True                                                                                                               |
| 5           | Verify initial game over state                              | `self.game_over` is False                                                                                                            |
| 6           | Verify `Road`  is instantiated                              | `self.road` is an instance of `Road`, initialized with correct settings                                                              |
| 7           | Verify `PlayerCar`  is instantiated                         | `self.player_car` is an instance of `PlayerCar`, initialized with correct settings                                                   |
| 8           | Verify `UIManager`  is instantiated                         | `self.ui_manager` is an instance of `UIManager`                                                                                      |
| 9           | Verify sprite groups are initialized                        | `self.all_sprites` contains `self.player_car`, `self.npc_cars` is an empty `pygame.sprite.Group`                                     |
| 10          | Verify score is set to zero                                 | `self.score` is 0                                                                                                                    |
| 11          | Verify high score is initialized and load attempt           | `self.high_score` is initially 0, `self._load_high_score()` method is called                                                         |
| 12          | Verify road speed is initialized                            | `self.current_road_speed` is 0                                                                                                       |
| 13          | Verify NPC spawn event is set up                            | `self.NPC_SPAWN_EVENT` is `pygame.USEREVENT + 1`, `pygame.time.set_timer` is called with the event and `settings.NPC_SPAWN_INTERVAL` |
##### Component Testing
![[game___init___test_results.png]]
```
============================= test session starts =============================
collecting ... collected 11 items

test_game___init__.py::test_pygame_and_mixer_initialization PASSED       [  9%]
test_game___init__.py::test_screen_caption_and_clock_setup PASSED        [ 18%]
test_game___init__.py::test_initial_game_states PASSED                   [ 27%]
test_game___init__.py::test_road_object_initialization PASSED            [ 36%]
test_game___init__.py::test_player_car_object_initialization PASSED      [ 45%]
test_game___init__.py::test_ui_manager_object_initialization PASSED      [ 54%]
test_game___init__.py::test_sprite_groups_initialization PASSED          [ 63%]
test_game___init__.py::test_score_initialization PASSED                  [ 72%]
test_game___init__.py::test_high_score_initialization_and_load_attempt PASSED [ 81%]
test_game___init__.py::test_current_road_speed_initialization PASSED     [ 90%]
test_game___init__.py::test_npc_spawn_event_setup PASSED                 [100%]

============================= 11 passed in 0.16s ==============================
```
#### `run`

##### Component Test Plan
| Test Number | Test Description                                                           | Expected Outcome                                                                                                                                                                |
| ----------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Game loop calls correct functions and terminates when `running` is `false` | `clock.tick`, `_handle_events`, `_update_game_state` (if not game over), `_draw_elements`, `display.flip`, `display.set_caption` called once each. `pygame.quit` called on exit |
| 2           | `_update_game_state` is not run when `game_over` is true                   | `_handle_events`, `_draw_elements` called. `_update_game_state` is not called. Loop continues if `running` is true until `running` becomes false                                |
| 3           | Game loop runs for multiple iterations correctly                           | Core methods (`clock.tick`, `_handle_events`, etc) are called for each iteration. `pygame.quit` called once upon final exit                                                     |
| 4           | FPS is displayed in window caption during loop                             | `pygame.display.set_caption()` is called in each loop iteration with a string including the current FPS value from `clock.get_fps()`                                            |
##### Component Testing
![[game_run_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 4 items

test_game_run.py::test_run_loop_single_iteration_and_termination PASSED  [ 25%]
test_game_run.py::test_run_skips_update_game_state_when_game_over PASSED [ 50%]
test_game_run.py::test_run_loop_multiple_iterations PASSED               [ 75%]
test_game_run.py::test_run_updates_caption_with_fps PASSED               [100%]

============================== 4 passed in 1.45s ==============================
```
#### `_handle_events`

##### Component Test Plan
| Test Number | Test Description                                 | Expected Outcome                                                  |
| ----------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| 1           | QUIT event occurs                                | `self.running` is set to `False`                                  |
| 2           | 'R' key pressed while game is over               | `_reset_game()` method is called                                  |
| 3           | 'ESC' key pressed (event) while game is over     | `self.running` is set to `False`                                  |
| 4           | `NPC_SPAWN_EVENT` occurs, game not over          | `_spawn_npc_car()` method is called                               |
| 5           | UP arrow key held, game not over                 | `current_road_speed` increases, limited by `MAX_SPEED`            |
| 6           | 'W' key held, game not over                      | `current_road_speed` increases, limited by `MAX_SPEED`            |
| 7           | DOWN arrow key held, game not over               | `current_road_speed` decreases, limited at 0                      |
| 8           | 'S' key held, game not over                      | `current_road_speed` decreases, limited at 0                      |
| 9           | LEFT arrow key held, game not over               | `player_car.move_horizontal()` called for left movement           |
| 10          | 'A' key held, game not over                      | `player_car.move_horizontal()` called for left movement           |
| 11          | RIGHT arrow key held, game not over              | `player_car.move_horizontal()` called for right movement          |
| 12          | 'D' key held, game not over                      | `player_car.move_horizontal()` called for right movement          |
| 13          | Accelerate (UP key) when speed is at `MAX_SPEED` | `current_road_speed` remains `MAX_SPEED`                          |
| 14          | Brake (DOWN key) when speed is 0                 | `current_road_speed` remains 0                                    |
| 15          | No relevant events or key presses                | Game state (running, speed) unchanged, no relevant methods called |
| 16          | 'R' key when game not over                       | `_reset_game()` is not called                                     |
| 17          | Gameplay keys held when game is over             | `current_road_speed` does not change, movement methods not called |
##### Component Testing
![[game__handle_events_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 17 items

test_game__handle_events.py::test_handle_event_quit PASSED               [  5%]
test_game__handle_events.py::test_handle_event_reset_game_when_over PASSED [ 11%]
test_game__handle_events.py::test_handle_event_quit_via_escape_when_over PASSED [ 17%]
test_game__handle_events.py::test_handle_event_npc_spawn_when_not_over PASSED [ 23%]
test_game__handle_events.py::test_handle_keys_accelerate[1073741906] PASSED [ 29%]
test_game__handle_events.py::test_handle_keys_accelerate[119] PASSED     [ 35%]
test_game__handle_events.py::test_handle_keys_brake[1073741905] PASSED   [ 41%]
test_game__handle_events.py::test_handle_keys_brake[115] PASSED          [ 47%]
test_game__handle_events.py::test_handle_keys_move_left[1073741904--100] PASSED [ 52%]
test_game__handle_events.py::test_handle_keys_move_left[97--100] PASSED  [ 58%]
test_game__handle_events.py::test_handle_keys_move_right[1073741903-100] PASSED [ 64%]
test_game__handle_events.py::test_handle_keys_move_right[100-100] PASSED [ 70%]
test_game__handle_events.py::test_accelerate_at_max_speed PASSED         [ 76%]
test_game__handle_events.py::test_brake_at_zero_speed PASSED             [ 82%]
test_game__handle_events.py::test_no_relevant_events_or_keys PASSED      [ 88%]
test_game__handle_events.py::test_game_over_key_r_when_not_game_over PASSED [ 94%]
test_game__handle_events.py::test_gameplay_keys_when_game_over PASSED    [100%]

============================= 17 passed in 0.36s ==============================
```
#### `_update_game_state`

##### Component Test Plan
| Test Number | Test Description                                  | Expected Outcome                                                                                                                                                                 |
| ----------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Call `_update_game_state` during normal gameplay. | `road.update` is called with `current_road_speed`. `player_car.update` is called. `npc_cars.update` (group) is called. `_check_collisions` is called. `_update_score` is called. |

##### Component Testing
![[game__update_game_state_test-results.png]]
```
============================= test session starts =============================
collecting ... collected 1 item

test_game__update_game_state.py::test_update_game_state_calls_all_dependencies PASSED [100%]

============================== 1 passed in 0.23s ==============================
```
#### `_draw_elements`

##### Component Test Plan
| Test Number | Test Description                    | Expected Outcome                                                                                                                                                                                                                                   |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Draw elements when game is not over | Screen is filled with `settings.BLACK`, `road.draw` is called, `all_sprites.draw` is called, `ui_manager.display_score` and `ui_manager.display_high_score` are called. `ui_manager.display_game_over` is NOT called                               |
| 2           | Draw elements when game is over     | Screen is filled with `settings.BLACK`, `road.draw` is called, `all_sprites.draw` is called, `ui_manager.display_score` and `ui_manager.display_high_score` are called. `ui_manager.display_game_over` IS called with current score and high score |
##### Component Testing
![[game__draw_elements.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_game__draw_elements.py::test_draw_elements_when_game_not_over pygame 2.6.1 (SDL 2.28.4, Python 3.13.2)
Hello from the pygame community. https://www.pygame.org/contribute.html
PASSED [ 50%]
test_game__draw_elements.py::test_draw_elements_when_game_is_over PASSED [100%]

============================== 2 passed in 0.26s ==============================
```
#### `_spawn_npc_car`

##### Component Test Plan
| Test Number | Test Description                                             | Expected Outcome                                                                                                                                                                                             |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1           | Spawn NPC when current NPC count is below `MAX_NPCS`         | A new `NPCCar` is created. The NPC is added to `self.npc_cars` and `self.all_sprites` groups. NPC counts in these groups increase by 1                                                                       |
| 2           | Attempt to spawn NPC when current NPC count is at `MAX_NPCS` | No new `NPCCar` is created. `self.npc_cars` and `self.all_sprites` groups remain the same                                                                                                                    |
| 3           | Verify spawned NPC is initialized with correct parameters    | `NPCCar` is instantiated with image path from `settings`, x-position from `settings.LANE_POSITIONS`, y-position as `-settings.PLACEHOLDER_NPC_HEIGHT`, and speed within `settings.NPC_MIN_SPEED`/`MAX_SPEED` |
##### Component Testing
![[game__spawn_npc_car_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 3 items

test_game__spawn_npc_car.py::test_spawn_npc_car_when_below_max PASSED    [ 33%]
test_game__spawn_npc_car.py::test_spawn_npc_car_when_at_max PASSED       [ 66%]
test_game__spawn_npc_car.py::test_spawn_npc_car_initializes_with_correct_parameters PASSED [100%]

============================== 3 passed in 0.32s ==============================
```
#### `_check_collisions`

##### Component Test Plan
| Test Number | Test Description                             | Expected Outcome                                                          |
| ----------- | -------------------------------------------- | ------------------------------------------------------------------------- |
| 1           | Player car does not collide with any NPC car | `self.game_over` remains `False`, `_save_high_score` method is not called |
| 2           | Player car collides with an NPC car          | `self.game_over` becomes `True`, `_save_high_score` method is called      |
##### Component Testing
![[game__check_collisions_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_game__check_collisions.py::TestGameCheckCollisions::test_no_collision_detected PASSED [ 50%]
test_game__check_collisions.py::TestGameCheckCollisions::test_collision_detected PASSED [100%]

============================== 2 passed in 0.06s ==============================
```
#### `_update_score`

##### Component Test Plan

| Test Number | Test Description                                  | Expected Outcome                                                                  |
|-------------|---------------------------------------------------|-----------------------------------------------------------------------------------|
| 1           | NPC is passed by player for the first time        | Score increases by 10, NPC is added to the set of passed NPCs                     |
| 2           | NPC has already been passed and is checked again  | Score does not change, NPC remains in the set of passed NPCs                      |
| 3           | NPC has not yet been passed by the player         | Score does not change, NPC is not added to the set of passed NPCs                 |
| 4           | There are no NPC cars on screen                   | Score does not change, set of passed NPCs remains empty                           |
| 5           | A previously passed NPC despawns (is not alive)   | NPC is removed from the set of passed NPCs, score remains unchanged from this event |
| 6           | An NPC that was never passed despawns             | Score does not change, set of passed NPCs remains unchanged                       |
##### Component Testing
![[game_update_score_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 6 items

test_game__update_score.py::test_npc_passed_first_time PASSED            [ 16%]
test_game__update_score.py::test_npc_already_passed PASSED               [ 33%]
test_game__update_score.py::test_npc_not_yet_passed PASSED               [ 50%]
test_game__update_score.py::test_no_npc_cars PASSED                      [ 66%]
test_game__update_score.py::test_passed_npc_despawns PASSED              [ 83%]
test_game__update_score.py::test_unpassed_npc_despawns PASSED            [100%]

============================== 6 passed in 0.32s ==============================
```
#### `_load_high_score`

##### Component Test Plan

| Test Number | Test Description                                                   | Expected Outcome                                 |
| ----------- | ------------------------------------------------------------------ | ------------------------------------------------ |
| 1           | Load high score from an existing file with a valid integer         | `self.high_score` is set to the positive integer |
| 2           | Attempt to load high score when the high score file does not exist | `self.high_score` is set to 0                    |
| 3           | Attempt to load high score from a file with non-integer content    | `self.high_score` is set to 0                    |
| 4           | Attempt to load high score from an empty file                      | `self.high_score` is set to 0                    |
| 5           | Load high score from an existing file with a negative integer      | `self.high_score` is set to the negative integer |
| 6           | Load high score from an existing file with zero as content         | `self.high_score` is set to 0                    |
##### Component Testing
![[game__load_high_score_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 6 items

test_game__load_high_score.py::test_load_high_score_file_exists_valid_content PASSED [ 16%]
test_game__load_high_score.py::test_load_high_score_file_not_found PASSED [ 33%]
test_game__load_high_score.py::test_load_high_score_invalid_content PASSED [ 50%]
test_game__load_high_score.py::test_load_high_score_empty_file PASSED    [ 66%]
test_game__load_high_score.py::test_load_high_score_negative_integer_content PASSED [ 83%]
test_game__load_high_score.py::test_load_high_score_zero_content PASSED  [100%]

============================== 6 passed in 0.61s ==============================
```
#### `_save_high_score`
##### Component Test Plan
| Test Number | Test Description                                          | Expected Outcome                                                                                     |
|-------------|-----------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| 1           | Current score is greater than the existing high score     | `self.high_score` is updated to the current score, and this new score is written to the high score file |
| 2           | Current score is not greater than the existing high score | `self.high_score` remains unchanged, and no attempt is made to write to the high score file         |
| 3           | File write fails with an `IOError` during a new high score| `self.high_score` is updated in memory, an error message is printed, and the program handles the error |

##### Component Testing
![[game__save_high_score_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 3 items

test_game__save_high_score_1.py::test_save_new_high_score_successful PASSED [ 33%]
test_game__save_high_score_1.py::test_save_score_not_higher_than_high_score PASSED [ 66%]
test_game__save_high_score_1.py::test_save_new_high_score_io_error_on_write PASSED [100%]

============================== 3 passed in 0.08s ==============================
```
#### `_reset_game`

##### Component Test Plan
| Test Number | Test Description                            | Expected Outcome                                                                            |
| ----------- | ------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1           | Verify game state variables are reset       | `game_over` is `False`, `score` is `0`, `passed_npcs` is empty, `current_road_speed` is `0` |
| 2           | Verify player car position is reset         | `player_car.reset_position()` method is called                                              |
| 3           | Verify high score is reloaded               | `_load_high_score()` method is called                                                       |
| 4           | Verify all NPC cars are cleared             | All `NPCCar` instances are removed from sprite groups, and their `kill()` method is called  |
| 5           | Verify the `Road` object is re-instantiated | A new `Road` object is created using current `settings` values and assigned to `self.road`  |
| 6           | Reset game when no NPC cars are present     | Game resets correctly and `npc_cars` group remains empty                                    |
##### Component Testing
![[game__reset_game_test_results.png]]
```============================= test session starts =============================
collecting ... collected 6 items

test_game__reset_game.py::test_reset_game_core_attributes PASSED         [ 16%]
test_game__reset_game.py::test_reset_game_player_car_position_reset PASSED [ 33%]
test_game__reset_game.py::test_reset_game_reloads_high_score PASSED      [ 50%]
test_game__reset_game.py::test_reset_game_clears_npcs PASSED             [ 66%]
test_game__reset_game.py::test_reset_game_reinitializes_road PASSED      [ 83%]
test_game__reset_game.py::test_reset_game_with_no_initial_npcs PASSED    [100%]

============================== 6 passed in 0.12s ==============================
```

## `car.py`
### Car Class
##### Component Planning
![[Car Class Decomposition]]
#### `__init__`

##### Component Test Plan
| Test Number | Test Description                                              | Expected Outcome                                                                                                                                      |
| ----------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Initialize Car with a valid image path, position, and mask    | `self.image` loads from `car_image`, `self.rect.center` matches `(x_pos, y_pos)`, and `self.mask` is created from `self.image`                        |
| 2           | Initialize Car with invalid image path when `is_npc` is true  | A blue placeholder surface is created for `self.image`, `self.rect.center` matches `(x_pos, y_pos)`, and `self.mask` is created from this placeholder |
| 3           | Initialize Car with invalid image path when `is_npc` is false | A red placeholder surface is created for `self.image`, `self.rect.center` matches `(x_pos, y_pos)`, and `self.mask` is created from this placeholder  |
##### Component Testing
![[car___init___test_results.png]]
```
============================= test session starts =============================
collecting ... collected 3 items

test_car___init__.py::test_car_init_valid_image_load PASSED              [ 33%]
test_car___init__.py::test_car_init_invalid_image_is_npc_true PASSED     [ 66%]
test_car___init__.py::test_car_init_invalid_image_is_npc_false PASSED    [100%]

============================== 3 passed in 0.43s ==============================
```
#### `update`

>[!note]
>No testing required as function is just placeholder
#### `draw`
##### Component Test Plan
| Test Number | Test Description                                  | Expected Outcome                                                                |
| :---------- | :------------------------------------------------ | :------------------------------------------------------------------------------ |
| 1           | Draw car with successfully loaded image           | `screen.blit` is called with the car's loaded `self.image` and `self.rect`      |
| 2           | Draw car with placeholder image (image load fail) | `screen.blit` is called with the car's placeholder `self.image` and `self.rect` |
##### Component Testing
![[car_draw_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_car_draw.py::TestCarDraw::test_draw_blits_loaded_image_to_screen PASSED [ 50%]
test_car_draw.py::TestCarDraw::test_draw_blits_placeholder_image_to_screen PASSED [100%]


============================== 2 passed in 0.13s ==============================
```
### PlayerCar Class
##### Component Planning
![[PlayerCar Class Decomposition]]
#### `__init__`

##### Component Test Plan
| Test Number | Test Description                                  | Expected Outcome                                                                                                                                                                                               |
| ----------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Initialize `PlayerCar` with valid image path      | `Car.__init__` is called with `is_npc=False`, image loads, rect and mask are created; `initial_x_pos`, `initial_y_pos`, `horizontal_speed_constant` are correctly assigned                                     |
| 2           | Initialize `PlayerCar` with an invalid image path | `Car.__init__` is called with `is_npc=False`, a red placeholder surface is used for the image, rect and mask are created; `initial_x_pos`, `initial_y_pos`, `horizontal_speed_constant` are correctly assigned |
##### Component Testing
![[playercar___init___test_results.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_playercar___init__.py::test_player_car_init_valid_image PASSED      [ 50%]
test_playercar___init__.py::test_player_car_init_invalid_image PASSED    [100%]

============================== 2 passed in 0.13s ==============================
```
#### `update`
##### Component Test Plan
| Test Number | Test Description                                                                    | Expected Outcome                                                                  |
| ----------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1           | Car is well within screen boundaries                                                | Car's `rect.left` and `rect.right` remain unchanged                               |
| 2           | Car's left edge is off-screen to the left (negative `rect.left`)                    | Car's `rect.left` is set to 0                                                     |
| 3           | Car's right edge is off-screen to the right (`rect.right` > `SCREEN_WIDTH`)         | Car's `rect.right` is adjusted to `settings.SCREEN_WIDTH`                         |
| 4           | Car's left edge is exactly at the screen boundary (`rect.left` == 0)                | Car's `rect.left` remains 0, `rect.right` remains unchanged                       |
| 5           | Car's right edge is exactly at the screen boundary (`rect.right` == `SCREEN_WIDTH`) | Car's `rect.right` remains `settings.SCREEN_WIDTH`, `rect.left` remains unchanged |
##### Component Testing
![[playercar_update_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 5 items

test_playercar_update.py::test_car_within_boundaries 
PASSED              [ 20%]
test_playercar_update.py::test_car_off_left_edge 
PASSED                  [ 40%]
test_playercar_update.py::test_car_off_right_edge 
PASSED                 [ 60%]
test_playercar_update.py::test_car_exactly_on_left_edge 
PASSED           [ 80%]
test_playercar_update.py::test_car_exactly_on_right_edge 
PASSED          [100%]

============================== 5 passed in 0.25s ==============================
```
#### `move_horizontal`

##### Component Test Plan
| Test Number | Test Description                    | Expected Outcome                                                           |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------- |
| 1           | Test moving the player car left     | The car's `rect.x` coordinate decreases by its `horizontal_speed_constant` |
| 2           | Test moving the player car right    | The car's `rect.x` coordinate increases by its `horizontal_speed_constant` |
| 3           | Test player car with zero direction | The car's `rect.x` coordinate remains unchanged                            |
##### Component Testing
![[playercar_move_horizontal_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 3 items

test_playercar_move_horizontal.py::test_move_horizontal_left 
PASSED      [ 33%]
test_playercar_move_horizontal.py::test_move_horizontal_right 
PASSED     [ 66%]
test_playercar_move_horizontal.py::test_move_horizontal_no_movement 
PASSED [100%]

============================== 3 passed in 0.18s ==============================
```
#### `reset_position`
##### Component Test Plan
| Test Number | Test Description                                    | Expected Outcome                                                                  |
| :---------- | :-------------------------------------------------- | :-------------------------------------------------------------------------------- |
| 1           | Reset car to initial position after being moved     | `rect.centerx` and `rect.centery` match `initial_x_pos` and `initial_y_pos`       |
| 2           | Reset car when already at its initial position      | `rect.centerx` and `rect.centery` remain at `initial_x_pos` and `initial_y_pos` |
##### Component Testing
![[playercar_reset_position_test_results.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_playercar_reset_position.py::test_reset_position_after_move 
PASSED  [ 50%]
test_playercar_reset_position.py::test_reset_position_when_at_initial 
PASSED [100%]

============================== 2 passed in 0.34s ==============================
```
### NPCCar Class
##### Component Planning
![[NPCCar Class Decomposition]]
#### `__init__`

##### Component Test Plan

| Test Number | Test Description                                               | Expected Outcome                                                                                                                                                                   |
| ----------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Initialize `NPCCar` with a valid image, position, and speed    | `Car.__init__` called with `is_npc=True`, image loads, `rect` and `speed` are correctly set, and `mask` is created from the image                                                  |
| 2           | Initialize `NPCCar` with an invalid image, position, and speed | `Car.__init__` called with `is_npc=True`, a blue placeholder surface is used for the image, `rect` and `speed` are correctly set, and `mask` is created from the placeholder image |
##### Component Testing
![[npccar__init___test_results.png]]
```
============================= test session starts =============================
collecting ... collected 2 items

test_npccar___init__.py::test_npccar_init_valid_image PASSED             [ 50%]
test_npccar___init__.py::test_npccar_init_invalid_image_uses_blue_placeholder PASSED [100%]


============================== 2 passed in 0.34s ==============================
```
#### `update`

##### Component Test Plan

| Test Number | Test Description                                                   | Expected Outcome                                                                                |
| ----------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| 1           | NPC moves down when road speed is greater than NPC speed           | NPC's `rect.y` increases, `self.kill()` is not called, NPC remains alive                        |
| 2           | NPC moves up when NPC speed is greater than road speed             | NPC's `rect.y` decreases, `self.kill()` is not called, NPC remains alive                        |
| 3           | NPC remains stationary vertically when road speed equals NPC speed | NPC's `rect.y` is unchanged, `self.kill()` is not called, NPC remains alive                     |
| 4           | NPC is killed when its top moves off the bottom of the screen      | NPC's `rect.y` increases, `self.kill()` is called, NPC is marked not alive                      |
| 5           | NPC is not killed when its top reaches exactly the screen bottom   | NPC's `rect.y` increases, `self.kill()` is not called, NPC remains alive                        |
| 6           | NPC starting off-screen is killed after moving further off-screen  | NPC's `rect.y` increases (further off-screen), `self.kill()` is called, NPC is marked not alive |
##### Component Testing
![[npccar_update_test_results.png]]


## `road.py`
### Road Class
##### Component Planning
![[Road Class Decomposition]]
#### `__init__`

##### Component Test Plan
| Test Number | Test Description                                  | Expected Outcome                                                                                                                              |
| ----------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Verify road image loads and scales correctly      | `self.image` is a scaled Surface, `self.rect1.topleft` is `(0,0)`, `self.rect2.topleft` is `(0, -self.image_height)`, no placeholder created  |
| 2           | Verify placeholder created on `FileNotFoundError` | Warning printed, `self.image_original` is a black Surface matching screen dimensions, `self.image` attribute is not set                       |
| 3           | Verify placeholder created on `pygame.error`      | Warning printed, `self.image_original` is a black Surface matching screen dimensions, `self.image` attribute is not set                       |
| 4           | Verify scaling handles aspect ratio correctly     | `self.image` is scaled to screen width, its height calculated via aspect ratio, `rect1` and `rect2` are positioned correctly, no errors occur |
##### Component Testing
![[road____init___test_results.png]]
#### `update`

##### Component Test Plan
| Test Number | Test Description                                      | Expected Outcome                                                                   |
| ----------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 1           | Road segments move down correctly                     | `rect1.y` and `rect2.y` increase by the given speed                                |
| 2           | `rect1` scrolls correctly past image height           | `rect1.y` becomes `rect2.y - image_height` after `rect1.top` passes `image_height` |
| 3           | `rect2` scrolls correctly past image height           | `rect2.y` becomes `rect1.y - image_height` after `rect2.top` passes `image_height` |
| 4           | Road doesn't move with `speed = 0`                    | `rect1.y` and `rect2.y` do not change                                              |
| 5           | Road segments move up correctly with a negative speed | `rect1.y` and `rect2.y` decrease by the value of the speed                         |
##### Component Testing
![[road_update_test_results.png]]
#### `draw`

##### Component Test Plan

| Test Number | Test Description                                 | Expected Outcome                                                                               |
| ----------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| 1           | Call draw method with a mock screen              | The `screen.blit` method is called twice                                                       |
| 2           | Check arguments of the first `screen.blit` call  | `screen.blit` is called with the road image (`self.image`) and first rectangle (`self.rect1`)  |
| 3           | Check arguments of the second `screen.blit` call | `screen.blit` is called with the road image (`self.image`) and second rectangle (`self.rect2`) |
##### Component Testing
![[road_draw_test_results.png]]

## `ui_manager.py`
### UIManager Class
##### Component Planning
![[UIManager Class Decomposition]]
#### `__init__`

##### Component Test Plan
| Test Number | Test Description                                | Expected Outcome                                                                                                                                                        |
| ----------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Initialize with default font and settings       | System font 'arial' used for all fonts (`default_font`, `medium_font`, `large_font`), default `font_size` (36), `text_color` is `settings.WHITE`, screen dimensions set |
| 2           | Initialize with a valid custom font             | Specified custom `font_name` used for all fonts, default `font_size` (36), `text_color` is `settings.WHITE`, screen dimensions set                                      |
| 3           | Initialize with an invalid font name            | Fallback to system 'arial' for all fonts, warning printed, default `font_size` (36), `text_color` is `settings.WHITE`, screen dimensions set                            |
| 4           | Initialize with custom font size and text color | System font 'arial' used for all fonts (`default_font` with custom `font_size`), custom `text_color` applied, screen dimensions set                                     |
##### Component Testing
![[uimanager___init___test_results.png]]
#### `display_score`

##### Component Test Plan
##### Component Testing
#### `display_high_score`

##### Component Test Plan
##### Component Testing
#### `display_game_over`

##### Component Test Plan
##### Component Testing
#### `display_message`

##### Component Test Plan
##### Component Testing

## `settings.py`
##### Component Planning
![[settings.py Decomposition]]
##### Component Test Plan
##### Component Testing