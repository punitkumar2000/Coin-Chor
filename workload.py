"""Team work index: each list points to real code used by that person."""

TEAM_WORK = {
    "Person 1 - Engine and integration": ["game.Game", "game.Game.run", "main.Game"],
    "Person 2 - Player": ["player.Player", "player.Player.update"],
    "Person 3 - Enemies and boss": ["enemy.Enemy", "levels.build_stage_one"],
    "Person 4 - Objects": ["objects.Platform", "objects.Coin"],
    "Person 5 - Stages and interface": ["levels.build_stage_one", "ui.UI"],
}

PHASES = {
    "Phase 1": "Window, controls, first stage, basic enemy and objects",
    "Phase 2": "More collisions, enemy types, moving platforms, pause and second stage",
    "Phase 3": "Power-ups, boss, third stage, menu and final integration",
}
