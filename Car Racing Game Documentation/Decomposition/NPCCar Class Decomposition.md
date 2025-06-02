---
kanban-plugin: board
---
# `__init__`
- [ ] Call `super().__init__`.

# `update`
- [ ] Adjust `self.rect.y` based on `road_speed` and `self.speed`.
- [ ] If `self.rect.top` is off-screen bottom, call `self.kill()`.