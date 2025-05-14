---
kanban-plugin: board
---

# `__init__`
- [ ] Initialise Pygame font module.
- [ ] Create `self.font`.
- [ ] Store `self.text_colour`.

# `_render_text_surface`
- [ ] Create a text surface using font and colour.
- [ ] Return the text surface and its rectangle.

# `display_score`
- [ ] Format score string.
- [ ] Call `_render_text_surface`.
- [ ] Position and blit the score surface.

# `display_high_score`
- [ ] Format high score string.
- [ ] Call `_render_text_surface`.
- [ ] Position and blit the high score surface.

# `display_game_over`
- [ ] Render "GAME OVER" text.
- [ ] Render final score text.
- [ ] Render "High Score: [current_high_score]" text.
- [ ] Render "Press [KEY] to Restart" text.
- [ ] Position and blit all texts.

# `display_message`
- [ ] Use provided or default colour/size.
- [ ] Render the message text.
- [ ] Position and blit the message surface.