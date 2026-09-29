"""Stage layouts. The other two stages are added in later project days."""

from enemy import Enemy
from objects import Coin, Platform, PowerUp


def build_stage_one():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(210, 405, 150),
        Platform(440, 335, 150),
        Platform(700, 405, 170),
        Platform(920, 380, 150),
        Platform(1170, 410, 170),
    ]
    coins = [Coin(x, y) for x, y in [(260, 370), (490, 300), (750, 370), (1060, 315), (1320, 375)]]
    powerups = [PowerUp(740, 370)]
    enemies = [Enemy(560, 460, 520, 650)]
    stage_info = {
    "name": "Green Meadow",
    "number": 1,
    "background": (155, 215, 245),
    }
    return {"platforms": platforms, "coins": coins, "powerups": powerups, "enemies": enemies, "info": stage_info}

def build_stage_two():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 130),
        Platform(370, 345, 140),
        Platform(610, 405, 150),
        Platform(850, 325, 140),
        Platform(1090, 395, 150),
        Platform(1360, 335, 170),
    ]

    coins = [
        Coin(x, y)
        for x, y in [
            (205, 375),
            (415, 310),
            (660, 370),
            (895, 290),
            (1135, 360),
            (1415, 300),
        ]
    ]

    enemies = [
        Enemy(520, 460, 470, 590),
        Enemy(1030, 460, 970, 1080),
    ]

    stage_info = {
    "name": "Moonlit Cave",
    "number": 2,
    "background": (45, 35, 75),
    }

    return {
        "platforms": platforms,
        "coins": coins,
        "enemies": enemies,
        "info": stage_info,
    }

def build_stage_three():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 140),
        Platform(400, 340, 150),
        Platform(660, 405, 150),
        Platform(900, 330, 150),
        Platform(1160, 400, 150),
        Platform(1390, 335, 170),
    ]

    coins = [
        Coin(x, y)
        for x, y in [
            (210, 375),
            (445, 305),
            (705, 370),
            (945, 295),
            (1205, 365),
            (1440, 300),
        ]
    ]

    enemies = [
        Enemy(520, 460, 470, 620),
        Enemy(1050, 460, 990, 1130),
    ]

    stage_info = {
        "name": "Sunset Castle",
        "number": 3,
        "background": (112, 84, 126),
    }

    return {
        "platforms": platforms,
        "coins": coins,
        "enemies": enemies,
        "info": stage_info,
    }