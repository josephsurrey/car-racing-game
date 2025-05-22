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
| 6           | Verify `Road`  is instantiated                              | `self.road` is an instance of `Road`, initialized with appropriate settings parameters                                               |
| 7           | Verify `PlayerCar`  is instantiated                         | `self.player_car` is an instance of `PlayerCar`, initialized with appropriate settings parameters                                    |
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
##### Component Testing
#### `_handle_events`

##### Component Test Plan
##### Component Testing
#### `_update_game_state`

##### Component Test Plan
##### Component Testing
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