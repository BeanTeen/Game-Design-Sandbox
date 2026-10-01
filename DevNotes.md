This document is to provide explanations for the game code in this folder. It is being written because the programmer, Bennett, is a massive stoner and often forgets how his own code works. Because writing notes in the program files can look messy if not properly formatted, he has decided to put all the notes here. This document will make it so he doesn't have to constantly google or ask chatgpt what his code does every time he (I) comes back to this project.

Each code segment will have a number and asterisk next to it. look for the corresponding number in this document to learn how the code works.
Each file will have its own number system and be separated accordingly.

Main.py:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

*1: Initialize game. Sets up the Pygame engine, fonts, window size (1400x700), and the initial game state (`'menu'`). It also creates the `Player` object and the static `Platform` list.
*2: `_load_settings` uses `configparser` to read the `settings.ini` file. It uses a `try/except` block so if the file is corrupted or has weird values, the game won't crash—it will just use the fallback defaults (60 FPS, color index 1).
*3: `update` is the brain of the game loop. It processes keyboard events (`pygame.event.get()`) differently depending on whether `self.state` is 'menu', 'settings', or 'game'. If the state is 'game', it triggers the player's update sequence.
*4: `draw` handles all rendering. It wipes the screen with the background color every frame, checks the current state, and draws the appropriate text menus or the actual game world (floor, platforms, player).
\*5: `run` is the main loop. `clock.tick(self.fps)/1000` calculates Delta Time (`dt`), which is the fraction of a second since the last frame. Multiplying movement by `dt` ensures the game runs at the exact same speed regardless of whether your FPS is 30, 60, or 120.

Character.py::::::::::::::::::::::::::::::::::::::::::::::::::::::

*1: `__init__` initializes physics variables. It strictly stores position as floats (`self.x`, `self.y`) because Pygame's `Rect` only holds whole integers. If you only used integers, slow movement calculations would get rounded down to zero and the character would get stuck.
*2: `update` handles movement in two distinct phases to prevent wall-clipping bugs: - **Horizontal First:** It moves the character along the X-axis and checks for platform collisions. If it hits a wall, it pushes the character's bounding box back outside the platform based on which way they were moving. - **Vertical Second:** It applies gravity to `vel_y`, moves the character along the Y-axis, and checks if they hit the `floor_Y` or landed on the _top_ of a platform. If they land, it snaps their feet to the surface, resets `vel_y` to 0, and calls `on_land()`.

Player.py:::::::::::::::::::::::::::::::::::::::::::::::::::::::::

*1: `__init__` inherits the physics from `Character` but adds player-specific stats. Jump power (`jp`) is negative because Pygame's Y-axis starts at 0 at the top of the screen and goes *down*. It also initializes the double jump counter and the list of active lasers.
*2: `jump` checks if the player has jumps left. If so, it snaps the vertical velocity (`vel_y`) directly to the jump power, launching them upward, and decrements the jump counter.
*3: `shoot` figures out which way the player is facing (1 for right, -1 for left), calculates the exact spawn point at the edge of the player's rectangle, and spawns a new `Laser` object into the `lasers` list.
*4: `handle_input` grabs the current state of all keyboard keys. It checks if the Shift key is held down (`pygame.KMOD_SHIFT`) to add a `sprint_speed` bonus, then applies positive or negative velocity based on the Left/Right arrow or A/D keys.
\*5: `update` runs the input check, calls the parent `Character` physics update, and then does two extra things: It clamps the player's X position so they can't walk off the edges of the 1400px screen, and it updates/clears out lasers that have flown off-screen so the game doesn't run out of memory tracking infinite lasers.

Laser.py::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

*1: `__init__` sets the starting position. The `direction` argument (1 or -1) passed from the player is multiplied by the base speed (900) so the laser knows which way to fly across the X-axis.
*2: `update` adds the speed to the X position using Delta Time (`dt`) for smooth movement. It does not check for collisions;
