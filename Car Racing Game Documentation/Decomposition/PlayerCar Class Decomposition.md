---

kanban-plugin: board

---

## `__init__`

- [ ] Call `super().__init__` with player image and position.
- [ ] Store the player's horizontal movement speed.


## `update`

- [ ] Ensure `self.rect.x` stays within screen/road boundaries.


## `move_horizontal`

- [ ] Adjust `self.rect.x` based on direction.
- [ ] Clamp `self.rect.x` to stay within boundaries.


## `reset_position`

- [ ] Reset `self.rect.x` and `self.rect.y` to starting positions




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false]}
```
%%