# JumpByte

JumpByte is an original 2D platformer made with Python and Pygame. Play as a rat, explore three worlds, collect coins and a speed-boost power-up, and avoid the cat enemy.

This is an educational, AI-assisted project. The leader integrated the code and managed the daily commits and pushes. Team members prepared to explain and demonstrate assigned modules.

## Features

- Three worlds: Green Meadow, Moonlit Cave, and Sunset Castle
- Rat character with movement, jumping, gravity, and platform collisions
- Cat enemy with patrol and projectile behavior
- Coins and a temporary speed-boost power-up
- Lives, respawn, game-over, and restart
- Different backgrounds and original Pygame-drawn scenery
- Pause and resume

## Controls

| Key | Action |
| --- | --- |
| Enter | Start the game |
| A / D or Left / Right arrows | Move |
| Space, Up arrow, or W | Jump |
| P | Pause or resume |
| R | Restart after game over or winning |

Reach the flag at the right side of each world to continue. Coins are optional.

## Run on macOS

From the project folder, open Terminal and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py

