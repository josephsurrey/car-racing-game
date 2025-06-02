---
kanban-plugin: board
---
# `__init__`
- [ ] Store `screen_width` and `screen_height`.
- [ ] Try to:
    - [ ] Load road image and apply `convert()`.
    - [ ] Get original image dimensions.
    - [ ] Calculate aspect ratio.
    - [ ] Scale image to screen width maintaining aspect ratio, assign to `self.image`.
    - [ ] Store scaled image height in `self.image_height`.
    - [ ] Initialize `self.y1_float` and `self.y2_float` for y-coordinate tracking.
    - [ ] Create `self.rect1` and `self.rect2` at initial y-positions.
- [ ] On image load error:
    - [ ] Print a warning.
    - [ ] Create a black placeholder `pygame.Surface`.

# `update`
- [ ] Increment `self.y1_float` and `self.y2_float` by `current_road_speed`.
- [ ] Update `self.rect1.y` and `self.rect2.y` from float counterparts.
- [ ] If `self.rect1` scrolls off bottom, reset its `self.y1_float` relative to `self.y2_float`.
- [ ] Else if `self.rect2` scrolls off bottom, reset its `self.y2_float` relative to `self.y1_float`.

# `draw`
- [ ] Blit `self.image` at `self.rect1` position.
- [ ] Blit `self.image` at `self.rect2` position.