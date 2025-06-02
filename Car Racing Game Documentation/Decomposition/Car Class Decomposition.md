---

kanban-plugin: board

---

## `__init__`

- [ ] Initialise as a Pygame Sprite.
- [ ] Store `self.speed`.
- [ ] Try to:
	- [ ] Load car image and apply `convert_alpha()`.
	- [ ] Get original image dimensions.
	- [ ] Calculate aspect ratio.
	- [ ] Scale image maintaining aspect ratio, assign to `self.image`.
- [ ] On image load error:
	- [ ] Print a warning.
	- [ ] Determine placeholder color based on `is_npc`.
	- [ ] Create and fill a placeholder `pygame.Surface` for `self.image`.
- [ ] Get `self.rect` from `self.image`.
- [ ] Set `self.rect.centerx` and `self.rect.centery`.
- [ ] Create `self.mask` from `self.image`.


## `update`

- [ ] Placeholder method (`pass`).


## `draw`

- [ ] Blit `self.image` onto `screen` at `self.rect`.




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%