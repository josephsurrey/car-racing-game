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
##### Component Testing
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