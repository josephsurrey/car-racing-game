---

kanban-plugin: board

---

## `__init__`

- [ ] Call `super().__init__`.
- [ ] Store initial X-position.
- [ ] Store initial Y-position.
- [ ] Store `horizontal_acceleration_constant`.
- [ ] Initialize `self.horizontal_speed`.

## `update`

- [ ] Keep car within horizontal screen boundaries.

## `move_horizontal`

- [ ] Update `self.horizontal_speed` based on `direction` and acceleration.
- [ ] Clamp `self.horizontal_speed` to max horizontal speed.
- [ ] Adjust `self.rect.centerx` by `self.horizontal_speed`.

## `reset_position`

- [ ] Reset `self.rect.centerx` to initial X-position.
- [ ] Reset `self.rect.centery` to initial Y-position.
