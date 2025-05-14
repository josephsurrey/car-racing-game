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
