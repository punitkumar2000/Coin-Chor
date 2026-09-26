# Cloudbound Trail — 10-Day Team Plan

An original Python/Pygame side-scrolling platform adventure with classic platform-game movement. Characters, names, shapes, levels, and any future audio/art must be original or properly licensed. The Day 1 game uses drawn shapes only.

## Architecture

`main.py` starts `Game`; `game.py` owns the loop, input/events, camera and integration; `player.py` owns player movement and state; `enemy.py` owns enemies and the boss; `objects.py` owns platforms, coins, blocks and power-ups; `levels.py` defines Green Meadow, Crystal Caves and Sky Castle; `ui.py` owns menus, HUD and end screens; `settings.py` stores shared constants; `workload.py` maps people and phases to code. `requirements.txt` lists Pygame.

## Daily plan

Each member owns their listed files for the day. Start each day by pulling the latest shared branch. Work in the assigned file(s), run the shared game, commit and push. If multiple members work at once, use separate branches and merge one at a time; never force-push shared work.

| Day | Person 1 — engine | Person 2 — player | Person 3 — enemies | Person 4 — objects | Person 5 — levels/UI | Shared result |
|---|---|---|---|---|---|---|
| 1 | `main.py`, `game.py`: window, loop, events, drawing | `player.py`: move, jump, gravity, platform landing | `enemy.py`: walking enemy and edge reversal | `objects.py`: platforms and coins | `levels.py`, `ui.py`, `settings.py`, `workload.py`: first stage and HUD | Runnable Green Meadow foundation; these starter files are provided now. |
| 2 | `game.py`: clean update/draw integration | `player.py`: reliable horizontal/vertical collision and fall reset | `enemy.py`: collision result hooks | `objects.py`: solid platform collision helpers | `levels.py`: tune first-stage geometry; `ui.py`: score/lives HUD | Stable single-screen first stage. |
| 3 | `game.py`: camera follows player | `player.py`: facing direction and player states | `enemy.py`: enemy/player contact behavior | `objects.py`: breakable and question blocks | `levels.py`: add block layout | Scrolling Stage 1 with block interactions. |
| 4 | `game.py`: restart and shared game state | `player.py`: temporary power-up state | `enemy.py`: flying enemy | `objects.py`: power-up and moving platform classes | `ui.py`: lives, score, pause prompt | Expanded gameplay objects and flying enemy. |
| 5 | `game.py`: lives and game-over transitions | `player.py`: death/respawn handling | `enemy.py`: `EnemyManager` for multiple enemies | `objects.py`: object interactions and reset behavior | `ui.py`: pause/game-over screens; `levels.py`: finish Stage 1 | Phase 1/2 integration checkpoint. |
| 6 | `game.py`: level-switching interface | `player.py`: preserve/reset stage state correctly | `enemy.py`: enemy variants and balancing | `objects.py`: validate all block/power-up types | `levels.py`: Stage 2 Underground/Crystal Caves | Two-stage game with transition. |
| 7 | `game.py`: transition and full reset | `player.py`: animation hook and power-up effects | `enemy.py`: boss class and health | `objects.py`: final-stage interactions | `ui.py`: boss health display; `levels.py`: Stage 3 layout | Three stages and boss encounter. |
| 8 | `game.py`: win state and integration pass | `player.py`: polish movement feel | `enemy.py`: boss defeat condition | `objects.py`: polish object behavior | `ui.py`: menu, win screen; `levels.py`: connect all stages | Complete game flow: menu → 3 stages → boss → win. |
| 9 | `game.py`, `main.py`: resolve integration issues | `player.py`: fix agreed movement bugs | `enemy.py`: fix agreed enemy/boss bugs | `objects.py`: fix agreed object bugs | `levels.py`, `ui.py`: fix stage/UI bugs; `workload.py`: update index | Feature freeze and one integrated build. |
| 10 | Integration/demo checklist | Explain player code and demo controls | Explain enemy/boss code | Explain objects and Python collections | Explain levels/UI and prepare screenshots/presentation | Final run-through, README, attribution for any assets, and presentation. |

### Daily shared-repo routine

1. At the start of the day, everyone gets the latest shared `main` branch. Assign one person to integrate; others use their own branches if working simultaneously.
2. Before editing, tell the group which file you own. Avoid editing another person's file that day.
3. Run `python main.py` after each integrated change. The integrator resolves conflicts and merges in order.
4. Each contributor commits their own work with a message such as `Day 3: add breakable blocks`, then pushes. Merge branches through a pull request or by the integrator after reviewing the changed files. Never use force-push.
5. End the day only when the integrated game launches and the team can explain the new feature.

For a single shared computer/branch, make commits one at a time: one contributor pulls, commits and pushes; the next contributor pulls before their own commit. Do not have everyone push to the same branch simultaneously.

## Python concepts to show

Variables and types appear in `settings.py`; conditions and loops in update/draw methods; functions in stage builders and game methods; lists in each stage's platforms/enemies/coins; tuples for coin positions; dictionaries for stage information; classes/objects in every game module; imports across modules. Sets and inheritance are planned for later phases and are not implemented yet.

## Day 1 setup

Install Python 3.10+ and Pygame: `python -m pip install -r requirements.txt`. Start the game with `python main.py`. Press Enter, move with arrows or A/D, and jump with Space, Up, or W. The code uses simple shapes so original art can be added later.

**Integration note:** The patrol, jump, shooting-timer, and bullet ideas from the teammate's enemy prototype have been adapted into `enemy.py` and connected through `game.py`. The platformer keeps its own `main.py`; the teammate's standalone main loop was not copied over. The cat image dependency was replaced with original Pygame-drawn shapes, so the game does not need an `enemy.png` file. The integrated version also has three lives, a short hit cooldown, a game-over screen, and an `R` restart.

Day 1 commit suggestion: `Day 1: add playable platformer foundation`.
