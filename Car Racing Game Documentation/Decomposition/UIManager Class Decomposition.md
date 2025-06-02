---
kanban-plugin: board
---
# `__init__`
- [ ] Try to:
    - [ ] Create `self.default_font`.
    - [ ] Create `self.medium_font`.
    - [ ] Create `self.large_font`.
- [ ] On font load error:
    - [ ] Print a warning.
    - [ ] Fallback to system 'arial' font for all fonts.
- [ ] Store `self.text_colour`.
- [ ] Store `self.screen_width` and `self.screen_height`.

# `display_score`
- [ ] Format score string.
- [ ] Render score text surface.
- [ ] Get text surface rectangle.
- [ ] Position score rect at top-left.
- [ ] Blit score surface onto `screen`.

# `display_high_score`
- [ ] Format high score string.
- [ ] Render high score text surface.
- [ ] Get text surface rectangle.
- [ ] Position high score rect at top-right.
- [ ] Blit high score surface onto `screen`.

# `display_game_over`
- [ ] Create and blit a translucent overlay.
- [ ] Render and blit "GAME OVER" text.
- [ ] Render and blit "Final Score: [score]" text.
- [ ] Render and blit "High Score: [high_score]" text.
- [ ] Render and blit "Press R to Restart" text.