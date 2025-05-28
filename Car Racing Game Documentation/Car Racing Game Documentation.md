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
##### Component Testing
#### `_spawn_npc_car`

##### Component Test Plan
##### Component Testing
#### `_check_collisions`

##### Component Test Plan
##### Component Testing
#### `_update_score`

##### Component Test Plan
##### Component Testing
#### `_load_high_score`

##### Component Test Plan
##### Component Testing
#### `_save_high_score`

##### Component Test Plan
##### Component Testing
#### `_reset_game`

##### Component Test Plan
##### Component Testing
#### `_show_game_over_screen`

##### Component Test Plan
##### Component Testing

## `car.py`
### Car Class
##### Component Planning
![[Car Class Decomposition]]
#### `__init__`

##### Component Test Plan
##### Component Testing
#### `update`

##### Component Test Plan
##### Component Testing
#### `draw`

##### Component Test Plan
##### Component Testing

### PlayerCar Class
##### Component Planning
![[PlayerCar Class Decomposition]]
#### `__init__`

##### Component Test Plan
##### Component Testing
#### `update`

##### Component Test Plan
##### Component Testing
#### `accelerate`

##### Component Test Plan
##### Component Testing
#### `brake`

##### Component Test Plan
##### Component Testing
#### `move_horizontal`

##### Component Test Plan
##### Component Testing

### NPCCar Class
##### Component Planning
![[NPCCar Class Decomposition]]
#### `__init__`

##### Component Test Plan
##### Component Testing
#### `update`

##### Component Test Plan
##### Component Testing

## `road.py`
### Road Class
##### Component Planning
![[Road Class Decomposition]]
#### `__init__`

##### Component Test Plan
##### Component Testing
#### `update`

##### Component Test Plan
##### Component Testing
#### `draw`

##### Component Test Plan
##### Component Testing

## `ui_manager.py`
### UIManager Class
##### Component Planning
![[UIManager Class Decomposition]]
#### `__init__`

##### Component Test Plan
##### Component Testing
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