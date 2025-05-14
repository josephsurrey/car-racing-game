---
kanban-plugin: board
---

# `__init__`
- [ ] Load the road image.
- [ ] Convert the loaded image.
- [ ] Store the loaded road image.
- [ ] Get the height of the road image.
- [ ] Store screen height.
- [ ] Create two `pygame.Rect` objects for the road image.
- [ ] Position first rect at top-left.
- [ ] Position second rect directly above first.

# `update`
- [ ] Increment Y positions of both rects by road speed.
- [ ] If first rect is off-screen (bottom), reset its Y position relative to second.
- [ ] If second rect is off-screen (bottom), reset its Y position relative to first.

# `draw`
- [ ] Blit the road image at first rect's position.
- [ ] Blit the road image at second rect's position.